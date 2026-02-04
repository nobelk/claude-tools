# Refactoring Checklist — C#/.NET

## Table of Contents
1. [SOLID Principles](#solid-principles)
2. [Dependency Decoupling](#dependency-decoupling)
3. [Logging Standards](#logging-standards)
4. [Clean Code Practices](#clean-code-practices)
5. [Error Handling](#error-handling)
6. [Async/Await Hygiene](#asyncawait-hygiene)

---

## SOLID Principles

### Single Responsibility (SRP)
- [ ] Each class has one reason to change.
- [ ] No class mixes I/O, business logic, and presentation concerns.
- [ ] Services are named after the behavior they own (e.g., `OrderPricingService`, not `OrderHelper`).

### Open/Closed (OCP)
- [ ] New behavior is added by adding classes, not modifying existing ones.
- [ ] Strategy/Factory patterns replace `switch` blocks that grow with each new case.

### Liskov Substitution (LSP)
- [ ] Derived classes honor the contract of their base class or interface.
- [ ] No `NotImplementedException` in interface implementations (indicates bad abstraction).

### Interface Segregation (ISP)
- [ ] No interface has >5 methods (split if larger).
- [ ] Consumers depend only on the methods they use.
- [ ] No "fat" interfaces force implementers to stub out unused methods.

### Dependency Inversion (DIP)
- [ ] High-level modules depend on abstractions, not concretions.
- [ ] All infrastructure concerns (DB, file system, HTTP, clock) are behind interfaces.
- [ ] `Program.cs` / `Startup.cs` is the only place concrete types are registered.

---

## Dependency Decoupling

### Constructor Injection
- [ ] All dependencies are injected via constructor parameters.
- [ ] No `new SomeService()` inside business logic classes.
- [ ] Constructor parameter count ≤ 4 (if more, extract a Facade or split the class).

### Interface Extraction
- [ ] Every service consumed by another class has an interface.
- [ ] Interfaces live in a contracts/abstractions project or namespace, not alongside implementations.
- [ ] Interface names describe capability, not implementation (`INotificationSender`, not `IEmailService` if SMS is also supported).

### Remove Static Coupling
- [ ] Static classes with state are replaced with injectable services.
- [ ] `DateTime.Now` and `DateTime.UtcNow` → inject `TimeProvider` (or `ISystemClock`).
- [ ] `File.ReadAllText` → inject `IFileSystem` (or wrap in a service).
- [ ] `HttpClient` → inject via `IHttpClientFactory`.

### Remove Service Locator
- [ ] No calls to `IServiceProvider.GetService<T>()` outside of composition root or factory classes.
- [ ] No ambient context patterns (`SomeContext.Current`).

---

## Logging Standards

### Framework
- [ ] Use `Microsoft.Extensions.Logging.ILogger<T>` as the primary abstraction.
- [ ] If Serilog is in use, configure it as a provider behind `ILogger<T>`.
- [ ] Remove all `Console.WriteLine`, `Debug.WriteLine`, `Trace.WriteLine` from production code.

### Structured Logging
- [ ] Use message templates with named parameters, not string interpolation.

```csharp
// WRONG
_logger.LogInformation($"Order {order.Id} processed for {order.CustomerId}");

// RIGHT
_logger.LogInformation("Order {OrderId} processed for {CustomerId}", order.Id, order.CustomerId);
```

### Log Levels
- [ ] `Trace` — fine-grained diagnostic events (disabled in production).
- [ ] `Debug` — internal state useful during development.
- [ ] `Information` — significant business events (order placed, user registered).
- [ ] `Warning` — unexpected but recoverable situations (retry triggered, fallback used).
- [ ] `Error` — operation failed but application continues (failed payment, timeout).
- [ ] `Critical` — application-wide failure (database unreachable, out of memory).

### Contextual Enrichment
- [ ] Use scopes to attach correlation IDs: `using (_logger.BeginScope(new { CorrelationId = correlationId }))`.
- [ ] Include operation context: who, what, which entity, outcome.
- [ ] Avoid logging sensitive data (PII, tokens, passwords).

### Performance
- [ ] Use `LoggerMessage.Define` source generators or high-performance logging for hot paths.
- [ ] Guard expensive log argument computation: `if (_logger.IsEnabled(LogLevel.Debug))`.

---

## Clean Code Practices

### Naming
- [ ] Classes: `PascalCase` nouns (`OrderProcessor`, not `ProcessOrders`).
- [ ] Methods: `PascalCase` verbs (`CalculateTotal`, not `Total`).
- [ ] Private fields: `_camelCase` with underscore prefix.
- [ ] No abbreviations unless universally understood (`Id`, `Url`, `Http` are fine; `Mgr`, `Svc`, `Proc` are not).
- [ ] Boolean names start with `is`, `has`, `can`, `should`.

### Method Design
- [ ] Methods ≤ 30 lines (extract helper methods if longer).
- [ ] Parameter count ≤ 3 (use a parameter object or builder if more).
- [ ] No flag arguments (boolean parameters that switch behavior) — split into two methods.
- [ ] Guard clauses at the top, happy path follows.
- [ ] Single level of abstraction per method — don't mix high-level orchestration with low-level details.

### Class Design
- [ ] Classes ≤ 300 lines (extract collaborators if larger).
- [ ] One public class per file, filename matches class name.
- [ ] Favor composition over inheritance — prefer injecting collaborators over deep class hierarchies.
- [ ] Mark classes `sealed` by default; only unseal when inheritance is intentional.

### Null Safety
- [ ] Enable `<Nullable>enable</Nullable>` in `.csproj`.
- [ ] Use null-conditional (`?.`) and null-coalescing (`??`) operators.
- [ ] Prefer `ArgumentNullException.ThrowIfNull()` (.NET 7+) for guard clauses.
- [ ] Avoid returning `null` from methods — use `Result<T>`, empty collections, or `Nullable<T>`.

### Code Organization
- [ ] Namespaces mirror folder structure.
- [ ] Remove all unused `using` directives.
- [ ] Apply `global using` for common namespaces (System, System.Collections.Generic, etc.).
- [ ] Group file-scoped namespace declarations (C# 10+).

---

## Error Handling

- [ ] Never catch `Exception` unless re-throwing or at the top-level boundary.
- [ ] Catch specific exception types.
- [ ] Always include the original exception as an inner exception when wrapping.
- [ ] Log and throw — never log and swallow silently (unless explicitly documented why).
- [ ] Use exception filters (`catch (HttpRequestException ex) when (ex.StatusCode == 429)`) for precision.
- [ ] Use the Result pattern for expected business failures.
- [ ] Centralize unhandled exception handling in middleware (ASP.NET) or `AppDomain.UnhandledException`.

---

## Async/Await Hygiene

- [ ] Async methods end with `Async` suffix.
- [ ] Never use `.Result` or `.Wait()` on tasks — use `await` throughout.
- [ ] Use `ConfigureAwait(false)` in library code (not in ASP.NET controllers/services).
- [ ] Use `ValueTask<T>` for hot paths that often complete synchronously.
- [ ] Pass `CancellationToken` through the entire async call chain.
- [ ] Avoid `async void` — only acceptable for event handlers.
