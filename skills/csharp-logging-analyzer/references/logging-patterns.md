# C# .NET Logging Patterns Reference

## Table of Contents
1. [Log Levels](#log-levels)
2. [ILogger Basics](#ilogger-basics)
3. [Structured Logging](#structured-logging)
4. [High-Performance Logging](#high-performance-logging)
5. [Correlation & Scopes](#correlation--scopes)
6. [Docker / Journal Output](#docker--journal-output)
7. [Distributed Tracing Integration](#distributed-tracing-integration)
8. [Async Logging Pitfalls](#async-logging-pitfalls)
9. [Common Anti-Patterns](#common-anti-patterns)
10. [Framework-Specific Notes](#framework-specific-notes)

---

## Log Levels

Use these guidelines to pick the right level. Being consistent matters more than being "right" —
pick a convention and stick to it across the codebase.

| Level | When to Use | Example |
|-------|-------------|---------|
| **Trace** | Ultra-verbose, inner-loop diagnostics. Almost never on in production. | `Evaluating cache key {Key}` |
| **Debug** | Developer-useful context. On during incident investigation. | `Resolved dependency {Type} from container` |
| **Information** | Key business events that operators want to see in normal operation. | `Order {OrderId} created for customer {CustomerId}` |
| **Warning** | Something unexpected but recoverable. Needs attention eventually. | `Retry {Attempt}/{MaxRetries} for {Endpoint} after {ErrorType}` |
| **Error** | An operation failed. Requires investigation. Include the exception. | `Failed to process payment for order {OrderId}` |
| **Critical** | The application or a major subsystem is about to crash or is unusable. | `Database connection pool exhausted, no connections available` |

### Level selection heuristics
- If the log fires on every request → probably **Debug** or **Trace** (not Information)
- If the log represents a business outcome → **Information**
- If something failed but the system recovered → **Warning**
- If you'd wake someone up for it → **Error** or **Critical**

---

## ILogger Basics

### Constructor injection (preferred)

```csharp
public class OrderService
{
    private readonly ILogger<OrderService> _logger;

    public OrderService(ILogger<OrderService> logger)
    {
        _logger = logger;
    }

    public void PlaceOrder(Order order)
    {
        _logger.LogInformation("Placing order {OrderId} for customer {CustomerId}",
            order.Id, order.CustomerId);

        // ... business logic ...
    }
}
```

### Static class / extension method logging

For static helpers or extension methods, accept `ILogger` as a parameter or use
`ILoggerFactory`:

```csharp
public static class RetryHelper
{
    public static async Task<T> WithRetry<T>(
        Func<Task<T>> action,
        int maxRetries,
        ILogger logger)
    {
        for (int attempt = 1; attempt <= maxRetries; attempt++)
        {
            try
            {
                return await action();
            }
            catch (Exception ex) when (attempt < maxRetries)
            {
                logger.LogWarning(ex,
                    "Attempt {Attempt}/{MaxRetries} failed, retrying",
                    attempt, maxRetries);
            }
        }
        return await action(); // Final attempt, let exception propagate
    }
}
```

---

## Structured Logging

### DO: Use message templates with named placeholders

```csharp
_logger.LogInformation("Processing order {OrderId} with {ItemCount} items",
    order.Id, order.Items.Count);
// Produces structured properties: OrderId="ORD-123", ItemCount=5
```

### DON'T: Use string interpolation

```csharp
// BAD — destroys structured logging, prevents log aggregation
_logger.LogInformation($"Processing order {order.Id} with {order.Items.Count} items");
```

### DON'T: Use string.Format or concatenation

```csharp
// BAD — same problem as interpolation
_logger.LogInformation("Processing order " + order.Id);
_logger.LogInformation(string.Format("Processing order {0}", order.Id));
```

### Property naming conventions
- Use **PascalCase**: `{OrderId}`, `{CustomerId}`, `{ElapsedMs}`
- Be specific: `{SourceEndpoint}` not `{Url}`
- Use `@` prefix for destructured objects: `{@OrderDetails}`
- Avoid generic names: `{Value}`, `{Data}`, `{Item}` — they're useless in queries

### Log exception objects properly

```csharp
// GOOD — exception is the first parameter to LogError/LogWarning
try { /* ... */ }
catch (Exception ex)
{
    _logger.LogError(ex, "Failed to process order {OrderId}", order.Id);
    // The exception's full stack trace, message, and inner exceptions
    // are captured automatically as structured data
}

// BAD — exception detail lost or mangled
catch (Exception ex)
{
    _logger.LogError("Failed to process order {OrderId}: {Error}",
        order.Id, ex.ToString()); // Stack trace in message field — can't query it
}
```

---

## High-Performance Logging

For hot paths (code that runs many times per second), avoid allocations in log calls.

### [LoggerMessage] Source Generator (.NET 6+) — PREFERRED

```csharp
public static partial class Log
{
    [LoggerMessage(
        EventId = 1001,
        Level = LogLevel.Information,
        Message = "Processing order {OrderId} with {ItemCount} items")]
    public static partial void ProcessingOrder(
        this ILogger logger, string orderId, int itemCount);

    [LoggerMessage(
        EventId = 1002,
        Level = LogLevel.Warning,
        Message = "Order {OrderId} processing slow, elapsed {ElapsedMs}ms")]
    public static partial void OrderProcessingSlow(
        this ILogger logger, string orderId, long elapsedMs);

    [LoggerMessage(
        EventId = 2001,
        Level = LogLevel.Error,
        Message = "Failed to process order {OrderId}")]
    public static partial void OrderProcessingFailed(
        this ILogger logger, Exception exception, string orderId);
}

// Usage:
_logger.ProcessingOrder(order.Id, order.Items.Count);
_logger.OrderProcessingSlow(order.Id, stopwatch.ElapsedMilliseconds);
_logger.OrderProcessingFailed(ex, order.Id);
```

Benefits:
- Zero allocation when log level is disabled (the generated code checks `IsEnabled` automatically)
- Compile-time validation of message template parameters
- Consistent EventId assignment

### LoggerMessage.Define (.NET Core 2.1+ / older .NET)

```csharp
public static class LogMessages
{
    private static readonly Action<ILogger, string, int, Exception?> _processingOrder =
        LoggerMessage.Define<string, int>(
            LogLevel.Information,
            new EventId(1001, nameof(ProcessingOrder)),
            "Processing order {OrderId} with {ItemCount} items");

    public static void ProcessingOrder(this ILogger logger, string orderId, int itemCount)
        => _processingOrder(logger, orderId, itemCount, null);
}
```

### When to use high-performance logging
- Any log that fires per-request in a high-throughput service
- Logs inside loops or batch-processing code
- Middleware / pipeline code that runs on every request
- Background workers processing queues at high rates

### Guard clauses for expensive log data assembly

```csharp
// Only compute the expensive data if Debug logging is on
if (_logger.IsEnabled(LogLevel.Debug))
{
    var diagnosticData = ComputeExpensiveDiagnostics(order);
    _logger.LogDebug("Order diagnostics: {@Diagnostics}", diagnosticData);
}
```

---

## Correlation & Scopes

### Log scopes for contextual properties

```csharp
public async Task<IActionResult> ProcessOrder(OrderRequest request)
{
    using (_logger.BeginScope(new Dictionary<string, object>
    {
        ["CorrelationId"] = HttpContext.TraceIdentifier,
        ["OrderId"] = request.OrderId,
        ["CustomerId"] = request.CustomerId
    }))
    {
        _logger.LogInformation("Order processing started");
        // Every log inside this scope automatically includes
        // CorrelationId, OrderId, and CustomerId
        await _orderService.Process(request);
        _logger.LogInformation("Order processing completed");
    }
}
```

### ASP.NET Core request logging middleware

```csharp
// In Program.cs or Startup.cs
app.Use(async (context, next) =>
{
    var logger = context.RequestServices.GetRequiredService<ILogger<Program>>();
    var sw = Stopwatch.StartNew();

    using (logger.BeginScope(new Dictionary<string, object>
    {
        ["CorrelationId"] = context.TraceIdentifier,
        ["RequestPath"] = context.Request.Path.Value ?? "",
        ["RequestMethod"] = context.Request.Method
    }))
    {
        try
        {
            await next();
        }
        finally
        {
            sw.Stop();
            logger.LogInformation(
                "HTTP {Method} {Path} responded {StatusCode} in {ElapsedMs}ms",
                context.Request.Method,
                context.Request.Path,
                context.Response.StatusCode,
                sw.ElapsedMilliseconds);
        }
    }
});
```

---

## Docker / Journal Output

### Console output for Docker (stdout/stderr → docker journal)

```csharp
// Program.cs — minimal configuration for Docker
builder.Logging.ClearProviders();
builder.Logging.AddConsole(options =>
{
    options.FormatterName = "json"; // JSON for structured log aggregation
});
// Or use the simpler:
builder.Logging.AddJsonConsole();
```

### Serilog console sink for Docker

```csharp
Log.Logger = new LoggerConfiguration()
    .WriteTo.Console(new CompactJsonFormatter()) // or RenderedCompactJsonFormatter
    .CreateLogger();
```

### File output for disk logging

```csharp
// Serilog file sink with rolling (most common approach)
Log.Logger = new LoggerConfiguration()
    .WriteTo.File(
        path: "logs/app-.log",
        rollingInterval: RollingInterval.Day,
        retainedFileCountLimit: 30,
        fileSizeLimitBytes: 100_000_000, // 100MB per file
        formatter: new CompactJsonFormatter())
    .CreateLogger();

// NOTE: Microsoft.Extensions.Logging does NOT have a built-in file provider.
// For file logging without Serilog, use a third-party package:
//   - Serilog.Extensions.Logging.File (lightweight, via builder.Logging.AddFile(...))
//   - NReco.Logging.File
//   - NetEscapades.Extensions.Logging.RollingFile
// If the codebase already uses one of these, match it. Otherwise prefer Serilog.
```

### systemd journal (Linux containers)

For Linux/Docker deployments, the standard approach is logging to **stdout** (console sink),
which systemd and Docker automatically capture. A dedicated journal sink is rarely needed:

```csharp
// Preferred: just log to console — Docker and systemd capture stdout automatically
builder.Logging.AddJsonConsole();

// If you specifically need systemd journal metadata (PRIORITY, SYSLOG_IDENTIFIER, etc.),
// use Serilog.Sinks.SystemdJournal — but this is an uncommon requirement:
// Log.Logger = new LoggerConfiguration()
//     .WriteTo.SystemdJournal()
//     .CreateLogger();
```

### Best practices for containerized apps
- Log to **stdout** (console) as primary output — let the orchestrator handle routing
- Use **JSON** format for machine-readable structured logs
- Include the **service name**, **version**, and **environment** in every log
- Set `Logging:LogLevel:Default` via environment variables for runtime tuning
- Avoid file logging inside containers unless you're mounting a volume

---

## Distributed Tracing Integration

If the codebase uses OpenTelemetry or `System.Diagnostics.Activity`, logs should be correlated
with traces automatically. Modern .NET logging integrates with `Activity.Current`:

```csharp
// .NET 6+ automatically attaches Activity.TraceId and SpanId to log scopes
// when using Microsoft.Extensions.Logging with OpenTelemetry.
// No manual correlation ID needed if OpenTelemetry is configured:
builder.Services.AddOpenTelemetry()
    .WithTracing(b => b.AddAspNetCoreInstrumentation()
                       .AddHttpClientInstrumentation());

// If NOT using OpenTelemetry, manually propagate correlation via HttpContext.TraceIdentifier
// (see Correlation & Scopes section above)
```

When analyzing a codebase, check if OpenTelemetry is already configured. If so, DO NOT add
manual correlation ID propagation — it would be redundant. Instead, ensure logs are enriched
with the existing trace context.

---

## Async Logging Pitfalls

### Log scopes and async/await

`BeginScope` works correctly with async/await as long as the `using` block wraps the `await`:

```csharp
// GOOD — scope survives the await
using (_logger.BeginScope("OrderId={OrderId}", orderId))
{
    await ProcessAsync();   // scope is active here
    await SaveAsync();      // and here
}

// BAD — scope lost after fire-and-forget
using (_logger.BeginScope("OrderId={OrderId}", orderId))
{
    _ = Task.Run(() => ProcessAsync()); // scope NOT available inside Task.Run
}
```

### Avoid async void with logging

```csharp
// BAD — async void loses exception context and scope
async void HandleEvent(object sender, EventArgs e)
{
    _logger.LogInformation("Handling event"); // may lose scope
    await DoWorkAsync(); // exceptions won't be caught
}

// GOOD — use async Task and log errors explicitly
async Task HandleEventAsync(object sender, EventArgs e)
{
    try
    {
        _logger.LogInformation("Handling event");
        await DoWorkAsync();
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Event handling failed");
    }
}
```

---

## Common Anti-Patterns

### 1. Swallowed exceptions
```csharp
// BAD — failure is invisible
catch (Exception) { /* do nothing */ }

// GOOD — at minimum, log it
catch (Exception ex)
{
    _logger.LogError(ex, "Unexpected error in {Method}", nameof(ProcessOrder));
    throw; // or handle appropriately
}
```

### 2. Logging sensitive data
```csharp
// BAD — PII/secrets in logs
_logger.LogInformation("User {Email} logged in with token {Token}", email, token);

// GOOD — redact sensitive fields
_logger.LogInformation("User {UserId} logged in", user.Id);
```

### 3. Inconsistent log messages for the same operation
```csharp
// BAD — hard to correlate
_logger.LogInformation("starting order");      // in method A
_logger.LogInformation("Order has started!");   // in method B (same operation)

// GOOD — consistent naming
_logger.LogInformation("Order {OrderId} processing started", orderId);
_logger.LogInformation("Order {OrderId} processing completed in {ElapsedMs}ms",
    orderId, elapsed);
```

### 4. Using string interpolation
```csharp
// BAD — allocates string even if log level is disabled
_logger.LogDebug($"Cache hit for key {key}");

// GOOD — no allocation if Debug is off
_logger.LogDebug("Cache hit for key {CacheKey}", key);
```

### 5. Logging inside tight loops without level guard
```csharp
// BAD — thousands of allocations per second even if Trace is off
foreach (var item in bigList)
{
    _logger.LogTrace("Processing item {ItemId}", item.Id);
}

// GOOD — guard the loop-interior log
var traceEnabled = _logger.IsEnabled(LogLevel.Trace);
foreach (var item in bigList)
{
    if (traceEnabled)
        _logger.LogTrace("Processing item {ItemId}", item.Id);
}
```

---

## Framework-Specific Notes

### Serilog

If the codebase uses Serilog, follow these conventions:
- Use `Log.ForContext<T>()` for static contexts
- Use `{@Object}` for destructuring complex objects
- Enrichers add global properties: `.Enrich.WithMachineName().Enrich.WithEnvironmentName()`
- Use `Serilog.Expressions` or `Serilog.Formatting.Compact` for output formatting

### NLog

If the codebase uses NLog:
- Configure via `nlog.config` XML or programmatically
- Use `${mdlc:CorrelationId}` in layouts for mapped diagnostic context
- NLog's structured logging uses `@` prefix: `logger.Info("Order {@Order}", order)`

### Microsoft.Extensions.Logging (default)

- Configured in `appsettings.json` under `"Logging"` section
- Supports scopes natively with `BeginScope`
- Use `[LoggerMessage]` attribute for source-generated high-perf logging
- EventIds are optional but useful for filtering: `new EventId(1001, "OrderCreated")`
