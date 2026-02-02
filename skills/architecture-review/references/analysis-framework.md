i# Analysis Framework

Comprehensive checklists for evaluating architecture, design, and code quality. Record file path and evidence for each finding.

## Table of Contents
1. [Architectural Style Identification](#1-architectural-style-identification)
2. [Design Pattern Detection](#2-design-pattern-detection)
3. [Clean Code & Principles Assessment](#3-clean-code--principles-assessment)
4. [Quality Attribute Evaluation](#4-quality-attribute-evaluation)
5. [Anti-Pattern Detection](#5-anti-pattern-detection)
6. [Cross-Cutting Concerns](#6-cross-cutting-concerns)
7. [Dependency & Coupling Analysis](#7-dependency--coupling-analysis)

---

## 1. Architectural Style Identification

Identify the primary and secondary architectural styles in use:

| Style | Key Indicators |
|---|---|
| Layered / N-Tier | Distinct presentation, business, persistence layers; layer-to-layer calls only |
| Clean / Hexagonal / Onion | Domain core with no outward dependencies; ports and adapters; use cases as application boundary |
| Microservices | Independent deployable services; separate data stores; inter-service communication (REST, gRPC, messaging) |
| Monolith | Single deployable unit; shared database; in-process function calls |
| Modular Monolith | Single deployable but clear module boundaries; internal APIs between modules |
| Event-Driven / EDA | Event bus/broker; publish-subscribe; event sourcing; CQRS |
| Serverless | Function-as-a-service handlers; cloud-native event triggers; stateless compute |
| MVC / MVP / MVVM | Model-View separation; controller/presenter/viewmodel orchestration |
| Pipe and Filter | Sequential processing stages; data transformation pipeline |
| Service-Oriented (SOA) | Shared enterprise services; ESB; WSDL/contract-based |
| Micro-frontend | Independent frontend modules; shell/host application; runtime composition |
| Plugin / Extension | Core engine with pluggable extensions; defined extension points |

Assess: Is the chosen style appropriate for the domain? Is it consistently applied? Are deviations intentional or accidental?

## 2. Design Pattern Detection

Check for these patterns and evaluate their correctness of implementation:

### Creational
- **Singleton** — Single instance control (look for: private constructors, static instance, `getInstance()`)
- **Factory Method / Abstract Factory** — Object creation delegation (look for: `create*()` methods, factory classes)
- **Builder** — Complex object construction (look for: fluent APIs, `Builder` inner classes, chained `set*()`)
- **Prototype** — Clone-based creation (look for: `clone()`, `copy()` methods)
- **Dependency Injection** — External dependency provision (look for: constructor injection, DI containers, `@Inject`)

### Structural
- **Adapter** — Interface conversion (look for: wrappers around third-party APIs)
- **Facade** — Simplified interface (look for: classes aggregating multiple subsystems)
- **Decorator** — Dynamic behavior addition (look for: wrapper classes with same interface, middleware chains)
- **Proxy** — Access control/caching (look for: lazy loading, access checks before delegation)
- **Composite** — Tree structures (look for: recursive component hierarchies)
- **Bridge** — Abstraction-implementation separation (look for: parallel class hierarchies)

### Behavioral
- **Observer / Pub-Sub** — Event notification (look for: listeners, event emitters, subscriptions)
- **Strategy** — Interchangeable algorithms (look for: interface-based algorithm selection, policy objects)
- **Command** — Encapsulated requests (look for: command objects, undo/redo, execute/rollback)
- **State** — Behavior based on state (look for: state classes, state machines, transitions)
- **Template Method** — Algorithm skeleton (look for: abstract base with `*Hook()` or overridable steps)
- **Chain of Responsibility** — Sequential handlers (look for: middleware, handler chains, `next()` calls)
- **Iterator** — Sequential access (look for: custom iterators, `hasNext()`/`next()`)
- **Mediator** — Centralized communication (look for: hub classes coordinating colleagues)
- **Repository** — Data access abstraction (look for: `*Repository` classes, query encapsulation)
- **Specification** — Business rule encapsulation (look for: `isSatisfiedBy()`, composable filter objects)
- **Visitor** — Operation dispatch on type hierarchy (look for: `accept(visitor)`, double dispatch)

### Architectural Patterns
- **CQRS** — Separate read/write models
- **Event Sourcing** — State from event log
- **Saga / Process Manager** — Distributed transaction coordination
- **API Gateway** — Unified API entry point
- **Circuit Breaker** — Failure isolation
- **Sidecar** — Auxiliary process alongside main service
- **Strangler Fig** — Incremental migration
- **Backend for Frontend (BFF)** — Client-specific API layers

## 3. Clean Code & Principles Assessment

### SOLID Principles

| Principle | What to Check | Violation Indicators |
|---|---|---|
| **Single Responsibility (SRP)** | Does each class/module have one reason to change? | God classes, classes with mixed concerns (e.g., business logic + I/O), files >500 lines |
| **Open/Closed (OCP)** | Can behavior be extended without modifying source? | Switch/if-else chains on type, modifications required for new variants |
| **Liskov Substitution (LSP)** | Can subtypes replace parent types without breaking? | Overridden methods that throw `NotImplemented`, precondition strengthening |
| **Interface Segregation (ISP)** | Are interfaces focused and cohesive? | Fat interfaces with many methods, clients forced to implement unused methods |
| **Dependency Inversion (DIP)** | Do high-level modules depend on abstractions? | Direct instantiation of infrastructure in domain code, no interfaces |

### Other Principles

| Principle | What to Check |
|---|---|
| **DRY** | Duplicated logic, copy-pasted code blocks, repeated boilerplate |
| **KISS** | Over-engineered abstractions, unnecessary complexity, premature generalization |
| **YAGNI** | Unused code, speculative features, over-parameterized interfaces |
| **Separation of Concerns** | Mixed layers (UI logic in data access, business rules in controllers) |
| **Law of Demeter** | Long method chains (`a.getB().getC().doThing()`), excessive knowledge of internal structure |
| **Composition over Inheritance** | Deep inheritance hierarchies (>3 levels), inheritance for code reuse vs polymorphism |
| **Program to Interfaces** | Concrete types in signatures, hard-coded dependencies |
| **Fail Fast** | Silent error swallowing, empty catch blocks, deferred validation |
| **Principle of Least Surprise** | Misleading names, unexpected side effects, non-standard conventions |

### Code Quality Indicators

- **Naming** — Are names descriptive, consistent, and domain-aligned?
- **Function length** — Average function length? Functions >30 lines?
- **Cyclomatic complexity** — Deeply nested conditionals? Functions with >4 branching paths?
- **Comments** — Self-documenting code vs stale/misleading comments?
- **Error handling** — Consistent strategy? Custom exceptions? Graceful degradation?
- **Magic numbers/strings** — Hard-coded values without named constants?
- **Dead code** — Unused functions, commented-out blocks, unreachable branches?

## 4. Quality Attribute Evaluation

Rate each 1–5. Provide file-level evidence for each rating.

### Extensibility
- Are extension points clearly defined (interfaces, plugins, hooks, events)?
- Can new features be added without modifying existing code (OCP)?
- Is the module/plugin system well-designed?
- Are configurations externalized?
- Is feature toggling supported?

### Robustness
- Is input validation comprehensive (boundary, type, format, injection)?
- Are edge cases handled (empty collections, null/undefined, concurrent access)?
- Is defensive programming practiced (assertions, preconditions, invariants)?
- Are external failures handled (network, filesystem, third-party APIs)?
- Are resource limits enforced (memory, connections, file handles)?

### Availability
- Are there single points of failure?
- Is graceful degradation supported?
- Is state management designed for HA (stateless services, externalized state)?
- Are health checks implemented?
- Is horizontal scaling supported?
- Is there load balancing configuration?

### Fault Tolerance
- Are retry mechanisms implemented (with backoff, jitter)?
- Are circuit breakers present?
- Is timeout handling proper (connect, read, total)?
- Are transient vs permanent failures distinguished?
- Is there dead letter queue / poison message handling?
- Is idempotency ensured for retryable operations?
- Are fallback strategies defined?

### Maintainability
- Is the code easy to understand for a new developer?
- Are changes localized (low coupling, high cohesion)?
- Is technical debt documented?
- Are coding standards enforced (linters, formatters)?
- Is the dependency tree manageable?
- Is the build system well-organized?

### Testability
- Is dependency injection used consistently?
- Are there clear seams for mocking/stubbing?
- Is business logic separated from infrastructure?
- Are tests readable, deterministic, and fast?
- Is test coverage adequate for critical paths?
- Are integration and e2e tests present?

### Security
- Is input validation / sanitization implemented at boundaries?
- Is authentication/authorization sound (principle of least privilege)?
- Is sensitive data protected (encryption at rest/transit, secret management)?
- Are common vulnerabilities addressed (injection, XSS, CSRF, SSRF)?
- Are dependencies scanned for known vulnerabilities?
- Is audit logging present?

### Performance
- Are there O(n²) or worse algorithms on hot paths?
- Is caching used appropriately (with invalidation strategy)?
- Are database queries optimized (indexes, N+1, pagination)?
- Is lazy loading / pagination implemented?
- Are expensive operations async / background-processed?
- Is resource pooling used (connections, threads)?

### Scalability
- Can the system scale horizontally?
- Are stateful components identified and isolated?
- Is data partitioning / sharding considered?
- Are bottlenecks identified (shared resources, locks)?
- Is async / event-driven processing used where appropriate?

### Observability
- Is structured logging present?
- Are metrics collected (latency, throughput, error rates)?
- Is distributed tracing configured?
- Are alerts and dashboards defined?
- Are log levels used appropriately?

### Deployability
- Is CI/CD configured?
- Are deployments automated and repeatable?
- Is rollback supported?
- Is blue/green or canary deployment supported?
- Is infrastructure as code used?
- Are database migrations versioned and reversible?

### Data Integrity & Consistency
- Are data validation boundaries clearly defined?
- Is transactional consistency maintained across operations?
- Are race conditions addressed (optimistic/pessimistic locking)?
- Is data schema evolution managed (migrations, backward compatibility)?
- Are backup and recovery strategies in place?

## 5. Anti-Pattern Detection

Flag these if found:

| Anti-Pattern | Symptoms |
|---|---|
| **God Class / Object** | Single class with >20 methods or >500 lines, handles multiple unrelated concerns |
| **Spaghetti Code** | Tangled control flow, unclear execution path, heavy use of goto/global state |
| **Lava Flow** | Dead code left because "we might need it", commented-out blocks, orphaned files |
| **Golden Hammer** | One tool/pattern applied everywhere regardless of fit |
| **Premature Optimization** | Complex caching/threading without measured need |
| **Big Ball of Mud** | No discernible architecture, everything depends on everything |
| **Leaky Abstraction** | Implementation details exposed through abstractions |
| **Anemic Domain Model** | Domain objects are pure data, logic lives in service classes |
| **Circular Dependencies** | Modules importing each other; bidirectional coupling |
| **Distributed Monolith** | Microservices that must deploy together, shared databases, synchronous chains |
| **Primitive Obsession** | Using strings/ints where domain types are appropriate |
| **Feature Envy** | Methods that use more data from other classes than their own |
| **Shotgun Surgery** | Single change requires modifications across many files |
| **Tight Coupling** | Direct dependencies between unrelated modules, inability to test in isolation |
| **Callback Hell / Promise Chains** | Deeply nested async code without proper abstraction |
| **Service Locator** | Runtime dependency lookup instead of injection; hidden dependencies |
| **Copy-Paste Architecture** | Duplicated modules with slight variations instead of proper abstraction |
| **Inappropriate Intimacy** | Classes that access each other's private/internal details extensively |

## 6. Cross-Cutting Concerns

Evaluate how these are handled:

- **Logging** — Strategy, levels, structured vs unstructured, correlation IDs
- **Error Handling** — Global handlers, error boundaries, custom exceptions, error reporting
- **Configuration** — Externalized, environment-specific, secret management, validation
- **Authentication & Authorization** — Strategy, middleware, role/permission model
- **Caching** — Strategy, invalidation, layers (in-memory, distributed, CDN)
- **Transaction Management** — Boundaries, distributed transactions, compensation
- **Internationalization** — String extraction, locale handling, formatting
- **API Versioning** — Strategy (URL, header, content negotiation), deprecation policy
- **Rate Limiting & Throttling** — Implementation, granularity, response codes

## 7. Dependency & Coupling Analysis

- **External dependencies** — Count, freshness, license compatibility, vulnerability status
- **Internal coupling** — Afferent and efferent coupling per module
- **Dependency direction** — Do dependencies flow inward (good) or outward from domain (bad)?
- **Vendor lock-in** — How tightly coupled to specific cloud/framework/library?
- **Abstraction quality** — Are third-party integrations wrapped behind interfaces?
