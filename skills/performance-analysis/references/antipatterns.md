# Performance Antipatterns Reference

## Table of Contents
1. CPU & Algorithmic
2. Memory & GC
3. Database & ORM
4. I/O & Network
5. Concurrency & Threading
6. Caching
7. Serialization
8. Logging & Observability
9. Configuration & Deployment
10. Architecture

---

## 1. CPU & Algorithmic Antipatterns

- **Nested loops over large collections** — O(n²)+ where O(n log n) or O(n) with hash lookup is possible.
- **Repeated linear search** — scanning a list/array to find items instead of using a dictionary/set/index.
- **Regex compilation inside loops** — compile once, reuse. In C#: use `static readonly Regex` or `[GeneratedRegex]` (.NET 7+).
- **String concatenation in loops** — use `StringBuilder` (C#/Java), `join` (Python), or `strings.Builder` (Go).
- **Unnecessary LINQ `.ToList()` / `.ToArray()` materialization** — materializing intermediate sequences defeats lazy evaluation.
- **Repeated reflection calls** — cache `MethodInfo`/`PropertyInfo`; use compiled expressions or source generators.
- **Boxing in hot paths** — value types boxed to `object` in generic collections or interface calls.
- **Excessive exception throwing for control flow** — exceptions are expensive; use `TryParse`, `TryGetValue`, etc.
- **Sorting when only min/max needed** — use `Min()`/`Max()` or partial sort instead of full sort.
- **Recomputing invariants inside loops** — hoist invariant computations out of loop bodies.

## 2. Memory & GC Antipatterns

- **Unbounded collection growth** — `List`, `Dictionary`, cache with no eviction, event handlers never unsubscribed.
- **Large Object Heap (LOH) fragmentation** — frequent allocation of objects ≥85 KB; arrays resizing across the LOH threshold.
- **Finalizer abuse** — classes with finalizers extend GC lifetime; use `IDisposable` + `using` instead.
- **Event handler leaks** — subscribing to events without unsubscribing prevents GC of subscriber.
- **Static references to large object graphs** — pinned for application lifetime.
- **Closure captures in hot paths** — lambdas capturing outer variables allocate heap objects.
- **Unnecessary `async` state machines** — methods that `await` a single already-completed `Task` allocate a state machine for nothing. Use `ValueTask` or return `Task` directly.
- **String duplication** — interning or caching repeated strings; use `string.Create` or `Span<char>` for formatting.
- **Missing `IDisposable`** — `HttpClient`, `DbConnection`, streams not disposed → handle/socket leaks.
- **ArrayPool / MemoryPool not used** — repeated allocation of temporary byte arrays in I/O paths.

## 3. Database & ORM Antipatterns

- **N+1 queries** — lazy loading triggers one query per related entity. Use eager loading (`.Include()` in EF Core, `JOIN FETCH` in JPA).
- **SELECT *** — fetching all columns when only a subset is needed; use projections.
- **Missing indexes** — queries filtering/sorting on unindexed columns. Check execution plans.
- **Full table scans** — queries that cannot use indexes due to functions on columns, implicit conversions, or leading wildcards.
- **Unbounded result sets** — missing `TOP`/`LIMIT`; fetching millions of rows into memory.
- **Long-running transactions** — holding locks across user interactions or external calls.
- **Missing connection pooling** — creating new connections per request; default pools too small.
- **Chatty database calls** — many small queries instead of batch or bulk operations.
- **ORM over-fetching / tracking overhead** — EF Core: use `AsNoTracking()` for read-only queries.
- **Parameter sniffing issues** — SQL Server cached plans optimized for atypical parameter values.
- **Missing query parameterization** — string concatenation in SQL → plan cache pollution + SQL injection risk.
- **Deadlocks from inconsistent lock ordering** — access tables in consistent order; use `NOLOCK` / snapshot isolation where appropriate.

## 4. I/O & Network Antipatterns

- **Synchronous I/O on async-capable threads** — blocking ASP.NET request threads with `.Result` or `.Wait()`.
- **Missing buffering** — unbuffered `FileStream` reads/writes; use `BufferedStream` or adequate buffer sizes.
- **Unbatched HTTP requests** — sequential calls that could be parallelized or batched.
- **Missing response compression** — no gzip/brotli for API responses.
- **Large payload transfers** — transferring full entities when diffs or pagination suffice.
- **DNS resolution in hot paths** — cache resolved endpoints; `HttpClient` reuse handles this.
- **Missing HTTP/2 multiplexing** — HTTP/1.1 head-of-line blocking when HTTP/2 is available.
- **No retry with backoff** — transient failures cause immediate failure instead of retry with exponential backoff + jitter.
- **Socket exhaustion** — creating new `HttpClient` instances per request instead of using `IHttpClientFactory`.
- **Chatty APIs** — many small API calls instead of composite/batch endpoints.

## 5. Concurrency & Threading Antipatterns

- **Lock contention** — coarse-grained locks serializing work. Prefer `ConcurrentDictionary`, `Channel<T>`, `ReaderWriterLockSlim`.
- **Deadlocks** — nested locks in inconsistent order; `async` code calling `.Result` on ASP.NET synchronization context.
- **Thread pool starvation** — blocking calls on thread pool threads; long-running synchronous work without `Task.Run` with `TaskCreationOptions.LongRunning`.
- **Over-synchronization** — locking around already thread-safe operations.
- **Missing parallelization** — CPU-bound loops that could use `Parallel.ForEach` or PLINQ.
- **Async void** — fire-and-forget with no error handling; use `async Task`.
- **`ConfigureAwait(false)` missing in library code** — unnecessary synchronization context capture.
- **Race conditions** — check-then-act without atomicity; non-volatile reads of shared state.
- **Unbounded task creation** — spawning unlimited tasks; use `SemaphoreSlim` or `Channel<T>` for throttling.
- **Timer leaks** — `System.Timers.Timer` or `System.Threading.Timer` not disposed.

## 6. Caching Antipatterns

- **No caching of expensive computations** — repeated identical work without memoization.
- **Cache without expiration** — stale data and unbounded memory growth.
- **Cache stampede** — many threads simultaneously computing a missing cache entry. Use `Lazy<T>`, `SemaphoreSlim`, or `GetOrAdd` with a factory.
- **Over-caching** — caching data that changes frequently, causing high invalidation overhead.
- **Distributed cache misuse** — serializing large objects to Redis/memcached when in-process cache suffices.
- **Missing cache-aside pattern** — not checking cache before database; not populating cache after database read.
- **Inconsistent cache invalidation** — stale data served after writes.

## 7. Serialization Antipatterns

- **JSON serialization in hot paths without source generators** — reflection-based `System.Text.Json` or `Newtonsoft.Json` is slow. Use `JsonSerializerContext` source generators in .NET 6+.
- **Excessive serialization/deserialization** — converting objects multiple times through a pipeline.
- **Large object graph serialization** — circular references, lazy-loaded proxies serialized accidentally.
- **Missing `[JsonIgnore]`** — serializing navigation properties, computed fields, or sensitive data.
- **Not using `Span<T>` / `Utf8JsonReader`** — for high-throughput JSON parsing, avoid `string` allocations.

## 8. Logging & Observability Antipatterns

- **Excessive logging in hot paths** — string formatting and I/O on every request/iteration.
- **Missing structured logging** — string interpolation instead of message templates. Use `LoggerMessage.Define` or `[LoggerMessage]` source generators.
- **Logging sensitive data** — PII in logs.
- **Synchronous log sinks** — file/database writes blocking request threads; use async sinks (Serilog `Async` sink).
- **Missing log levels** — everything at `Information`; no `Debug`/`Trace` separation.
- **No distributed tracing** — missing correlation IDs across service boundaries.

## 9. Configuration & Deployment Antipatterns

- **Debug/diagnostic mode in production** — Entity Framework `EnableSensitiveDataLogging`, debug-level logging.
- **Missing connection string tuning** — default pool sizes, timeouts, retry counts.
- **Tiered compilation not leveraged** — .NET: ensure `TieredCompilation` is enabled (default in .NET 6+).
- **Server GC not enabled** — ASP.NET apps should use server GC (`<ServerGarbageCollection>true</ServerGarbageCollection>`).
- **Missing HTTP.sys / Kestrel tuning** — default thread counts, keep-alive timeouts, request limits.
- **No health checks or readiness probes** — can't distinguish healthy from degraded instances.
- **Missing rate limiting** — no protection against burst traffic; use `System.Threading.RateLimiting` (.NET 7+).

## 10. Architecture Antipatterns

- **Synchronous inter-service calls in a chain** — latency compounds; use async messaging or parallel fan-out.
- **Missing circuit breaker** — cascading failures from a degraded dependency; use Polly.
- **Monolithic data access** — single database bottleneck; consider CQRS, read replicas, or sharding.
- **Over-abstraction** — excessive layering adding method call depth and allocation overhead.
- **Missing backpressure** — producers overwhelming consumers; use bounded channels or queues.
- **Retry storms** — all clients retrying simultaneously after an outage; use jitter + exponential backoff.
