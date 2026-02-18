# Logging Gap Analysis Checklist

Use this checklist when scanning each file/layer of the codebase. Not every item applies to
every codebase — skip what's irrelevant. But walk through each category systematically.

---

## 1. Application Lifecycle

- [ ] **Startup** — Is there a log when the application starts? Including:
  - Application name and version
  - Environment (Development / Staging / Production)
  - Loaded configuration sources
  - Key configuration values (non-sensitive: port, endpoints, feature flags)
- [ ] **Shutdown** — Is there a log on graceful shutdown? Including:
  - Shutdown reason if available
  - In-flight request count at shutdown
  - Time taken to drain
- [ ] **Health checks** — If health check endpoints exist, do they log failures?
- [ ] **Dependency readiness** — On startup, are dependency connections logged?
  - Database connection established / failed
  - Cache (Redis, etc.) connected
  - Message broker connected
  - External service reachable

---

## 2. Request / Response Pipeline (ASP.NET Core)

- [ ] **Incoming request** — Is each HTTP request logged with:
  - Method, path, query string (sanitized)
  - Correlation ID / trace ID
  - Client IP (if appropriate)
  - Authenticated user ID
- [ ] **Response** — Is the response logged with:
  - Status code
  - Duration (elapsed time)
  - Response size (for large payloads)
- [ ] **Request body** — For POST/PUT, is the body logged at Debug level (with PII redaction)?
- [ ] **Middleware** — Custom middleware should log its action:
  - Authentication middleware: auth result
  - Rate limiting: throttled requests
  - CORS: blocked origins
- [ ] **Model validation** — Are `ModelState` validation failures logged?
- [ ] **Routing** — Are 404s and routing failures logged with the attempted path?
- [ ] **Minimal APIs** — If using `.MapGet()` / `.MapPost()` etc.:
  - Same request/response logging standards as controllers
  - Endpoint filters should log their actions
- [ ] **gRPC services** — If using gRPC:
  - Incoming call: service/method name, metadata
  - Response: status code, duration
  - Streaming: stream start/end, message counts
- [ ] **SignalR hubs** — If using SignalR:
  - Connection established/disconnected: connection ID, user ID
  - Hub method invoked: method name, caller
  - Group membership changes

---

## 3. Business Logic / Services

- [ ] **Method entry/exit** — For key service methods, are entry and exit logged?
  - Entry: input parameters (sanitized)
  - Exit: outcome, duration
- [ ] **Decision branches** — Where code takes different paths based on conditions:
  - Which branch was taken and why
  - The data that drove the decision
  ```csharp
  // Example: decision branch logging
  if (customer.IsVip)
  {
      _logger.LogInformation("Applying VIP discount for customer {CustomerId}", customer.Id);
      ApplyVipDiscount(order);
  }
  else
  {
      _logger.LogDebug("Standard pricing for customer {CustomerId}", customer.Id);
  }
  ```
- [ ] **State transitions** — When entities change state:
  - Previous state → new state
  - Who/what triggered the transition
  - `_logger.LogInformation("Order {OrderId} state changed from {OldStatus} to {NewStatus}", ...)`
- [ ] **Validation failures** — Business rule validation (not just model binding):
  - What rule failed
  - What data caused the failure
- [ ] **Domain events** — If using domain events / event sourcing:
  - Event type, aggregate ID, event data

---

## 4. Data Access / Repository Layer

- [ ] **Query execution** — Are significant database operations logged?
  - Log at Debug level: query description, parameters
  - Log at Warning level: slow queries (> threshold)
  - Log at Error level: query failures
- [ ] **Connection issues** — Database connection failures, timeouts, retries
- [ ] **Transactions** — Transaction begin, commit, rollback
  - Especially rollbacks — always log why
- [ ] **Bulk operations** — Batch insert/update/delete:
  - Record count, duration
- [ ] **EF Core** — If using Entity Framework:
  - Consider enabling EF Core logging at Debug level for SQL queries
  - Log SaveChanges failures with entity details
- [ ] **Caching** — Cache operations:
  - Cache hit/miss at Debug level
  - Cache invalidation at Information level
  - Cache connection failures at Error level

---

## 5. External Integration Points

- [ ] **HTTP client calls** — Every outbound HTTP call should log:
  - Request: method, URL, key headers (at Debug)
  - Response: status code, duration
  - Failure: exception, retry count
  - Use `IHttpClientFactory` with `DelegatingHandler` for centralized logging
- [ ] **Message queues** — Publish/consume operations:
  - Message published: queue/topic, message type, correlation ID
  - Message received: queue/topic, message type, correlation ID
  - Processing completed/failed: duration, error details
  - Dead-letter events
- [ ] **File I/O** — File system operations:
  - File read/write: path, size
  - File not found: at Warning
  - Permission errors: at Error
- [ ] **Email/SMS/Notifications** — External notification sends:
  - Sent: recipient (masked), type
  - Failed: error, retry plan
- [ ] **Third-party APIs** — Same as HTTP calls but include:
  - API name, operation, rate limit headers

---

## 6. Error Handling

- [ ] **Catch blocks** — EVERY catch block must either:
  1. Log the exception and handle it, OR
  2. Re-throw (in which case a higher-level handler logs it)
  - Never silently swallow exceptions
- [ ] **Global exception handler** — Is there a global handler that:
  - Logs unhandled exceptions at Error/Critical
  - Includes correlation ID
  - Returns appropriate error response
- [ ] **Specific exception types** — Are specific exceptions logged with relevant context?
  - `HttpRequestException` → log URL, status code
  - `DbException` → log query context
  - `TimeoutException` → log what timed out and the timeout duration
  - `ValidationException` → log what failed validation
- [ ] **Fallback paths** — When using fallback/default behavior:
  - Log that the fallback was triggered and why
  - Log at Warning level (it's not normal)
- [ ] **Circuit breaker** — If using Polly or similar:
  - State changes: Closed → Open → Half-Open
  - Break reason, duration

---

## 7. Security & Authentication

- [ ] **Login attempts** — Success and failure:
  - Success: user ID, method (at Information)
  - Failure: attempted identifier, reason (at Warning)
  - Never log passwords or tokens
- [ ] **Authorization failures** — 403 responses:
  - User ID, attempted resource, required permission
  - At Warning level
- [ ] **Token events** — Token issued, refreshed, rejected, expired
  - Never log the token value itself
  - Log token type, expiry, associated user
- [ ] **Suspicious activity** — Rate limit hits, unusual patterns:
  - Multiple failed logins from same IP
  - Access to admin endpoints from non-admin users
  - At Warning or Error level
- [ ] **Data access audit** — Access to sensitive data:
  - Who accessed what (user ID, resource type/ID)
  - At Information level

---

## 8. Background Services / Workers

- [ ] **Service lifecycle** — `BackgroundService` / `IHostedService`:
  - `ExecuteAsync` started / stopped
  - Iteration count, last run time
- [ ] **Job processing** — For each job/task:
  - Job started: job ID, type, parameters
  - Job completed: duration, result summary
  - Job failed: exception, retry plan
- [ ] **Scheduling** — Cron jobs, timers:
  - Next scheduled run
  - Skipped runs (if applicable)
- [ ] **Queue processing** — Dequeue operations:
  - Queue depth at Debug level (periodically)
  - Processing rate
  - Poison messages / dead letters at Error level
- [ ] **Graceful shutdown** — On cancellation token:
  - Log remaining items in queue
  - Log drain completion

---

## 9. Performance-Sensitive Paths

- [ ] **Timing** — Operations that might be slow:
  - Wrap with `Stopwatch` and log elapsed time
  - Set Warning threshold (e.g., > 1000ms)
  ```csharp
  var sw = Stopwatch.StartNew();
  var result = await _repository.GetOrdersAsync(customerId);
  sw.Stop();
  if (sw.ElapsedMilliseconds > 500)
  {
      _logger.LogWarning("Slow query: GetOrders for {CustomerId} took {ElapsedMs}ms",
          customerId, sw.ElapsedMilliseconds);
  }
  else
  {
      _logger.LogDebug("GetOrders for {CustomerId} completed in {ElapsedMs}ms",
          customerId, sw.ElapsedMilliseconds);
  }
  ```
- [ ] **Batch sizes** — Log the size of batches being processed
- [ ] **Queue depths** — Periodically log queue depths at Debug level
- [ ] **Memory / resource pressure** — If monitoring resources:
  - Connection pool utilization
  - Thread pool queue length
  - GC pressure indicators

---

## 10. Configuration & Feature Flags

- [ ] **Configuration changes** — If config is reloadable:
  - Log when configuration is reloaded
  - Log which values changed (non-sensitive)
- [ ] **Feature flags** — When a feature flag is evaluated:
  - At Debug level: flag name, evaluated value
  - At Information level: when a flag changes state
- [ ] **Environment-specific behavior** — Log when code branches on environment:
  - "Running in {Environment} mode, feature X is {Enabled/Disabled}"

---

## 11. Dependency Injection Gaps

- [ ] **Missing ILogger injection** — Scan all service classes for constructor injection:
  - Every class registered in DI that performs business logic, data access, or external calls
    should accept `ILogger<T>` in its constructor
  - Static classes that do significant work should accept `ILogger` as a method parameter
  - Flag any service class that has `try/catch` blocks but no `ILogger` dependency
- [ ] **Logger category correctness** — Verify `ILogger<T>` uses the correct `T`:
  - `ILogger<OrderService>` in `OrderService`, NOT `ILogger<Program>` or untyped `ILogger`

---

## Scanning Strategy

When analyzing a codebase, process files in this order (highest impact first):

1. **Program.cs / Startup.cs** — Application bootstrap and middleware pipeline
2. **Exception handlers** — Global error handling, middleware exception filters
3. **Middleware** — Custom middleware classes
4. **Controllers / Endpoints** — Request entry points
5. **Services** — Business logic layer
6. **External integration classes** — HTTP clients, message handlers, etc.
7. **Repository / Data access** — Database operations
8. **Background services** — Workers, hosted services
9. **Helpers / Utilities** — Shared code
10. **Configuration** — appsettings.json, logging config
