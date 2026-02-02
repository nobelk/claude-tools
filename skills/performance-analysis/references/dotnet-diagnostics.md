# .NET Performance Diagnostics Reference

## Table of Contents
1. Tool Installation
2. dotnet-counters (Live Metrics)
3. dotnet-trace (CPU / Event Profiling)
4. dotnet-dump (Memory Analysis)
5. dotnet-gcdump (GC Heap Snapshots)
6. dotnet-monitor (Remote / Container Diagnostics)
7. BenchmarkDotNet (Micro-benchmarks)
8. PerfView (Windows ETW)
9. Visual Studio Diagnostic Tools
10. Entity Framework Query Analysis
11. ASP.NET Core Diagnostics
12. Interpreting Results

---

## 1. Tool Installation

```bash
# Install all .NET diagnostic CLI tools globally
dotnet tool install --global dotnet-counters
dotnet tool install --global dotnet-trace
dotnet tool install --global dotnet-dump
dotnet tool install --global dotnet-gcdump
dotnet tool install --global dotnet-monitor

# Verify installations
dotnet tool list --global
```

If tools are already installed, update to latest:
```bash
dotnet tool update --global dotnet-counters
```

## 2. dotnet-counters — Live Metrics

Real-time monitoring of runtime counters. Use to quickly identify CPU, GC, threadpool, or HTTP anomalies.

### List running .NET processes
```bash
dotnet-counters ps
```

### Monitor default counters
```bash
dotnet-counters monitor --process-id <PID>
```

### Monitor specific counter providers
```bash
# Runtime counters (GC, threadpool, exceptions)
dotnet-counters monitor --process-id <PID> \
  --counters System.Runtime

# ASP.NET Core counters
dotnet-counters monitor --process-id <PID> \
  --counters Microsoft.AspNetCore.Hosting

# HTTP client counters
dotnet-counters monitor --process-id <PID> \
  --counters System.Net.Http

# EF Core counters
dotnet-counters monitor --process-id <PID> \
  --counters Microsoft.EntityFrameworkCore

# All useful providers combined
dotnet-counters monitor --process-id <PID> \
  --counters System.Runtime,Microsoft.AspNetCore.Hosting,System.Net.Http,Microsoft.EntityFrameworkCore
```

### Collect counters to file for analysis
```bash
dotnet-counters collect --process-id <PID> \
  --format csv \
  --output perf_counters.csv \
  --counters System.Runtime,Microsoft.AspNetCore.Hosting \
  --refresh-interval 1
```

### Key counters to watch

| Counter | Healthy | Warning |
|---------|---------|---------|
| `gc-heap-size` | Stable | Monotonically increasing → leak |
| `gen-0-gc-count` | Moderate rate | Extremely high → excess allocations |
| `gen-2-gc-count` | Low rate | High rate → LOH issues or memory pressure |
| `threadpool-queue-length` | Near 0 | Growing → threadpool starvation |
| `threadpool-thread-count` | Stable | Climbing → blocking calls on pool threads |
| `exception-count` | Low | High → exceptions used for control flow |
| `monitor-lock-contention-count` | Near 0 | High → lock contention |
| `working-set` | Stable | Monotonically increasing → leak |
| `active-timer-count` | Stable | Growing → timer leaks |

## 3. dotnet-trace — CPU / Event Profiling

Collect detailed traces for CPU profiling, event analysis, and performance investigation.

### Collect a CPU profile (default: 30 seconds)
```bash
dotnet-trace collect --process-id <PID> \
  --duration 00:00:30 \
  --output cpu_profile.nettrace
```

### Profile with specific providers
```bash
# CPU sampling profile
dotnet-trace collect --process-id <PID> \
  --profile cpu-sampling \
  --output cpu_sampling.nettrace

# GC detailed events
dotnet-trace collect --process-id <PID> \
  --providers Microsoft-Windows-DotNETRuntime:0x1:5 \
  --output gc_events.nettrace

# GC allocation tracking (verbose — use briefly)
dotnet-trace collect --process-id <PID> \
  --providers Microsoft-Windows-DotNETRuntime:0x200001:5 \
  --output gc_alloc.nettrace

# ASP.NET Core request timing
dotnet-trace collect --process-id <PID> \
  --providers Microsoft.AspNetCore:5 \
  --output aspnet_trace.nettrace

# ThreadPool events
dotnet-trace collect --process-id <PID> \
  --providers Microsoft-Windows-DotNETRuntime:0x10000:4 \
  --output threadpool.nettrace
```

### Convert trace to SpeedScope format (viewable in browser)
```bash
dotnet-trace convert cpu_profile.nettrace --format Speedscope
# Open the .speedscope.json file at https://www.speedscope.app
```

### Convert to Chromium format
```bash
dotnet-trace convert cpu_profile.nettrace --format Chromium
# Open in Chrome DevTools → Performance tab → Load Profile
```

## 4. dotnet-dump — Memory Analysis

Capture and analyze memory dumps to find leaks and large allocations.

### Capture a dump
```bash
# Full dump (large, complete)
dotnet-dump collect --process-id <PID> --type Full --output full_dump.dmp

# Heap-only dump (smaller, sufficient for most memory analysis)
dotnet-dump collect --process-id <PID> --type Heap --output heap_dump.dmp
```

### Analyze a dump interactively
```bash
dotnet-dump analyze heap_dump.dmp
```

### Key SOS commands inside dotnet-dump analyze

```
# Heap summary — shows total size per generation
dumpheap -stat

# Top objects by total size
dumpheap -stat | sort by size (look at bottom of output)

# Find all instances of a specific type
dumpheap -type System.String -stat
dumpheap -type MyApp.Models.Order -stat

# Show details of a specific object
dumpobj <address>

# GC roots — why an object is alive (find leaks)
gcroot <address>

# Finalizer queue — objects awaiting finalization
finalizequeue

# Thread stacks — see what threads are doing
clrthreads
dumpstack

# Sync blocks — find lock contention
syncblk

# Dump all exceptions
dumpheap -type Exception -stat

# Memory regions and segment info
eeheap -gc
```

### Automated leak detection workflow
```bash
# 1. Take dump at T=0
dotnet-dump collect --process-id <PID> --type Heap --output dump_t0.dmp
# 2. Wait while workload runs (e.g., 5 minutes)
# 3. Take dump at T=1
dotnet-dump collect --process-id <PID> --type Heap --output dump_t1.dmp
# 4. Compare dumpheap -stat output between the two dumps
#    Objects with growing counts/sizes are likely leaking
```

## 5. dotnet-gcdump — GC Heap Snapshots

Lightweight alternative to full dumps for GC heap analysis. Lower overhead, safe for production.

```bash
# Capture a GC heap snapshot
dotnet-gcdump collect --process-id <PID> --output gc_snapshot.gcdump

# View in Visual Studio: File → Open → gc_snapshot.gcdump
# Or use PerfView to open .gcdump files
```

### When to use gcdump vs dump
- **gcdump**: Quick, low overhead, shows object types and sizes, safe for production.
- **dump**: Full memory content, allows object inspection, root analysis, thread stacks.

## 6. dotnet-monitor — Remote / Container Diagnostics

For containerized or remote applications.

```bash
# Run as a sidecar or standalone
dotnet monitor collect --urls http://localhost:52323

# API endpoints (accessible via HTTP):
# GET /processes                — list processes
# GET /dump/{pid}               — capture dump
# GET /gcdump/{pid}             — capture gcdump
# GET /trace/{pid}              — collect trace
# GET /livemetrics/{pid}        — stream live metrics
# GET /logs/{pid}               — stream logs
```

## 7. BenchmarkDotNet — Micro-benchmarks

Add to a project for rigorous micro-benchmarking.

### Setup
```bash
dotnet add package BenchmarkDotNet
```

### Example benchmark class
```csharp
using BenchmarkDotNet.Attributes;
using BenchmarkDotNet.Running;

[MemoryDiagnoser]          // Track allocations
[ThreadingDiagnoser]       // Track thread contention
[DisassemblyDiagnoser]     // Show JIT-generated assembly
public class MyBenchmarks
{
    [Benchmark(Baseline = true)]
    public string StringConcat()
    {
        var s = "";
        for (int i = 0; i < 1000; i++) s += i.ToString();
        return s;
    }

    [Benchmark]
    public string StringBuilder()
    {
        var sb = new System.Text.StringBuilder();
        for (int i = 0; i < 1000; i++) sb.Append(i);
        return sb.ToString();
    }
}

// Run: BenchmarkRunner.Run<MyBenchmarks>();
```

### Run from CLI
```bash
dotnet run -c Release -- --filter '*MyBenchmarks*'
```

### Key diagnosers
- `[MemoryDiagnoser]` — Gen0/Gen1/Gen2 collections, allocated bytes.
- `[ThreadingDiagnoser]` — lock contention, thread count.
- `[EventPipeProfiler(EventPipeProfile.CpuSampling)]` — CPU profile per benchmark.

## 8. PerfView (Windows ETW)

PerfView is the gold standard for deep .NET performance analysis on Windows.

### Common commands
```bash
# Collect CPU and GC events for 30 seconds
PerfView collect /BufferSizeMB:512 /CircularMB:512 /MaxCollectSec:30

# Collect with .NET allocation tracking
PerfView collect /GCCollectOnly /MaxCollectSec:30

# Collect thread time (wall clock analysis including I/O waits)
PerfView collect /ThreadTime /MaxCollectSec:30

# Open a trace
PerfView open my_trace.etl.zip
```

### Key views in PerfView
- **CPU Stacks**: Hot methods by CPU time.
- **GC Stats**: GC pause times, gen0/1/2 collections, allocation rates.
- **Thread Time Stacks**: Wall-clock time including I/O and lock waits.
- **GC Heap Snapshots**: Object graph analysis for leaks.
- **Events**: Raw ETW events for custom analysis.

## 9. Visual Studio Diagnostic Tools

### Performance Profiler (Alt+F2)
Available tools (select one or more):
- **CPU Usage** — call tree with hot path highlighting.
- **.NET Object Allocation Tracking** — allocation call stacks and types.
- **Memory Usage** — heap snapshots with diff comparison.
- **Database** — ADO.NET / EF Core query timing and counts.
- **Events Viewer** — ETW events inline with timeline.
- **.NET Async** — async state machine visualization.
- **Instrumentation** — exact call counts and timings.

### Diagnostic Tools (debug-time, F5)
- CPU timeline
- Memory timeline with snapshot comparison
- Events pane (exceptions, GC, module loads)

## 10. Entity Framework Core Query Analysis

### Enable sensitive data logging (development only)
```csharp
optionsBuilder
    .LogTo(Console.WriteLine, LogLevel.Information)
    .EnableSensitiveDataLogging()
    .EnableDetailedErrors();
```

### Detect N+1 at runtime
```csharp
// In Program.cs or Startup.cs (development only)
optionsBuilder.ConfigureWarnings(w =>
    w.Throw(RelationalEventId.MultipleCollectionIncludeWarning));
```

### Query tags for tracing
```csharp
var orders = context.Orders
    .TagWith("GetRecentOrders - OrderService.cs:42")
    .Where(o => o.Date > cutoff)
    .ToListAsync();
```

### Compiled queries for hot paths
```csharp
private static readonly Func<MyDbContext, int, Task<Order?>> GetOrderById =
    EF.CompileAsyncQuery((MyDbContext ctx, int id) =>
        ctx.Orders.Include(o => o.Items).FirstOrDefault(o => o.Id == id));
```

### Key EF Core counters (via dotnet-counters)
| Counter | Meaning |
|---------|---------|
| `active-db-contexts` | Open DbContext instances |
| `total-queries` | Cumulative query count |
| `queries-per-second` | Query throughput |
| `total-save-changes` | Cumulative SaveChanges calls |
| `optimistic-concurrency-failures` | Conflict count |
| `total-execution-strategy-operation-failures` | Retry failures |

## 11. ASP.NET Core Diagnostics

### Request timing middleware
```csharp
app.Use(async (context, next) =>
{
    var sw = Stopwatch.StartNew();
    context.Response.OnCompleted(() =>
    {
        sw.Stop();
        if (sw.ElapsedMilliseconds > 500)
            logger.LogWarning("Slow request: {Method} {Path} took {Elapsed}ms",
                context.Request.Method, context.Request.Path, sw.ElapsedMilliseconds);
        return Task.CompletedTask;
    });
    await next();
});
```

### Key ASP.NET Core counters (via dotnet-counters)
| Counter | Healthy | Warning |
|---------|---------|---------|
| `requests-per-second` | Stable under load | Dropping → bottleneck |
| `current-requests` | Low | Growing → threadpool starvation |
| `failed-requests` | Near 0 | Rising → errors |
| `request-queue-length` | 0 | Growing → can't keep up |

## 12. Interpreting Results

### CPU profiling interpretation
- **Flat profile**: Methods consuming the most CPU time. Top offenders are optimization targets.
- **Call tree**: Identify which callers contribute the most to a method's inclusive time.
- **Hot path**: The call chain consuming the most CPU — optimize the leaf method or reduce call frequency.

### Memory analysis interpretation
- **Growing working set + growing GC heap**: Memory leak. Use `gcroot` in dump to find what holds references.
- **High Gen0 GC rate**: Excessive allocations. Profile allocations with `dotnet-trace` allocation provider.
- **High Gen2 GC rate**: Large/long-lived objects promoted unnecessarily. Check LOH allocations and pinning.
- **High % time in GC**: Application spending too much time collecting. Reduce allocation rate or increase heap budget.

### ThreadPool interpretation
- **Growing queue length + growing thread count**: Blocking calls starving the pool. Find synchronous I/O or `.Result`/`.Wait()` calls.
- **High lock contention count**: Reduce lock granularity or switch to lock-free structures.

### Database interpretation
- **Query count >> expected**: N+1 or chatty access pattern.
- **Slow individual queries**: Missing index or suboptimal plan. Check execution plan.
- **High connection count**: Missing pooling or connection leaks (not disposing `DbConnection`).
