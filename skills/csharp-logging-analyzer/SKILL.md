---
name: csharp-logging-analyzer
description: >
  Analyzes a C# .NET codebase and produces a comprehensive, actionable logging plan (logging_plan.md)
  to improve debugging and production traceability. Use this skill whenever the user asks to
  "add logging", "improve logging", "create a logging plan", "analyze logging gaps",
  "improve traceability", or "improve debuggability" for a C# / .NET project. Also trigger when
  the user mentions missing logs, production debugging issues, log coverage, structured logging,
  or wants to instrument a .NET codebase with ILogger / Serilog / NLog patterns. Even if the user
  just says "help me debug this in production" for a C# project, this skill applies.
---

# C# .NET Logging Analyzer & Plan Generator

You analyze a C# .NET codebase, identify logging gaps, and produce a detailed `logging_plan.md`
that a developer (or Claude) can follow to add production-grade logging with unit tests.

## High-Level Workflow

```
1. DISCOVER  → Scan codebase structure, find existing logging patterns
2. ANALYZE   → Identify gaps and missing logging scenarios
3. PLAN      → Write logging_plan.md with specific, line-level recommendations
4. TEST      → Generate unit test code for the proposed logging
5. REVIEW    → Self-review the plan for accuracy, optimality, and consistency
```

Before starting, read the reference files for detailed guidance:
- `references/logging-patterns.md` — Standard C# logging patterns, performance tips, log levels
- `references/analysis-checklist.md` — Exhaustive checklist of what to look for during analysis

---

## Step 1: DISCOVER — Scan the Codebase

### 1a. Map the project structure

```bash
find <codebase_root> -name '*.csproj' -o -name '*.sln' | head -50
find <codebase_root> -name '*.cs' | head -200
```

Identify: solution files, project files, entry points (`Program.cs`, `Startup.cs`), layers
(Controllers, Services, Repositories, Middleware, Background Services, etc.).

### 1b. Detect existing logging infrastructure

Search for these patterns to understand what's already in place:

```bash
# Logging frameworks
grep -rn "using Microsoft.Extensions.Logging" <root> --include="*.cs" | head -30
grep -rn "using Serilog" <root> --include="*.cs" | head -30
grep -rn "using NLog" <root> --include="*.cs" | head -30

# Logger injection and existing log calls
grep -rnE "ILogger<|ILoggerFactory" <root> --include="*.cs" | head -30
grep -rnE "\.(Log|LogInformation|LogWarning|LogError|LogDebug|LogCritical|LogTrace)\(" <root> --include="*.cs" | head -60

# Log configuration
grep -rnE "AddSerilog|AddNLog|AddConsole|AddDebug|AddEventLog|AddJsonConsole" <root> --include="*.cs" | head -20
find <root> -name "appsettings*.json" -exec head -50 {} +

# High-performance logging (LoggerMessage.Define / [LoggerMessage])
grep -rnE "LoggerMessage\.Define|\[LoggerMessage" <root> --include="*.cs" | head -20

# .NET version (needed to determine LoggerMessage source gen support)
grep -rn "TargetFramework" <root> --include="*.csproj" | head -10

# Existing test frameworks (needed to match test patterns in Step 4)
grep -rnE "using Xunit|using NUnit|using Microsoft.VisualStudio.TestTools" <root> --include="*.cs" | head -10
grep -rnE "using Moq|using NSubstitute|using FakeItEasy" <root> --include="*.cs" | head -10
```

### 1c. Determine the logging standard to follow

**Critical rule:** If the codebase already uses a logging framework or pattern, FOLLOW IT.
Do not introduce a new framework. Match the existing style exactly (naming, message templates,
log levels, structured properties).

If NO logging exists, default to:
- `Microsoft.Extensions.Logging` (`ILogger<T>`) as the abstraction
- High-performance `[LoggerMessage]` source-generated attributes (.NET 6+) or
  `LoggerMessage.Define` (older .NET) for hot paths — **check `TargetFramework` in .csproj to
  decide which to use** (e.g., `net8.0` → use `[LoggerMessage]`, `netcoreapp3.1` → use `Define`)
- Structured logging with message templates (NO string interpolation in log calls)

Also record:
- The **.NET version** (from TargetFramework) — this determines available logging APIs
- The **test framework** in use (xUnit, NUnit, MSTest) and mocking library (Moq, NSubstitute) —
  needed to write matching unit tests in Step 4
- Whether the project uses **dependency injection** — services without `ILogger<T>` injection are
  themselves a gap to flag

---

## Step 2: ANALYZE — Identify Logging Gaps

Read `references/analysis-checklist.md` for the full checklist. The categories below are a summary.

For each `.cs` file (prioritize by importance: entry points > middleware > services > repositories > models):

### Categories of logging gaps

1. **Application Lifecycle** — Startup, shutdown, configuration loaded, feature flags, dependency health checks
2. **Request/Response Pipeline** — Incoming requests, outgoing responses, correlation IDs, request duration
3. **Business Logic** — Key decision branches, state transitions, domain events, validation failures
4. **External Integrations** — HTTP calls, database queries, message queue publish/consume, file I/O, cache hits/misses
5. **Error Handling** — All catch blocks, unhandled exceptions, fallback paths, circuit breaker state changes
6. **Security** — Authentication attempts, authorization failures, token validation, suspicious activity
7. **Performance** — Slow operations, timeout thresholds, batch sizes, queue depths, retry counts
8. **Background Processing** — Job start/complete/fail, scheduling, dequeue events, dead-letter handling

For EACH gap found, record:
- **File** and **line number** (or method name)
- **What's missing** — describe the log statement(s) needed
- **Log level** — Trace/Debug/Information/Warning/Error/Critical
- **Why it matters** — what production problem this log would help diagnose
- **Structured properties** — which values to capture as structured log properties

### Prioritization

Assign each recommendation a priority:

| Priority | Criteria |
|----------|----------|
| **P0 — Critical** | Error/catch blocks with no logging; unobservable failures |
| **P1 — High** | Missing request/response tracing; external call logging |
| **P2 — Medium** | Business logic branches; performance-sensitive operations |
| **P3 — Low** | Verbose debug/trace logging; nice-to-have context |

---

## Step 3: PLAN — Write logging_plan.md

Create the file at the codebase root (or wherever the user specifies). Use this exact structure:

```markdown
# Logging Improvement Plan

## 1. Executive Summary
Brief overview: how many gaps found, top priorities, estimated effort.

## 2. Current Logging State
- Framework(s) in use
- Logging configuration (sinks, levels, format)
- Existing patterns (code examples from the codebase)
- Coverage assessment (which layers have logging, which don't)

## 3. Logging Standards
- Framework to use (match existing or recommend)
- Log level guidelines (when to use each level — be specific to THIS codebase)
- Message template conventions (naming, structured properties)
- Performance guidelines (when to use LoggerMessage source gen, when to guard with IsEnabled)
- Correlation / tracing strategy (how to propagate correlation IDs)

## 4. Gap Analysis by Category
For each category (Lifecycle, Request Pipeline, Business Logic, etc.):

### 4.X [Category Name]

#### [File:Method or Component]
- **Location:** `path/to/File.cs`, line ~N (or method name)
- **Priority:** P0/P1/P2/P3
- **Current behavior:** What happens now (no log, insufficient log, etc.)
- **Recommended log:**
  ```csharp
  // Exact code to add — use the project's actual class/variable names
  _logger.LogInformation("Order {OrderId} placed by {CustomerId} with {ItemCount} items",
      order.Id, order.CustomerId, order.Items.Count);
  ```
- **Rationale:** Why this log is needed for production debugging

## 5. Logging Configuration
Recommended appsettings.json logging section (or Serilog/NLog config).
Include minimum log levels per category, sink configuration for the target
deployment environment (Docker stdout, file on disk, both), and runtime
override guidance (environment variables, Azure App Configuration, etc.).

```json
// Example for appsettings.json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning",
      "Microsoft.EntityFrameworkCore": "Warning",
      "YourApp.Namespace": "Debug"
    }
  }
}
```

## 6. High-Performance Logging Patterns
Show how to define LoggerMessage source-generated methods for any hot-path logs.
Include concrete examples from the codebase.

```csharp
// Example using [LoggerMessage] attribute (.NET 6+)
public static partial class LogMessages
{
    [LoggerMessage(Level = LogLevel.Information, Message = "Processing order {OrderId}")]
    public static partial void ProcessingOrder(this ILogger logger, string orderId);
}
```

## 7. Unit Tests for Logging
Provide test code verifying that key log statements fire with correct level and message.
See the "Unit Tests" section below for patterns.

## 8. Implementation Checklist
Ordered list of tasks a developer can follow, grouped by priority.
Include estimated LOC changes per task.

## 9. Review Notes
Self-review observations: consistency, coverage completeness, potential issues.
```

### Writing guidelines for the plan

- **Be concrete.** Every recommendation must include actual code using real class names, variable
  names, and namespaces from the codebase. Never write placeholder code like `// add logging here`.
- **Use structured logging.** All message templates must use `{PropertyName}` placeholders,
  NEVER string interpolation (`$"..."`). This is critical for log aggregation and search.
- **Respect log levels.** Don't over-log at Information. Use Debug/Trace for verbose output.
  Use Warning for recoverable issues. Use Error only for actual errors. Use Critical for
  catastrophic failures.
- **Consider performance.** For any log in a tight loop or hot path, use `[LoggerMessage]`
  source-generated logging or guard with `if (_logger.IsEnabled(LogLevel.Debug))`.

---

## Step 4: TEST — Generate Unit Tests

Include test code in section 7 of the plan AND as separate test file suggestions.

**Important:** Match the test framework and mocking library already in use in the codebase (detected
in Step 1b). If xUnit + Moq is used, write xUnit + Moq tests. If NUnit + NSubstitute, match that.
If no test project exists, default to xUnit + Moq and suggest creating a test project.

### Test patterns to use

**Pattern A: Verify logging with `ILogger<T>` mock (using Moq or NSubstitute)**

```csharp
[Fact]
public void ProcessOrder_LogsInformationWithOrderId()
{
    // Arrange
    var logger = new Mock<ILogger<OrderService>>();
    var service = new OrderService(logger.Object);

    // Act
    service.ProcessOrder(new Order { Id = "ORD-123" });

    // Assert — verify LogInformation was called
    // NOTE: For non-error logs, the exception param is null.
    // For LogError/LogWarning WITH exception, use It.IsAny<Exception?>() instead of null.
    logger.Verify(
        x => x.Log(
            LogLevel.Information,
            It.IsAny<EventId>(),
            It.Is<It.IsAnyType>((o, t) => o.ToString()!.Contains("ORD-123")),
            It.IsAny<Exception?>(),
            It.IsAny<Func<It.IsAnyType, Exception?, string>>()),
        Times.Once);
}

[Fact]
public void ProcessOrder_WhenFails_LogsErrorWithException()
{
    // Arrange
    var logger = new Mock<ILogger<OrderService>>();
    var service = new OrderService(logger.Object);

    // Act
    Assert.Throws<InvalidOperationException>(() =>
        service.ProcessOrder(new Order { Id = "BAD-ORDER" }));

    // Assert — verify LogError was called WITH an exception object
    logger.Verify(
        x => x.Log(
            LogLevel.Error,
            It.IsAny<EventId>(),
            It.Is<It.IsAnyType>((o, t) => o.ToString()!.Contains("BAD-ORDER")),
            It.IsNotNull<Exception?>(),
            It.IsAny<Func<It.IsAnyType, Exception?, string>>()),
        Times.Once);
}
```

**Pattern B: Use `FakeLogger` (Microsoft.Extensions.Diagnostics.Testing, .NET 8+)**

```csharp
[Fact]
public void ProcessOrder_LogsExpectedMessage()
{
    // Arrange
    var fakeLogger = new FakeLogger<OrderService>();
    var service = new OrderService(fakeLogger);

    // Act
    service.ProcessOrder(new Order { Id = "ORD-123" });

    // Assert
    var record = Assert.Single(fakeLogger.Collector.GetSnapshot());
    Assert.Equal(LogLevel.Information, record.Level);
    Assert.Contains("ORD-123", record.Message);
}
```

**Pattern C: Custom test sink / collector for integration tests**

```csharp
public class TestLogSink : ILoggerProvider
{
    public ConcurrentBag<(LogLevel Level, string Message)> Logs { get; } = new();

    public ILogger CreateLogger(string categoryName) => new TestLogger(this);
    public void Dispose() { }

    private class TestLogger(TestLogSink sink) : ILogger
    {
        public IDisposable? BeginScope<TState>(TState state) where TState : notnull => null;
        public bool IsEnabled(LogLevel logLevel) => true;
        public void Log<TState>(LogLevel logLevel, EventId eventId, TState state,
            Exception? exception, Func<TState, Exception?, string> formatter)
            => sink.Logs.Add((logLevel, formatter(state, exception)));
    }
}
```

Generate tests for at minimum:
- All P0 (Critical) logging additions
- A representative sample of P1 (High) additions
- Error/exception logging paths
- Any `[LoggerMessage]` source-generated methods

---

## Step 5: REVIEW — Self-Review the Plan

After generating `logging_plan.md`, perform these review checks:

### Accuracy checks
- [ ] Every file path and class name referenced in the plan actually exists in the codebase
- [ ] Every code snippet compiles conceptually (correct using statements, correct method signatures)
- [ ] Log levels are appropriate (not over-logging at Information, not under-logging errors)
- [ ] Structured property names follow consistent PascalCase naming
- [ ] The plan does NOT recommend string interpolation in log calls

### Optimality checks
- [ ] Hot-path logging uses `[LoggerMessage]` or `LoggerMessage.Define` (not direct `_logger.Log*`)
- [ ] No redundant logs (same information logged twice at the same level in the same flow)
- [ ] Exception objects are passed as the `exception` parameter, not `.ToString()` in message
- [ ] Sensitive data (passwords, tokens, PII) is NOT included in log messages
- [ ] Log messages are unique enough to identify the exact location in code

### Consistency checks
- [ ] All recommendations follow the SAME logging framework the codebase already uses
- [ ] Message template style is consistent (e.g., "Verb-ing noun {Property}" pattern)
- [ ] Log level choices are consistent across similar operations
- [ ] Test patterns match the test framework already in use in the codebase

### Completeness checks
- [ ] Every public method in service/controller layers has at least entry-level logging
- [ ] Every catch block either logs or re-throws (no swallowed exceptions without logging)
- [ ] External integration points have timing/outcome logging
- [ ] The implementation checklist is ordered by priority (P0 first)

If any check fails, FIX the plan before presenting it. Include a "Review Notes" section at the
bottom of the plan documenting what was checked and any trade-offs made.

---

## Output

The primary output is `logging_plan.md` saved to the codebase root (or user-specified location).
Copy it to `/mnt/user-data/outputs/logging_plan.md` for the user to download.

If the user asks Claude to also implement the changes (not just plan), Claude should follow the
plan to make the actual code changes, but that's a separate step — the plan always comes first.
