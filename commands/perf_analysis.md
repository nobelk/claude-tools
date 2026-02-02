# Performance Profiling Analysis Command
# Usage: Analyze application performance bottlenecks: <PROFILING_DATA|LOG_FILE|CLASS_NAME>

# Parse performance target
Set PERF_TARGET to $Arguments
Validate that PERF_TARGET is provided, otherwise error "Please provide profiling data, log file, or class name"

# Step 1: Initial Assessment
Execute these analyses in parallel:
- Scan for common performance anti-patterns in code
- Search for database queries (SQL, ORM patterns)
- Identify I/O operations (file, network, database)
- Locate loops and recursive functions
- Find thread/async operations

# Step 2: Performance Analysis
## Identify performance bottlenecks

### CPU Analysis
- Hot methods and CPU-intensive operations
- Inefficient algorithms (nested loops, O(n²) or worse)
- Unnecessary object creation in tight loops
- Regex compilation in loops
- String concatenation in loops (use StringBuilder)

### Memory Analysis
- Memory leaks (unclosed resources, growing collections)
- Excessive object allocations
- Large object graphs held in memory
- Missing weak/soft references where appropriate
- Static collection growth

### Database Performance
- N+1 query problems (ORM lazy loading)
- Missing indexes on frequently queried columns
- Full table scans
- Unoptimized JOIN operations
- Missing connection pooling
- Long-running transactions

### I/O Performance
- Synchronous I/O blocking main threads
- Missing buffering for file operations
- Unbatched network requests
- Missing response compression
- Large payload transfers

### Concurrency Issues
- Lock contention and deadlocks
- Unnecessary synchronization
- Missing parallelization opportunities
- Thread pool exhaustion
- Race conditions affecting performance

# Step 3: Bottleneck Categorization

## CRITICAL (Immediate performance impact)
- Memory leaks causing OutOfMemory errors
- Infinite loops or unbounded recursion
- Blocking I/O on main/UI threads
- Database queries without indexes on large tables
- Connection/resource leaks

## HIGH (Significant performance degradation)
- N+1 query problems
- O(n²) algorithms where O(n log n) or O(n) is achievable
- Missing caching for expensive repeated operations
- Synchronous operations that should be async
- Excessive logging in hot paths

## MEDIUM (Noticeable performance impact)
- Suboptimal data structures
- Unnecessary serialization/deserialization
- Missing connection pooling
- Redundant computations
- Inefficient collection operations

## LOW (Minor optimization opportunities)
- Micro-optimizations
- Code style improvements
- Minor caching opportunities
- Logging level adjustments

# Step 4: Optimization Recommendations

For each identified bottleneck, provide:
1. **Current Issue**: Description with code location (file:line)
2. **Impact**: Quantified performance impact when possible
3. **Solution**: Specific fix with code example
4. **Verification**: How to measure improvement

# Step 5: Generate Output

## Output Format

### Performance Analysis Summary
**Target**: [File/Class/Module analyzed]
**Analysis Date**: [Date]
**Critical Issues**: [Count]
**High Priority Issues**: [Count]

### Executive Summary
[2-3 sentences describing overall performance health and key concerns]

### Bottleneck Inventory
| ID | Category | Severity | Location | Description | Est. Impact |
|----|----------|----------|----------|-------------|-------------|
| P1 | [CPU/Memory/DB/IO] | [CRIT/HIGH/MED/LOW] | [file:line] | [Brief description] | [e.g., 50% latency] |

### Detailed Findings

#### [P1] [Issue Title]
- **Category**: [CPU/Memory/Database/I/O/Concurrency]
- **Severity**: [CRITICAL/HIGH/MEDIUM/LOW]
- **Location**: `[file:line]`
- **Description**: [Detailed explanation]
- **Current Code**:
```
[problematic code snippet]
```
- **Recommended Fix**:
```
[optimized code snippet]
```
- **Expected Improvement**: [Quantified when possible]
- **Testing Approach**: [How to verify the fix]

### Monitoring Recommendations
- Key metrics to track
- Alerting thresholds to set
- Dashboard suggestions

### Load Testing Recommendations
- Suggested test scenarios
- Expected performance baselines
- Tools to use (JMeter, Gatling, k6, etc.)

### Quick Wins
[List of low-effort, high-impact optimizations]

### Long-term Improvements
[Architectural changes for sustained performance]
