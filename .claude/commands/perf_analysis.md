# Performance Profiling Analysis Command
# Usage: Analyze application performance bottlenecks: <PROFILING_DATA|LOG_FILE|CLASS_NAME>

# Parse performance target
Set PERF_TARGET to $Arguments
Validate that PERF_TARGET is provided, otherwise error "Please provide profiling data, log file, or class name"

# Step 1: Performance Analysis
## Identify performance bottlenecks
- CPU usage hotspots and inefficient algorithms
- Memory leaks and excessive allocations
- Database query performance (N+1 problems, slow queries)
- Network I/O bottlenecks
- Caching opportunities and inefficiencies

# Step 2: Bottleneck Categorization
## CRITICAL (Immediate performance impact)
- Memory leaks causing OutOfMemory errors
- Infinite loops or recursive calls
- Blocking I/O operations on main threads
- Database queries without proper indexing

## HIGH (Significant performance degradation)
- N+1 query problems
- Inefficient algorithms (O(n²) where O(n) possible)
- Missing caching for expensive operations
- Synchronous operations that could be async

# Step 3: Optimization Recommendations
- Provide specific performance improvements
- Include before/after performance metrics
- Suggest monitoring and alerting strategies
- Recommend load testing approaches
- Generate performance benchmarks
