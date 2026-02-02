---
name: codebase-review
description: Perform a senior software engineer-level codebase review that produces a prioritized, actionable to_do.md of bug fixes and improvements. Use when a user asks to review, audit, or analyze a codebase for bugs, code quality issues, missing tests, TODOs, technical debt, or general cleanup. Also triggers on requests like "what's wrong with this code", "find bugs", "audit this project", "improve code quality", or "generate a TODO list from the code".
---

# Codebase Review

Perform a thorough codebase review as a senior software engineer and produce a prioritized `to_do.md` listing all bug fixes, improvements, and action items.

## Workflow

### 1. Discover the Codebase

Understand the project structure before reviewing individual files:

1. List the top-level directory (`view` the project root).
2. Identify the language(s), framework(s), and build system from config files (e.g., `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`).
3. Locate entry points, core modules, test directories, and config files.
4. Read any existing README, CONTRIBUTING, or architecture docs briefly for context.

**C#/.NET discovery hints:** Look for `.sln`, `.csproj`, `global.json`, `Directory.Build.props`, `Directory.Packages.props`, `nuget.config`, `appsettings.json`, `appsettings.*.json`, `launchSettings.json`, and `Program.cs` / `Startup.cs`. Check the `<TargetFramework>` in `.csproj` files to identify the .NET version. Note whether the project uses Minimal APIs vs controller-based routing, and whether it is a Web API, Blazor, Worker Service, or class library.

### 2. Systematic File Review

Read every meaningful source file. For each file, evaluate all categories below.

**Code Issues**
- Syntax errors, typos, dead code, unused imports/variables
- Poor naming, inconsistent style, overly complex functions
- Missing or incorrect type annotations
- Hard-coded values that should be configurable
- Code duplication that should be refactored
- _C#/.NET:_ `async void` methods (must be `async Task` except event handlers)
- _C#/.NET:_ `throw ex` instead of `throw` (destroys original stack trace)
- _C#/.NET:_ Classes not marked `sealed` when not designed for inheritance
- _C#/.NET:_ Using `DateTime.Now` instead of `DateTime.UtcNow` or `DateTimeOffset`
- _C#/.NET:_ Inconsistent `var` usage; missing use of target-typed `new()` or collection expressions (C# 12+)
- _C#/.NET:_ Not leveraging pattern matching, `is`, `switch` expressions where they simplify logic

**Logical Bugs**
- Off-by-one errors, incorrect boundary conditions
- Race conditions, concurrency issues
- Null/undefined reference risks
- Incorrect operator precedence or boolean logic
- Broken control flow (unreachable code, missing break/return)
- _C#/.NET:_ Missing `CancellationToken` propagation through async call chains
- _C#/.NET:_ Deadlocks from `.Result` or `.Wait()` on tasks in sync-over-async patterns
- _C#/.NET:_ Incorrect DI lifetime causing captive dependencies (e.g., Scoped service injected into Singleton)
- _C#/.NET:_ EF Core N+1 queries (missing `.Include()` / `.ThenInclude()`)
- _C#/.NET:_ EF Core unbounded queries missing `.Take()` or pagination
- _C#/.NET:_ Modifying a collection while enumerating it

**Error Handling & Fault Tolerance**
- Missing try/catch or error propagation
- Swallowed exceptions (empty catch blocks)
- Missing input validation or sanitization
- Missing timeout/retry logic for network or I/O calls
- Lack of graceful degradation
- _C#/.NET:_ Catching bare `Exception` instead of specific exception types
- _C#/.NET:_ Missing global exception handling middleware (`UseExceptionHandler` / `IExceptionHandler`)
- _C#/.NET:_ Missing `[Required]`, `FluentValidation`, or `MinimalApis.Validation` for model/request validation
- _C#/.NET:_ Missing `Polly` or equivalent retry/circuit-breaker policies on `HttpClient` calls
- _C#/.NET:_ Not using `IHttpClientFactory` (socket exhaustion and DNS issues with raw `HttpClient`)

**Security Concerns**
- SQL injection, XSS, or command injection vectors
- Hard-coded secrets, credentials, or API keys
- Insecure defaults (e.g., disabled TLS, permissive CORS)
- Missing authentication or authorization checks
- _C#/.NET:_ Connection strings or secrets in `appsettings.json` committed to source (should use User Secrets, environment variables, or Azure Key Vault)
- _C#/.NET:_ Missing `[Authorize]` or policy-based authorization on controllers/endpoints
- _C#/.NET:_ Missing anti-forgery token validation (`[ValidateAntiForgeryToken]`) on state-changing endpoints
- _C#/.NET:_ Overly permissive CORS policy (e.g., `AllowAnyOrigin().AllowCredentials()`)
- _C#/.NET:_ Missing security headers middleware (CSP, HSTS, X-Content-Type-Options)
- _C#/.NET:_ Raw SQL via `FromSqlRaw` with string interpolation instead of `FromSqlInterpolated` or parameterized queries

**Test Coverage Gaps**
- Untested public functions or critical paths
- Missing edge case tests (empty input, large input, nulls)
- Missing integration or end-to-end tests
- Tests that exist but are incomplete or have weak assertions
- _C#/.NET:_ Missing `WebApplicationFactory<T>` integration tests for API endpoints
- _C#/.NET:_ Not using `IServiceCollection` test doubles; manually newing up classes with deep dependency trees
- _C#/.NET:_ Missing EF Core in-memory or SQLite test fixtures for data-access layer
- _C#/.NET:_ No tests for DI registration (verifying all services resolve without error)
- _C#/.NET:_ Missing `IOptions<T>` / configuration binding tests

**Missing Implementations**
- TODO/FIXME/HACK/XXX comments left in source
- Stub functions or placeholder logic
- Incomplete features indicated by surrounding code
- Missing API endpoints, routes, or handlers implied by the codebase
- _C#/.NET:_ `NotImplementedException` left in method bodies
- _C#/.NET:_ Missing `IDisposable` / `IAsyncDisposable` implementation on classes holding unmanaged resources or disposable fields
- _C#/.NET:_ Missing health check endpoints (`/health`, `/ready`) for hosted services or APIs
- _C#/.NET:_ Missing `IOptions<T>` / `IOptionsSnapshot<T>` configuration classes for raw `Configuration["key"]` access

**Performance & Scalability**
- O(n²) or worse algorithms where better alternatives exist
- Missing caching, pagination, or batching
- Memory leaks (unclosed resources, event listener buildup)
- Unnecessary synchronous blocking operations
- _C#/.NET:_ `Task.Run` inside ASP.NET request pipeline (thread pool starvation risk)
- _C#/.NET:_ LINQ `.ToList()` / `.ToArray()` when `IEnumerable` enumeration suffices
- _C#/.NET:_ String concatenation in loops instead of `StringBuilder` or `string.Join`
- _C#/.NET:_ Missing `AsNoTracking()` on read-only EF Core queries
- _C#/.NET:_ Large object allocations in hot paths — consider `Span<T>`, `ArrayPool<T>`, `stackalloc`
- _C#/.NET:_ Not using `ValueTask<T>` for frequently synchronous-completing async methods
- _C#/.NET:_ Missing `ConfigureAwait(false)` in library code (non-ASP.NET contexts)
- _C#/.NET:_ EF Core lazy loading pulling data in loops without batching

**Documentation & Maintainability**
- Missing or outdated docstrings on public APIs
- Confusing code that needs explanatory comments
- Missing or outdated README / setup instructions
- _C#/.NET:_ Missing XML doc comments (`<summary>`, `<param>`, `<returns>`) on public types and members
- _C#/.NET:_ Missing or outdated `README` with `dotnet run` / `dotnet test` instructions and prerequisite .NET SDK version

**Project & Build Configuration (C#/.NET specific)**
- Nullable reference types not enabled (`<Nullable>enable</Nullable>`) in `.csproj`
- `<TreatWarningsAsErrors>` not set to `true`
- Missing `<ImplicitUsings>enable</ImplicitUsings>` (for .NET 6+)
- Outdated `<TargetFramework>` (e.g., targeting `net6.0` when `net8.0` or `net9.0` is current LTS)
- Missing `Directory.Build.props` for shared analyzer/build settings across multi-project solutions
- Missing `.editorconfig` for consistent code style enforcement
- Missing or outdated NuGet package versions with known vulnerabilities
- Missing `<InvariantGlobalization>` setting when globalization is not needed (trimming/AOT scenarios)
- Analyzer packages not referenced (`Microsoft.CodeAnalysis.NetAnalyzers`, `SonarAnalyzer.CSharp`, `Roslynator`)

### 3. Write to_do.md

Produce the file at the project root (or `/home/claude/to_do.md` if no project root is clear). Use this structure:

```markdown
# Codebase Review — TODO

> Auto-generated codebase review by Claude.
> Reviewed on: [date]

## Summary

[2-3 sentence overview: languages, framework, overall health, biggest risk areas]

## Critical — Bug Fixes

| # | File | Line(s) | Issue | Suggested Fix |
|---|------|---------|-------|---------------|
| 1 | ... | ... | ... | ... |

## High — Security & Fault Tolerance

| # | File | Line(s) | Issue | Suggested Fix |
|---|------|---------|-------|---------------|

## Medium — Code Quality & Refactoring

| # | File | Line(s) | Issue | Suggested Fix |
|---|------|---------|-------|---------------|

## Low — Style, Docs & Cleanup

| # | File | Line(s) | Issue | Suggested Fix |
|---|------|---------|-------|---------------|

## Test Coverage Gaps

| # | File / Area | What's Missing |
|---|-------------|----------------|

## Missing Implementations

| # | File | Line(s) | Description |
|---|------|---------|-------------|
```

**For C#/.NET projects, also include this section:**

```markdown
## .NET Project Health

| Area | Status | Action Needed |
|------|--------|---------------|
| Target Framework | e.g. net8.0 ✅ | — |
| Nullable Reference Types | enabled/disabled | Enable if disabled |
| TreatWarningsAsErrors | true/false | Set to true |
| Analyzers | present/missing | Add recommended analyzers |
| Health Checks | present/missing | Add /health endpoint |
| Structured Logging | present/missing | Adopt Serilog/OpenTelemetry |
| Secret Management | user-secrets/KeyVault/hardcoded | Migrate hardcoded secrets |
```

**Prioritization rules:**
- **Critical**: Logical bugs, data corruption/loss risks, crashes
- **High**: Security vulnerabilities, missing error handling on critical paths
- **Medium**: Code duplication, poor structure, missing validation on non-critical paths
- **Low**: Style issues, naming, documentation gaps

### 4. Self-Review Pass (mandatory)

After writing `to_do.md`, re-read the entire file and perform these checks:

1. **Accuracy** — Re-examine each reported file/line reference. Remove or correct any item where the file doesn't exist, the line number is wrong, or the described issue doesn't match what the code actually does.
2. **False positives** — Remove items that are actually correct code or intentional design choices.
3. **Duplicates** — Merge items that describe the same underlying issue in different words.
4. **Actionability** — Every item must have a concrete suggested fix. Vague items like "improve this" must be made specific or removed.
5. **Completeness** — Verify no major file was skipped during the review.
6. **Priority accuracy** — Verify each item is in the right severity bucket.

Apply all corrections in-place, then save the final version.

## Guidelines

- Be specific: always include file paths and line numbers where possible.
- Be objective: distinguish between definite bugs and subjective style preferences.
- Be practical: suggest the simplest fix that resolves each issue.
- Do not flag issues in generated files, lock files, or vendored dependencies.
- If the codebase is very large, prioritize core application code over configuration, build scripts, and boilerplate.
- When in doubt whether something is a bug, include it as "Medium" with a note that it may be intentional.

### C#/.NET-Specific Guidelines

- Skip auto-generated files: `*.Designer.cs`, `*.g.cs`, `obj/`, `bin/`, and EF migration files (flag migrations only if they contain obvious data-loss operations like `DropTable` without safeguards).
- Check `Program.cs` / `Startup.cs` middleware order — the order of `app.Use*()` calls matters (e.g., `UseAuthentication` must precede `UseAuthorization`).
- Verify DI registrations match usage: a service registered as `Transient` that holds state is a bug; a `Scoped` service injected into a `Singleton` is a captive dependency bug.
- Flag any `public` on types or members that should be `internal` — default to minimal visibility.
- For ASP.NET APIs, verify consistent use of `ActionResult<T>` or `Results<T1, T2>` (Minimal APIs) with proper HTTP status codes, not just returning bare objects.
- For EF Core, verify that `DbContext` is registered as `Scoped` (default) and never captured in a `Singleton`.
- Note where `async`/`await` is used but the method lacks a `CancellationToken` parameter — this should be flagged as Medium.
