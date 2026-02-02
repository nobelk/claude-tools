i# Analysis Patterns Reference

Framework-specific patterns for codebase analysis. Sections are referenced from SKILL.md by `§` markers.

---

## .NET/C# Discovery

### Project Structure Indicators

| File/Pattern | Indicates |
|-------------|-----------|
| `*.sln` | Solution root — lists all projects |
| `*.csproj` | Project file — dependencies, target framework, package refs |
| `Program.cs` | Application entry point (minimal hosting or traditional) |
| `Startup.cs` | Legacy startup config (pre-.NET 6) |
| `appsettings.json` / `appsettings.*.json` | Configuration by environment |
| `launchSettings.json` | Dev environment profiles |
| `Directory.Build.props` / `Directory.Packages.props` | Central package/build management |
| `global.json` | SDK version pinning |
| `nuget.config` | Package source configuration |
| `Dockerfile` / `docker-compose.yml` | Container deployment |
| `*.dacpac` / `*.sqlproj` | SQL Server database projects |

### Framework Detection

Identify the .NET variant from `*.csproj` contents:

| Pattern in csproj | Framework |
|-------------------|-----------|
| `<Project Sdk="Microsoft.NET.Sdk.Web">` | ASP.NET Core web app |
| `<Project Sdk="Microsoft.NET.Sdk.Worker">` | Worker Service (background) |
| `<Project Sdk="Microsoft.NET.Sdk.BlazorWebAssembly">` | Blazor WASM |
| `PackageReference Include="Microsoft.AspNetCore.Components.WebAssembly"` | Blazor WASM |
| `PackageReference Include="Microsoft.EntityFrameworkCore"` | EF Core ORM |
| `PackageReference Include="MediatR"` | CQRS/Mediator pattern |
| `PackageReference Include="MassTransit"` or `NServiceBus` | Message bus |
| `PackageReference Include="Grpc.AspNetCore"` | gRPC services |
| `PackageReference Include="Microsoft.AspNetCore.SignalR"` | Real-time (SignalR) |
| `PackageReference Include="Hangfire"` or `Quartz` | Background job scheduling |
| `PackageReference Include="Swashbuckle"` or `NSwag` | OpenAPI/Swagger |
| `PackageReference Include="Serilog"` or `NLog` | Structured logging |
| `PackageReference Include="FluentValidation"` | Input validation library |
| `PackageReference Include="AutoMapper"` or `Mapster` | Object mapping |
| `PackageReference Include="Polly"` | Resilience/retry policies |
| `PackageReference Include="HealthChecks"` | Health check endpoints |
| `PackageReference Include="Dapper"` | Micro-ORM (alternative to EF) |
| `PackageReference Include="xunit"` or `NUnit` or `MSTest` | Test framework |

### Solution Architecture Patterns

Recognize common .NET solution layouts:

**Clean Architecture / Onion:**
```
src/
├── Domain/          (entities, value objects, interfaces)
├── Application/     (use cases, DTOs, CQRS handlers)
├── Infrastructure/  (EF, external services, repositories)
└── WebAPI/          (controllers, middleware, startup)
```

**Vertical Slice:**
```
src/Features/
├── Orders/
│   ├── CreateOrder.cs       (handler + request + response)
│   ├── GetOrder.cs
│   └── OrderValidator.cs
├── Products/
│   ├── CreateProduct.cs
│   └── ListProducts.cs
```

**N-Tier:**
```
src/
├── Web/             (MVC controllers, views/pages)
├── Business/        (services, logic)
├── DataAccess/      (repositories, EF context)
└── Models/          (shared DTOs/entities)
```

---

## .NET/C# Feature Detection

### API / Controller Patterns

| Pattern | Feature Type |
|---------|-------------|
| `[ApiController]` + `[Route]` on class | REST API controller |
| `[HttpGet]`, `[HttpPost]`, `[HttpPut]`, `[HttpDelete]` | CRUD endpoints |
| `[Authorize]` or `[AllowAnonymous]` | Protected/public endpoints |
| `ControllerBase` or `Controller` inheritance | API vs MVC controller |
| `IActionResult` / `ActionResult<T>` return types | Endpoint responses |
| `[FromBody]`, `[FromQuery]`, `[FromRoute]` | Parameter binding |

### MVC / Razor Pages

| Pattern | Feature Type |
|---------|-------------|
| `.cshtml` files in `Views/` | MVC views |
| `.cshtml` files in `Pages/` | Razor Pages |
| `@page` directive | Razor Page route |
| `_Layout.cshtml` | Shared layout template |
| `_ViewImports.cshtml` | Tag helper imports |
| ViewModels / PageModels | UI data binding |

### Blazor Components

| Pattern | Feature Type |
|---------|-------------|
| `.razor` files | Blazor components |
| `@code { }` blocks | Component logic |
| `[Parameter]` properties | Component inputs |
| `@inject` directives | Service injection |
| `NavigationManager` usage | Client-side routing |
| `IJSRuntime` usage | JavaScript interop |
| `AuthorizeView` component | Auth-gated UI |

### CQRS / MediatR Handlers

| Pattern | Feature Type |
|---------|-------------|
| `IRequest<T>` / `IRequest` | Command or query definition |
| `IRequestHandler<TRequest, TResponse>` | Business logic handler |
| `INotification` / `INotificationHandler` | Domain event handling |
| `IPipelineBehavior<,>` | Cross-cutting concerns (validation, logging) |

### Entity Framework Core

| Pattern | Feature Type |
|---------|-------------|
| `DbContext` subclass | Database context / unit of work |
| `DbSet<T>` properties | Entity table mappings |
| `IEntityTypeConfiguration<T>` | Fluent entity configuration |
| `Migration` files in `Migrations/` | Schema evolution history |
| `HasOne`, `HasMany`, `WithMany` | Relationship definitions |
| `.Include()` / `.ThenInclude()` | Eager loading navigation properties |
| `ValueConverter` usage | Custom type conversions |

### SignalR (Real-time)

| Pattern | Feature Type |
|---------|-------------|
| `: Hub` or `: Hub<T>` inheritance | Real-time hub |
| `Clients.All.SendAsync()` | Broadcast messaging |
| `HubConnection` in client code | Client-side real-time connection |
| `[HubMethodName]` attribute | Named hub methods |

### Background Processing

| Pattern | Feature Type |
|---------|-------------|
| `BackgroundService` / `IHostedService` | Long-running background service |
| `IJob` (Hangfire/Quartz) | Scheduled job |
| `[Queue]` attribute | Job queue assignment |
| `RecurringJob.AddOrUpdate` | Cron-scheduled recurring work |
| Channel<T> usage | In-process producer/consumer |

### Middleware and Pipeline

| Pattern | Feature Type |
|---------|-------------|
| `IMiddleware` or `app.Use()` | HTTP pipeline middleware |
| `app.UseAuthentication()` / `app.UseAuthorization()` | Auth middleware |
| `app.UseCors()` | CORS policy |
| `app.UseRateLimiter()` | Rate limiting |
| Exception handling middleware | Global error handling |
| `IExceptionHandler` (.NET 8+) | Structured exception handling |

### Dependency Injection Registration

| Pattern | Feature Type |
|---------|-------------|
| `builder.Services.AddScoped<>()` | Per-request service |
| `builder.Services.AddSingleton<>()` | Application-wide service |
| `builder.Services.AddTransient<>()` | Per-resolution service |
| `builder.Services.AddDbContext<>()` | Database context |
| `builder.Services.AddHttpClient<>()` | Named/typed HTTP client |
| Extension methods `Add*()` on `IServiceCollection` | Feature registration modules |

### Authentication & Authorization

| Pattern | Feature Type |
|---------|-------------|
| `AddAuthentication().AddJwtBearer()` | JWT token auth |
| `AddAuthentication().AddCookie()` | Cookie-based auth |
| `AddIdentity<>()` / `AddDefaultIdentity<>()` | ASP.NET Identity |
| `AddAuthorization(o => o.AddPolicy(...))` | Policy-based authorization |
| `[Authorize(Policy = "...")]` | Policy enforcement |
| `[Authorize(Roles = "...")]` | Role-based access |
| `IAuthorizationHandler` | Custom authorization logic |
| `ClaimsPrincipal` usage | Claims-based identity |

### Validation

| Pattern | Feature Type |
|---------|-------------|
| `AbstractValidator<T>` (FluentValidation) | Request/model validation |
| `DataAnnotations` (`[Required]`, `[StringLength]`, etc.) | Attribute-based validation |
| `IValidatableObject` | Self-validating models |
| `ModelState.IsValid` checks | MVC validation |
| `IPipelineBehavior` validation behavior | MediatR pipeline validation |

---

## .NET/C# Gap Detection

### Common Missing Features in ASP.NET Applications

- **Health checks**: No `/health` or `/ready` endpoints (`IHealthCheck` implementations)
- **API versioning**: No `AddApiVersioning()` or URL/header versioning
- **Rate limiting**: No `UseRateLimiter()` or throttling middleware
- **Response caching**: No `[ResponseCache]` or output caching
- **CORS policy**: No `UseCors()` or overly permissive `AllowAnyOrigin()`
- **Request logging**: No HTTP request/response logging middleware
- **API documentation**: No Swagger/OpenAPI generation
- **Global error handling**: No exception middleware, raw stack traces returned
- **Idempotency**: No idempotency keys on POST/PUT endpoints
- **Pagination**: Endpoints return unbounded collections
- **ETag / conditional requests**: No concurrency control on GET/PUT
- **Structured logging**: Using `Console.WriteLine` instead of `ILogger<T>`
- **Correlation IDs**: No request tracing across services

### Common Missing Features in EF Core

- **Audit trails**: No `CreatedAt`/`UpdatedAt`/`CreatedBy` on entities
- **Soft deletes**: No `IsDeleted` flag or query filters
- **Concurrency tokens**: No `[ConcurrencyCheck]` or `RowVersion`
- **Seeding**: No `HasData()` or seed migration
- **Index definitions**: Missing indexes on frequently queried columns

### Common Missing Features in Background Services

- **Retry logic**: No Polly policies or retry mechanisms
- **Dead letter handling**: Failed messages not captured
- **Graceful shutdown**: `StopAsync` not properly implemented
- **Health reporting**: Background service health not exposed

---

## .NET/C# Issue Detection

### Logical Issues

| Pattern | Problem |
|---------|---------|
| `async void` methods (except event handlers) | Exceptions silently swallowed, caller cannot await |
| `.Result` or `.Wait()` on Tasks | Deadlock risk in synchronous contexts |
| Missing `ConfigureAwait(false)` in library code | Potential deadlocks in non-ASP.NET hosts |
| `catch (Exception) { }` empty catch blocks | Silent failure, lost error context |
| `throw ex;` instead of `throw;` | Stack trace destroyed |
| Mutable statics shared across requests | Thread-safety violations |
| `DateTime.Now` instead of `DateTime.UtcNow` | Timezone-dependent bugs |
| String comparison without `StringComparison` | Culture-dependent behavior |
| Missing null checks on injected services | `NullReferenceException` at runtime |
| `IEnumerable<T>` multiple enumeration | Repeated database queries or side effects |

### Performance Issues

| Pattern | Problem |
|---------|---------|
| `.ToList()` before `.Where()` on `IQueryable` | Loads entire table into memory |
| Missing `.AsNoTracking()` on read-only queries | Unnecessary change tracking overhead |
| `Include()` chains loading excessive navigation data | Over-fetching related entities |
| `foreach` with individual `SaveChangesAsync()` calls | N+1 write pattern, should batch |
| `string` concatenation in loops | Allocations — use `StringBuilder` |
| `AddScoped` for stateless services that should be `Singleton` | Unnecessary per-request allocation |
| Large objects on LOH without pooling | GC pressure from `byte[]` / `string` |
| `Task.Run()` in ASP.NET request pipeline | Thread pool starvation under load |
| Synchronous I/O (`File.ReadAllText` vs `ReadAllTextAsync`) | Thread blocking under concurrency |
| Missing `CancellationToken` propagation | Cannot cancel long-running operations |
| Unbounded `Channel<T>` or `ConcurrentQueue` | Memory growth without backpressure |

### Security Issues

| Pattern | Problem |
|---------|---------|
| Raw SQL via `FromSqlRaw` with string interpolation | SQL injection |
| `[AllowAnonymous]` on sensitive endpoints | Authentication bypass |
| Secrets in `appsettings.json` committed to source | Credential exposure |
| Missing `[ValidateAntiForgeryToken]` on POST actions | CSRF vulnerability |
| `CORS AllowAnyOrigin` with `AllowCredentials` | Credential leakage to any origin |
| Missing `[Authorize]` on controllers (no global filter) | Unprotected endpoints by default |
| Logging sensitive data (`ILogger.Log(password)`) | Credential leakage in logs |
| `HttpClient` without certificate validation override check | Potential MITM if validation disabled |
| JWT token without expiration or with very long expiry | Token abuse window |
| Missing `Content-Security-Policy` headers | XSS attack surface |

### Code Quality Issues

| Pattern | Problem |
|---------|---------|
| Service classes with 10+ injected dependencies | SRP violation, class doing too much |
| Controllers with business logic (not delegating) | Fat controllers, poor testability |
| No interface for service registrations | Tight coupling, untestable |
| Mixed `async` and sync code in same method | Inconsistent execution model |
| Magic strings for config keys, routes, claim types | Brittle, error-prone |
| Commented-out code blocks | Dead code noise |
| Missing XML doc comments on public APIs | Undocumented contracts |
| `#region` blocks hiding complexity | Likely SRP violations |
| Test projects missing or empty | No verification of behavior |
| No `.editorconfig` or code style enforcement | Inconsistent formatting |

---

## General Feature Detection (Non-.NET)

### Route/Endpoint Definitions

- Express: `app.get()`, `router.post()`
- Django: `urlpatterns`, `@api_view`
- FastAPI: `@app.get()`, `@router.post()`
- Rails: `routes.rb`, `resources :items`
- Spring: `@RestController`, `@RequestMapping`
- Go: `http.HandleFunc`, `mux.Handle`

### UI Component Patterns

- React: Component files, hooks, JSX
- Vue: `.vue` files, component registration
- Angular: `@Component` decorators, modules
- Svelte: `.svelte` files

### General Gap Detection

**Web Applications:** Authentication, authorization, user management, logging, error pages, API docs, rate limiting, caching, HTTPS enforcement.

**APIs:** Versioning, pagination, filtering/sorting, input validation, consistent error responses, health checks, OpenAPI docs, request throttling.

**Data Applications:** Backup mechanisms, data export, audit trails, validation, migration scripts, archival strategy.

### General Issue Detection

**Logical:** Unchecked null access, missing error handling in async code, incorrect loop bounds, race conditions.

**Performance:** N+1 queries, missing indexes, unbounded fetches, sync-over-async, memory leaks.

**Security:** Injection vectors, XSS, missing CSRF protection, hardcoded secrets, insecure direct object references.

**Quality:** Dead code, duplication, high cyclomatic complexity, missing types, inconsistent naming.
