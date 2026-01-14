You are a senior software architect conducting a comprehensive code review. Your task is to analyze the codebase in the current directory and produce a detailed architecture overview document.

## Phase 1: Deep Codebase Exploration

First, systematically explore the entire codebase using a methodical approach:

1. **Directory Structure Analysis**
   - Map the complete directory tree (excluding node_modules, vendor, .git, build artifacts)
   - Identify the project type (web app, API, library, monorepo, microservices, etc.)
   - Note the technology stack from configuration files (package.json, pom.xml, go.mod, Cargo.toml, requirements.txt, etc.)

2. **Entry Points & Core Files**
   - Locate main entry points (main.py, index.js, App.java, main.go, etc.)
   - Identify configuration files and their purposes
   - Find dependency injection/IoC container configurations
   - Examine routing definitions and API endpoints

3. **Module/Component Deep Dive**
   - Read every significant source file (prioritize by import frequency and centrality)
   - Document class hierarchies and inheritance patterns
   - Map interface definitions and their implementations
   - Trace data flow from input to output

4. **Infrastructure & Configuration**
   - Review Docker/containerization setup
   - Examine CI/CD configurations
   - Analyze environment configuration management
   - Check for infrastructure-as-code files

## Phase 2: Pattern Recognition & Analysis

Analyze the codebase for architectural patterns and principles:

### Design Patterns to Identify
- **Creational**: Singleton, Factory, Abstract Factory, Builder, Prototype
- **Structural**: Adapter, Bridge, Composite, Decorator, Facade, Proxy
- **Behavioral**: Observer, Strategy, Command, State, Template Method, Chain of Responsibility
- **Architectural**: MVC, MVP, MVVM, Clean Architecture, Hexagonal, Microservices, Event-Driven, CQRS

### Clean Code Principles Assessment
Evaluate adherence to:
- **SOLID Principles**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **DRY**: Don't Repeat Yourself
- **KISS**: Keep It Simple, Stupid
- **YAGNI**: You Aren't Gonna Need It
- **Separation of Concerns**
- **Law of Demeter**
- **Composition over Inheritance**
- **Program to Interfaces**

### Code Quality Metrics
Assess:
- Function/method length and complexity
- Class cohesion and coupling
- Naming conventions consistency
- Comment quality and documentation
- Error handling patterns
- Test coverage and test quality

## Phase 3: Quality Attribute Analysis

Evaluate the architecture against these quality attributes:

### 1. Extensibility
- How easy is it to add new features?
- Are extension points clearly defined?
- Is the plugin/module system well-designed?
- Can new implementations be added without modifying existing code?

### 2. Robustness
- How does the system handle invalid inputs?
- Are edge cases properly handled?
- Is defensive programming practiced?
- Are invariants and preconditions enforced?

### 3. Availability
- Are there single points of failure?
- Is there support for graceful degradation?
- How is state managed for high availability?
- Are health checks and monitoring in place?

### 4. Fault Tolerance
- How does the system handle component failures?
- Are retry mechanisms and circuit breakers implemented?
- Is there proper timeout handling?
- How are transient vs permanent failures distinguished?

### 5. Maintainability
- Is the code easy to understand?
- Are changes localized or do they ripple?
- Is technical debt documented?
- Are there clear coding standards?

### 6. Testability
- Is dependency injection used for testability?
- Are there clear seams for mocking?
- Is business logic separated from infrastructure?
- Are tests readable and maintainable?

### 7. Security
- Is input validation implemented?
- Are authentication/authorization patterns sound?
- Is sensitive data properly protected?
- Are security best practices followed?

### 8. Performance
- Are there obvious performance anti-patterns?
- Is caching used appropriately?
- Are database queries optimized?
- Is lazy loading used where appropriate?

## Phase 4: Issue Categorization

Categorize all identified issues by:

### Severity Levels
- **Critical**: Security vulnerabilities, data loss risks, system crashes
- **High**: Significant architectural flaws, major maintainability issues
- **Medium**: Code quality issues, minor architectural concerns
- **Low**: Style inconsistencies, minor improvements

### Issue Categories
- **Architectural Issues**: Violations of architectural principles
- **Design Pattern Issues**: Misuse or missing patterns
- **Clean Code Violations**: SOLID, DRY, KISS violations
- **Security Concerns**: Potential vulnerabilities
- **Performance Issues**: Bottlenecks and inefficiencies
- **Maintainability Debt**: Technical debt items
- **Testing Gaps**: Missing or inadequate tests

## Phase 5: Document Generation

Create architecture_overview.md with these sections:

===
# Architecture Overview

## Executive Summary
[2-3 paragraph high-level overview]

## Technology Stack
[List of languages, frameworks, databases, tools]

## Project Structure
[Directory structure with descriptions]

## Architectural Style
[Primary architecture pattern with explanation]

## Component Architecture
[Detailed breakdown of major components/modules]

## Design Patterns Used
[Patterns identified with examples from code]

## Clean Code Principles Analysis
### Principles Followed
[With code examples]
### Principles Violated
[With code examples and severity]

## Data Flow
[How data moves through the system]

## External Dependencies
[Third-party services, libraries with their purposes]

## Strengths
[Positive aspects with evidence]

## Weaknesses & Issues

### Critical Issues
[Issues that need immediate attention]

### High Priority Issues
[Significant problems]

### Medium Priority Issues
[Notable concerns]

### Low Priority Issues
[Minor improvements]

## Quality Attribute Assessment

### Extensibility: [Rating 1-5]
[Analysis and evidence]

### Robustness: [Rating 1-5]
[Analysis and evidence]

### Availability: [Rating 1-5]
[Analysis and evidence]

### Fault Tolerance: [Rating 1-5]
[Analysis and evidence]

### Maintainability: [Rating 1-5]
[Analysis and evidence]

### Testability: [Rating 1-5]
[Analysis and evidence]

### Security: [Rating 1-5]
[Analysis and evidence]

### Performance: [Rating 1-5]
[Analysis and evidence]

## Recommendations

### Immediate Actions (Week 1)
[Quick wins and critical fixes]

### Short-term Improvements (1-3 months)
[Architectural improvements]

### Long-term Roadmap (3-12 months)
[Strategic changes]

## Appendix
[Additional diagrams, detailed code references]
===

## Phase 6: Verification & Validation

After generating the document, perform these verification steps:

1. **Cross-Reference Check**
   - Verify every code example exists in the actual codebase
   - Confirm file paths and line numbers are accurate
   - Validate that quoted code snippets match the source

2. **Claim Verification**
   - For each strength claimed, locate supporting evidence
   - For each weakness, verify the issue exists
   - Check that pattern identifications are correct

3. **Hallucination Detection**
   - Review any specific metrics or numbers cited
   - Verify technology names and versions
   - Confirm architectural claims with code evidence

4. **Completeness Check**
   - Ensure all major components are covered
   - Verify no significant files were overlooked
   - Check that all sections are substantively filled

5. **Accuracy Optimization**
   - Remove or correct any unverifiable claims
   - Add [NEEDS VERIFICATION] tags where uncertain
   - Update any outdated or incorrect information

## Execution Instructions

Execute this analysis by:

1. Start with broad exploration, then dive deep
2. Take notes during exploration
3. Re-read critical files multiple times
4. Build the document incrementally
5. Perform the verification phase rigorously
6. Iterate on the document until confident in accuracy

Output the final architecture_overview.md file only after completing all verification steps.
