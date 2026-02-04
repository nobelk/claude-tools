# C#/.NET Design Patterns — When and How to Apply

## Table of Contents
1. [Creational Patterns](#creational-patterns)
2. [Structural Patterns](#structural-patterns)
3. [Behavioral Patterns](#behavioral-patterns)
4. [.NET-Specific Patterns](#net-specific-patterns)
5. [Anti-Pattern Recognition](#anti-pattern-recognition)

---

## Creational Patterns

### Factory Method
**When to apply:** Multiple `if/switch` blocks decide which concrete type to instantiate.
**C# signal:** `new ConcreteType()` scattered across business logic.

```csharp
// BEFORE
public INotification CreateNotification(string type)
{
    if (type == "email") return new EmailNotification();
    if (type == "sms") return new SmsNotification();
    throw new ArgumentException($"Unknown type: {type}");
}

// AFTER
public interface INotificationFactory
{
    INotification Create(string type);
}
```

### Builder
**When to apply:** Constructors with >4 parameters, or multi-step object construction.
**C# signal:** Telescoping constructors, large object initializer blocks.

```csharp
// BEFORE
var report = new Report(title, author, DateTime.Now, format, true, null, theme);

// AFTER
var report = new ReportBuilder()
    .WithTitle(title)
    .ByAuthor(author)
    .InFormat(format)
    .Build();
```

### Singleton → Scoped/Transient DI
**When to apply:** Static classes or manual singleton implementations.
**C# signal:** `private static readonly instance`, `static` utility classes with state.
**Preferred .NET approach:** Register in DI container as `AddSingleton<T>`, `AddScoped<T>`, or `AddTransient<T>` — avoid hand-rolled singletons.

---

## Structural Patterns

### Adapter
**When to apply:** Integrating third-party libraries or legacy code with incompatible interfaces.
**C# signal:** Wrapper classes that translate between two interfaces.

```csharp
public interface IPaymentProcessor { Task<PaymentResult> ProcessAsync(PaymentRequest request); }

// Adapter wraps the third-party SDK
public class StripePaymentAdapter : IPaymentProcessor
{
    private readonly StripeClient _client;
    public async Task<PaymentResult> ProcessAsync(PaymentRequest request)
    {
        var stripeCharge = await _client.ChargeAsync(/* map fields */);
        return new PaymentResult { Success = stripeCharge.Paid };
    }
}
```

### Decorator
**When to apply:** Adding cross-cutting behavior (caching, logging, retry) without modifying the original class.
**C# signal:** Repeated boilerplate wrapping method calls.

```csharp
// Logging decorator for any repository
public class LoggingRepository<T> : IRepository<T>
{
    private readonly IRepository<T> _inner;
    private readonly ILogger _logger;

    public async Task<T?> GetByIdAsync(int id)
    {
        _logger.LogInformation("Fetching {Entity} with ID {Id}", typeof(T).Name, id);
        return await _inner.GetByIdAsync(id);
    }
}
```

### Facade
**When to apply:** Client code interacts with many subsystem classes to complete one operation.
**C# signal:** Controller or service methods with 5+ injected dependencies all called sequentially.

---

## Behavioral Patterns

### Strategy
**When to apply:** Algorithms or business rules vary by context and are selected at runtime.
**C# signal:** Large `switch` statements on enum or string that execute different logic branches.

```csharp
// BEFORE — switch in service
public decimal CalculateDiscount(Order order)
{
    switch (order.CustomerTier)
    {
        case "Gold": return order.Total * 0.2m;
        case "Silver": return order.Total * 0.1m;
        default: return 0;
    }
}

// AFTER — strategy pattern
public interface IDiscountStrategy { decimal Calculate(Order order); }

public class GoldDiscount : IDiscountStrategy
{
    public decimal Calculate(Order order) => order.Total * 0.2m;
}
```

### Mediator (MediatR)
**When to apply:** Controllers or services are bloated with orchestration logic; many classes depend on each other.
**C# signal:** A controller injects 5+ services. Services call each other in chains.
**.NET approach:** Use MediatR with `IRequest<T>` / `IRequestHandler<T>` to decouple command/query dispatch from handling.

### Observer / Event-Driven
**When to apply:** One action triggers side effects in multiple subsystems (email, audit log, cache invalidation).
**C# signal:** A method explicitly calls 3+ unrelated services after completing its main work.
**.NET approach:** Use `INotification` / `INotificationHandler` (MediatR) or domain events.

### Chain of Responsibility
**When to apply:** A request passes through a pipeline of processing steps (validation, enrichment, authorization).
**C# signal:** Sequential `if` blocks that each check and transform data.
**.NET approach:** ASP.NET middleware pipeline is a built-in chain of responsibility.

---

## .NET-Specific Patterns

### Options Pattern
**When to apply:** Configuration values are read directly from `IConfiguration` throughout the codebase.
**Replace with:** `IOptions<T>` / `IOptionsSnapshot<T>` with strongly-typed settings classes.

### Repository + Unit of Work
**When to apply:** EF Core `DbContext` is injected directly into controllers or thick service classes.
**Note:** Only introduce if the codebase genuinely needs to abstract persistence (e.g., for testability or multi-ORM support). For simple CRUD apps, `DbContext` alone is often sufficient — avoid unnecessary abstraction.

### Result Pattern
**When to apply:** Methods throw exceptions for expected business failures (e.g., validation errors, not-found).
**Replace with:** A `Result<T>` type that encodes success/failure without exceptions.

```csharp
public class Result<T>
{
    public bool IsSuccess { get; private init; }
    public T? Value { get; private init; }
    public string? Error { get; private init; }

    public static Result<T> Success(T value) => new() { IsSuccess = true, Value = value };
    public static Result<T> Failure(string error) => new() { IsSuccess = false, Error = error };
}
```

---

## Anti-Pattern Recognition

| Smell | Likely Pattern Fix |
|---|---|
| God class (>500 lines, 10+ dependencies) | Extract services, apply Facade or Mediator |
| `new ConcreteService()` in business logic | Introduce DI + interface |
| Massive `switch`/`if-else` on type | Strategy or Factory Method |
| Repeated try/catch/log/rethrow | Decorator or middleware |
| Static helper classes with state | Convert to injectable service |
| Configuration strings scattered in code | Options pattern |
| Throwing exceptions for control flow | Result pattern |
| Circular project references | Extract shared interfaces into a contracts assembly |
