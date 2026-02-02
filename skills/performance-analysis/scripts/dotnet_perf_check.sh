#!/usr/bin/env bash
# dotnet_perf_check.sh — Automated .NET performance diagnostic collection
#
# Usage:
#   ./dotnet_perf_check.sh --pid <PID>               Diagnose a running process
#   ./dotnet_perf_check.sh --project <path.csproj>    Build, run, and diagnose a project
#   ./dotnet_perf_check.sh --dll <path.dll>           Run and diagnose a compiled assembly
#
# Options:
#   --duration <seconds>   Collection duration (default: 15)
#   --output <dir>         Output directory (default: ./perf_output)
#   --skip-trace           Skip dotnet-trace collection
#   --skip-dump            Skip memory dump collection
#   --counters-only        Only collect counter snapshots

set -euo pipefail

# --- Platform detection ---
OS="$(uname -s)"
ARCH="$(uname -m)"

# Portable ISO-8601 timestamp (BSD date on macOS lacks -Iseconds)
iso_timestamp() {
  if date -Iseconds &>/dev/null; then
    date -Iseconds
  else
    date -u +"%Y-%m-%dT%H:%M:%S+00:00"
  fi
}

DURATION=15
OUTPUT_DIR="./perf_output"
PID=""
PROJECT=""
DLL=""
SKIP_TRACE=false
SKIP_DUMP=false
COUNTERS_ONLY=false
STARTED_PROCESS=false

usage() {
  echo "Usage: $0 [--pid <PID> | --project <path.csproj> | --dll <path.dll>]"
  echo "  --duration <seconds>   Collection duration (default: 15)"
  echo "  --output <dir>         Output directory (default: ./perf_output)"
  echo "  --skip-trace           Skip dotnet-trace collection"
  echo "  --skip-dump            Skip memory dump collection"
  echo "  --counters-only        Only collect counter snapshots"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case $1 in
    --pid)       PID="$2"; shift 2 ;;
    --project)   PROJECT="$2"; shift 2 ;;
    --dll)       DLL="$2"; shift 2 ;;
    --duration)  DURATION="$2"; shift 2 ;;
    --output)    OUTPUT_DIR="$2"; shift 2 ;;
    --skip-trace)   SKIP_TRACE=true; shift ;;
    --skip-dump)    SKIP_DUMP=true; shift ;;
    --counters-only) COUNTERS_ONLY=true; shift ;;
    -h|--help)   usage ;;
    *)           echo "Unknown option: $1"; usage ;;
  esac
done

mkdir -p "$OUTPUT_DIR"
LOG="$OUTPUT_DIR/diagnostic_log.txt"
echo "=== .NET Performance Diagnostic Collection ===" | tee "$LOG"
echo "Started: $(iso_timestamp)" | tee -a "$LOG"
echo "Platform: $OS ($ARCH)" | tee -a "$LOG"
echo "Duration: ${DURATION}s" | tee -a "$LOG"

# --- Ensure diagnostic tools are installed ---
# Format duration as HH:MM:SS (handles values >= 60 seconds)
format_duration() {
  local secs=$1
  printf "%02d:%02d:%02d" $((secs / 3600)) $(((secs % 3600) / 60)) $((secs % 60))
}

ensure_tool() {
  local tool=$1
  if ! command -v "$tool" &>/dev/null; then
    echo "[INFO] Installing $tool..." | tee -a "$LOG"
    dotnet tool install --global "$tool" 2>>"$LOG" || true
  fi
}

ensure_tool dotnet-counters
ensure_tool dotnet-trace
ensure_tool dotnet-dump
ensure_tool dotnet-gcdump

# --- Resolve PID ---
if [[ -n "$PROJECT" ]]; then
  echo "[INFO] Building project: $PROJECT" | tee -a "$LOG"
  dotnet build "$PROJECT" -c Release --nologo -v quiet 2>>"$LOG"
  echo "[INFO] Starting project in background..." | tee -a "$LOG"
  dotnet run --project "$PROJECT" -c Release --no-build &
  PID=$!
  STARTED_PROCESS=true
  sleep 3
elif [[ -n "$DLL" ]]; then
  echo "[INFO] Starting assembly: $DLL" | tee -a "$LOG"
  dotnet "$DLL" &
  PID=$!
  STARTED_PROCESS=true
  sleep 3
fi

if [[ -z "$PID" ]]; then
  echo "[ERROR] No target specified. Use --pid, --project, or --dll." | tee -a "$LOG"
  echo "" | tee -a "$LOG"
  echo "Available .NET processes:" | tee -a "$LOG"
  dotnet-counters ps 2>/dev/null | tee -a "$LOG" || echo "(none found)"
  exit 1
fi

# Verify process exists
if ! kill -0 "$PID" 2>/dev/null; then
  echo "[ERROR] Process $PID not found or not accessible." | tee -a "$LOG"
  if [[ "$OS" == "Darwin" ]]; then
    echo "[HINT] macOS System Integrity Protection (SIP) may block process attachment." | tee -a "$LOG"
    echo "       Try running with sudo, or use --project/--dll to let this script launch the process." | tee -a "$LOG"
  fi
  exit 1
fi

echo "Target PID: $PID" | tee -a "$LOG"
echo "Output dir: $OUTPUT_DIR" | tee -a "$LOG"
echo "" | tee -a "$LOG"

cleanup() {
  if [[ "$STARTED_PROCESS" == true ]] && kill -0 "$PID" 2>/dev/null; then
    echo "[INFO] Stopping started process $PID" | tee -a "$LOG"
    kill "$PID" 2>/dev/null || true
    wait "$PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT

# --- Step 1: Counter snapshot ---
echo "=== Step 1: Collecting runtime counters (${DURATION}s) ===" | tee -a "$LOG"
COUNTER_FILE="$OUTPUT_DIR/counters.csv"
dotnet-counters collect \
  --process-id "$PID" \
  --format csv \
  --output "$COUNTER_FILE" \
  --counters "System.Runtime,Microsoft.AspNetCore.Hosting,System.Net.Http,Microsoft.EntityFrameworkCore" \
  --refresh-interval 1 \
  &
COUNTER_PID=$!

# Let counters collect for the duration
sleep "$DURATION"
kill "$COUNTER_PID" 2>/dev/null || true
wait "$COUNTER_PID" 2>/dev/null || true
echo "[OK] Counters saved to $COUNTER_FILE" | tee -a "$LOG"

if [[ "$COUNTERS_ONLY" == true ]]; then
  echo "" | tee -a "$LOG"
  echo "=== Counters-only mode — skipping trace and dump ===" | tee -a "$LOG"
  echo "=== Collection complete ===" | tee -a "$LOG"
  echo "Results in: $OUTPUT_DIR" | tee -a "$LOG"
  exit 0
fi

# --- Step 2: CPU trace ---
if [[ "$SKIP_TRACE" == false ]]; then
  echo "" | tee -a "$LOG"
  echo "=== Step 2: Collecting CPU trace (${DURATION}s) ===" | tee -a "$LOG"
  TRACE_FILE="$OUTPUT_DIR/cpu_profile.nettrace"
  dotnet-trace collect \
    --process-id "$PID" \
    --profile cpu-sampling \
    --duration "$(format_duration "$DURATION")" \
    --output "$TRACE_FILE" \
    2>>"$LOG" || { echo "[WARN] Trace collection failed" | tee -a "$LOG"; }

  if [[ -f "$TRACE_FILE" ]]; then
    echo "[OK] Trace saved to $TRACE_FILE" | tee -a "$LOG"
    # Convert to SpeedScope for browser viewing
    dotnet-trace convert "$TRACE_FILE" --format Speedscope 2>>"$LOG" || true
    echo "[OK] SpeedScope conversion attempted" | tee -a "$LOG"
  fi
else
  echo "" | tee -a "$LOG"
  echo "=== Step 2: Skipped (--skip-trace) ===" | tee -a "$LOG"
fi

# --- Step 3: GC dump ---
echo "" | tee -a "$LOG"
echo "=== Step 3: Collecting GC heap snapshot ===" | tee -a "$LOG"
GCDUMP_FILE="$OUTPUT_DIR/gc_snapshot.gcdump"
dotnet-gcdump collect \
  --process-id "$PID" \
  --output "$GCDUMP_FILE" \
  2>>"$LOG" || { echo "[WARN] GC dump collection failed" | tee -a "$LOG"; }

if [[ -f "$GCDUMP_FILE" ]]; then
  echo "[OK] GC dump saved to $GCDUMP_FILE" | tee -a "$LOG"
fi

# --- Step 4: Memory dump ---
if [[ "$SKIP_DUMP" == false ]]; then
  echo "" | tee -a "$LOG"
  echo "=== Step 4: Collecting heap dump ===" | tee -a "$LOG"
  DUMP_FILE="$OUTPUT_DIR/heap_dump.dmp"
  dotnet-dump collect \
    --process-id "$PID" \
    --type Heap \
    --output "$DUMP_FILE" \
    2>>"$LOG" || { echo "[WARN] Dump collection failed" | tee -a "$LOG"; }

  if [[ -f "$DUMP_FILE" ]]; then
    echo "[OK] Heap dump saved to $DUMP_FILE" | tee -a "$LOG"

    # macOS ARM64 has limited SOS command support in dotnet-dump analyze
    if [[ "$OS" == "Darwin" && "$ARCH" == "arm64" ]]; then
      echo "[WARN] macOS ARM64 detected — dotnet-dump analyze SOS commands have limited support." | tee -a "$LOG"
      echo "[WARN] Some analysis commands may fail or produce incomplete output." | tee -a "$LOG"
      echo "[HINT] For full analysis, transfer the .dmp file to a Linux or Windows machine," | tee -a "$LOG"
      echo "       or open in Visual Studio on Windows." | tee -a "$LOG"
    fi

    # Auto-analyze: top objects by size
    echo "" | tee -a "$LOG"
    echo "=== Auto-analysis: Top heap objects ===" | tee -a "$LOG"
    dotnet-dump analyze "$DUMP_FILE" -c "dumpheap -stat" \
      > "$OUTPUT_DIR/heap_stat.txt" 2>>"$LOG" || { echo "[WARN] dumpheap -stat failed (may be unsupported on this platform)" | tee -a "$LOG"; }
    if [[ -s "$OUTPUT_DIR/heap_stat.txt" ]]; then
      echo "[OK] Heap stats saved to $OUTPUT_DIR/heap_stat.txt" | tee -a "$LOG"
    fi

    # Finalizer queue
    dotnet-dump analyze "$DUMP_FILE" -c "finalizequeue" \
      > "$OUTPUT_DIR/finalizer_queue.txt" 2>>"$LOG" || { echo "[WARN] finalizequeue failed (may be unsupported on this platform)" | tee -a "$LOG"; }
    if [[ -s "$OUTPUT_DIR/finalizer_queue.txt" ]]; then
      echo "[OK] Finalizer queue saved to $OUTPUT_DIR/finalizer_queue.txt" | tee -a "$LOG"
    fi

    # Thread info
    dotnet-dump analyze "$DUMP_FILE" -c "clrthreads" \
      > "$OUTPUT_DIR/threads.txt" 2>>"$LOG" || { echo "[WARN] clrthreads failed (may be unsupported on this platform)" | tee -a "$LOG"; }
    if [[ -s "$OUTPUT_DIR/threads.txt" ]]; then
      echo "[OK] Thread info saved to $OUTPUT_DIR/threads.txt" | tee -a "$LOG"
    fi

    # Sync blocks (lock contention)
    dotnet-dump analyze "$DUMP_FILE" -c "syncblk" \
      > "$OUTPUT_DIR/syncblk.txt" 2>>"$LOG" || { echo "[WARN] syncblk failed (may be unsupported on this platform)" | tee -a "$LOG"; }
    if [[ -s "$OUTPUT_DIR/syncblk.txt" ]]; then
      echo "[OK] Sync block info saved to $OUTPUT_DIR/syncblk.txt" | tee -a "$LOG"
    fi
  fi
else
  echo "" | tee -a "$LOG"
  echo "=== Step 4: Skipped (--skip-dump) ===" | tee -a "$LOG"
fi

# --- Summary ---
echo "" | tee -a "$LOG"
echo "=========================================" | tee -a "$LOG"
echo "=== Collection Complete ===" | tee -a "$LOG"
echo "=========================================" | tee -a "$LOG"
echo "Results directory: $OUTPUT_DIR" | tee -a "$LOG"
echo "" | tee -a "$LOG"
echo "Files collected:" | tee -a "$LOG"
ls -lh "$OUTPUT_DIR"/ 2>/dev/null | tee -a "$LOG"
echo "" | tee -a "$LOG"
echo "Next steps:" | tee -a "$LOG"
echo "  1. Review counters.csv for runtime anomalies" | tee -a "$LOG"
echo "  2. Open .speedscope.json at https://www.speedscope.app for CPU profile" | tee -a "$LOG"
echo "  3. Open .gcdump in Visual Studio for heap analysis" | tee -a "$LOG"
echo "  4. Run 'dotnet-dump analyze heap_dump.dmp' for interactive memory analysis" | tee -a "$LOG"
echo "Finished: $(iso_timestamp)" | tee -a "$LOG"
