i# Review Checklist

Evaluate each changed file against every applicable category below. Not all categories apply to every file — use judgment. Focus on the diff, not pre-existing code.

## 1. Correctness & Logic

- **Control flow**: Are all branches reachable? Any unreachable code after early returns?
- **Boundary conditions**: Off-by-one in loops, array indexing, pagination, string slicing.
- **Null / empty handling**: Could any variable be null, undefined, empty, or zero where not expected?
- **Type safety**: Implicit coercions, wrong types passed across boundaries, missing type guards.
- **State transitions**: Are state machines / enums handled exhaustively (e.g., switch default)?
- **Arithmetic**: Integer overflow, floating-point precision, division by zero.
- **String handling**: Encoding issues, locale-sensitive comparisons, unterminated strings.
- **Boolean logic**: De Morgan violations, short-circuit side effects, inverted conditions.
- **Comparison semantics**: `==` vs `===`, object identity vs equality, NaN comparisons.

## 2. Security (OWASP-aligned)

- **Injection**: SQL, NoSQL, OS command, LDAP, XPath, template injection. Is user input parameterized / escaped before reaching interpreters?
- **Broken auth**: Credential exposure, missing rate limiting on auth endpoints, session fixation.
- **Broken access control**: Missing authorization checks, IDOR, privilege escalation, CORS misconfig.
- **Sensitive data exposure**: PII/secrets in logs, error messages, URLs, or client-side code.
- **Hardcoded secrets**: API keys, tokens, passwords, connection strings in source.
- **XSS**: Unescaped user content rendered in HTML/JS. CSP headers present?
- **CSRF**: State-changing requests without CSRF tokens.
- **Deserialization**: Untrusted data deserialized without validation (pickle, Java serialization, YAML `load`).
- **Dependency risk**: New or upgraded dependencies — check for known CVEs, suspicious packages, excessive permissions.
- **Cryptography**: Rolling custom crypto, weak algorithms (MD5/SHA1 for security), hardcoded IVs/salts.
- **Input validation**: Size limits, type checks, allow-lists vs deny-lists at trust boundaries.

## 3. Design & Architecture

- **Consistency**: Does the change follow existing patterns in the codebase (naming, structure, abstractions)?
- **Abstraction level**: Right level of indirection — not too abstract (enterprise astronaut), not too concrete (copy-paste)?
- **Single Responsibility**: Does each class/function/module do one thing well?
- **Open/Closed**: Can the design be extended without modifying existing code?
- **Dependency Inversion**: Are high-level modules depending on abstractions, not concretions?
- **Coupling**: Are modules loosely coupled? Would a change here ripple across the codebase?
- **Cohesion**: Are related things grouped together? Unrelated things separated?
- **Code duplication**: Repeated logic that should be extracted into a shared function/module.
- **Magic values**: Unexplained literal numbers, strings, or booleans — should these be named constants?
- **Naming**: Do names accurately describe intent? Are they consistent with the domain language?

## 4. Error Handling & Resilience

- **Fail modes**: What happens when the happy path fails? Is the failure mode safe (fail-closed, not fail-open)?
- **Error propagation**: Are errors swallowed silently? Caught too broadly (`catch (Exception)`)? Rethrown with context?
- **Resource cleanup**: Are files, connections, locks, transactions properly closed/released in all paths (including error paths)? Use of try-finally / `defer` / `using` / context managers.
- **Retry logic**: Are retries idempotent? Is there exponential backoff? Is there a max retry limit?
- **Timeouts**: Do network calls, DB queries, and external API calls have timeouts configured?
- **Graceful degradation**: If a non-critical dependency fails, does the system still serve its primary function?
- **Error messages**: Informative for debugging, but no leaking of internals (stack traces, SQL, file paths) to end users.

## 5. Performance & Scalability

- **N+1 queries**: Querying inside a loop — should use batch fetching or joins.
- **Unbounded operations**: Loops, queries, or collections without size limits. Could an attacker or organic growth cause OOM/timeout?
- **Missing indexes**: New query patterns without supporting DB indexes.
- **Expensive operations in hot paths**: Regex compilation, JSON serialization, reflection in tight loops.
- **Caching**: Is cacheable data being fetched repeatedly? Is cache invalidation correct?
- **Pagination**: Are list endpoints paginated? Are large result sets streamed?
- **Memory**: Large objects held longer than necessary, accidental closures capturing large scopes, missing pooling.
- **Algorithmic complexity**: O(n²) where O(n log n) or O(n) is achievable.
- **Database**: Full table scans, missing `LIMIT`, `SELECT *` when only a few columns are needed, large transactions holding locks.

## 6. Concurrency & Thread Safety

- **Shared mutable state**: Variables accessed from multiple threads/goroutines/coroutines without synchronization.
- **Race conditions**: TOCTOU (time-of-check-time-of-use), read-modify-write without atomicity.
- **Deadlocks**: Lock ordering inconsistencies, nested locks.
- **Async correctness**: Missing `await`, unhandled promise rejections, callback ordering assumptions.
- **Atomic operations**: Counter increments, flag checks that should be atomic.
- **Thread-local assumptions**: Code that assumes single-threaded execution but may run concurrently.

## 7. Testing

- **Coverage of new code**: Every new public function/method should have at least one test.
- **Happy path + error paths**: Tests for both success and failure scenarios.
- **Edge cases**: Empty inputs, boundary values, null, large inputs, Unicode, concurrent access.
- **Assertion quality**: Tests asserting specific outcomes, not just "didn't throw." Asserting behavior, not implementation.
- **Test isolation**: Tests should not depend on execution order, shared mutable state, or external services.
- **Anti-patterns**: Sleeping for timing, testing private internals, brittle selectors, overly broad mocks that hide real bugs.
- **Test naming**: Descriptive names following a consistent convention (e.g., `should_[behavior]_when_[condition]`).
- **Integration tests**: If the change involves cross-service or cross-layer interactions, are there integration tests?
- **Regression tests**: If fixing a bug, is there a test that reproduces the original bug?

## 8. API & Contract

- **Backward compatibility**: Will existing clients break? Are field removals or type changes guarded by versioning?
- **Request/response validation**: Are new API fields validated? Are defaults sensible?
- **HTTP semantics**: Correct status codes, idempotent methods for GET/PUT/DELETE, proper use of PATCH.
- **Pagination & filtering**: Large collections must be paginated. Filter parameters validated.
- **Rate limiting**: New endpoints exposed to the public should have rate limits.
- **Deprecation**: Are deprecated fields/endpoints marked and documented with a migration path?
- **Error format**: API errors follow the project's standard error schema.

## 9. Data Integrity

- **Migrations**: Are schema migrations reversible? Will they lock tables on large datasets? Are they backward-compatible with the current running code (important for zero-downtime deploys)?
- **Transactions**: Are multi-step writes wrapped in transactions where atomicity is needed?
- **Idempotency**: Can the operation be safely retried? Are idempotency keys used for external API calls?
- **Consistency**: Are related data updates atomic? Could partial failure leave data in an inconsistent state?
- **Validation at persistence layer**: Are constraints enforced at the DB level (NOT NULL, UNIQUE, FK), not just in application code?
- **Data deletion**: Soft vs hard delete — is the choice intentional? Are cascading deletes safe?

## 10. Observability

- **Logging**: Are new code paths logged at appropriate levels? Structured logging preferred. No sensitive data in logs.
- **Metrics**: Are key operations instrumented (latency, error rate, throughput)?
- **Tracing**: Are distributed trace IDs propagated through new service calls?
- **Alerting**: Do new failure modes have corresponding alerts or at least logged error codes that can be alerted on?
- **Health checks**: If adding new dependencies, are they covered by health checks?
- **Debug-ability**: In an incident, would an on-call engineer be able to diagnose issues from the logs and metrics this code produces?

## 11. Configuration & Environment

- **Env-specific behavior**: Are environment differences (dev/staging/prod) handled through configuration, not conditionals in code?
- **Feature flags**: Should the new behavior be gated behind a feature flag for safe rollout?
- **Secrets management**: Secrets loaded from a vault or environment, not hardcoded or committed.
- **Default values**: Are defaults safe and sensible? Would a missing config value cause a crash or silent misbehavior?
- **Config validation**: Is configuration validated at startup, failing fast on invalid values?

## 12. Documentation

- **Complex logic**: Non-obvious algorithms or business rules should have inline comments explaining *why*, not *what*.
- **Public API docs**: New or changed API endpoints, functions, or classes should have updated docstrings/comments.
- **README**: If the change affects setup, usage, or architecture, is the README updated?
- **Breaking changes**: Are breaking changes documented in the PR description and changelog?
- **Decision rationale**: For significant design decisions, is the reasoning recorded (PR description, ADR, or inline)?
