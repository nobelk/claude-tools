# Railway Software Testing Standards Reference

Load this file during Phase 3 (Gap Analysis). It contains the normative test techniques, SIL-graded requirements, and safety analysis methods derived from the CENELEC EN 5012x family and related standards.

## Governing Standards Hierarchy

The railway CENELEC standards are derived from IEC 61508 (Functional Safety of E/E/PE systems):

- **EN 50126** (IEC 62278) — RAMS lifecycle for the entire system (hardware + software + human). Defines the V-model process. Two parts: Part 1 = generic RAMS process; Part 2 = systems approach to safety.
- **EN 50716:2023** — Supersedes both EN 50128:2011 and EN 50657:2017 as of November 2023. Single framework for all railway software (signaling, control, protection, AND rolling stock). Defines software lifecycle, test techniques, tool qualification (T1/T2/T3), and SIL-graded requirements.
- **EN 50128:2011** (IEC 62279) — Predecessor standard for software in railway control and protection. Still referenced in legacy projects.
- **EN 50129** — Safety case for safety-related electronic systems for signaling. Covers system architecture, hardware failures, and Safety Case evidence.
- **EN 50657:2017** — Predecessor for rolling stock software. Now merged into EN 50716.
- **CLC/TS 50701** — Railway cybersecurity standard (published June 2021).

## Safety Integrity Levels (SIL)

SIL is assigned per EN 50129 based on hazard severity and frequency:

| SIL | Meaning | Typical Application |
|-----|---------|---------------------|
| Basic Integrity | Non-safety-related (replaces SIL 0 in EN 50716) | Passenger information, non-critical logging |
| SIL 1 | Low safety relevance | Door control interlocks, HVAC safety cutoffs |
| SIL 2 | Medium safety relevance | Speed monitoring, platform screen doors |
| SIL 3 | High safety relevance | ATP supervision, level crossing control |
| SIL 4 | Highest safety relevance | Interlocking logic, vital signaling, ATP intervention |

## EN 50716 / EN 50128 Test Technique Requirements by SIL

The standard defines techniques as M (Mandatory), HR (Highly Recommended), R (Recommended), or — (No recommendation). The test plan must cover all M and HR techniques for the target SIL, and should cover R techniques.

### Functional / Black-Box Test Techniques (derived from Table A.13 / A.14 of EN 50716)

| Technique | Basic | SIL 1 | SIL 2 | SIL 3 | SIL 4 |
|-----------|-------|-------|-------|-------|-------|
| Equivalence classes & input partition | R | HR | HR | HR | HR |
| Boundary value analysis | R | HR | HR | HR | HR |
| Cause-effect diagrams / decision tables | — | R | R | HR | HR |
| Error guessing / error seeding | R | R | R | R | R |
| Process simulation | — | R | R | R | R |
| Prototyping / animation | R | R | R | R | R |
| Avalanche / stress testing | R | R | R | HR | HR |
| Performance requirements testing | R | R | HR | HR | HR |
| Interface testing | R | HR | HR | HR | HR |
| State transition testing | — | R | R | HR | HR |

### Structure-Based / White-Box Test Coverage (Table A.21 of EN 50716)

| Coverage Metric | Basic | SIL 1 | SIL 2 | SIL 3 | SIL 4 |
|-----------------|-------|-------|-------|-------|-------|
| Statement coverage | R | HR | HR | HR | HR |
| Branch coverage | — | R | R | HR | HR |
| Compound condition coverage | — | — | R | HR | HR |
| Data flow analysis | — | R | R | HR | HR |
| Path coverage | — | — | R | R | R |

For SIL 3/4 at component level: Branches AND compound conditions, OR Branches AND data flow, OR Path coverage.

### Software Assurance Activities (Clause 6 of EN 50716)

| Activity | Basic | SIL 1 | SIL 2 | SIL 3 | SIL 4 |
|----------|-------|-------|-------|-------|-------|
| Component testing | R | HR | HR | M | M |
| Integration testing | R | HR | HR | M | M |
| Final validation testing | R | M | M | M | M |
| Regression testing | R | HR | HR | M | M |
| Requirements traceability | R | HR | HR | M | M |

## Gap Analysis Checklists

### A. Functional Coverage (Black-Box)

For every stated requirement or function:
- [ ] At least one positive (happy-path) test exists
- [ ] At least one negative (error-handling / invalid input) test exists
- [ ] Equivalence partitions defined and each partition has ≥1 test
- [ ] Boundary values tested (min-1, min, min+1, nominal, max-1, max, max+1)
- [ ] Decision logic covered via decision table or cause-effect diagram
- [ ] All system states identified and state transitions tested (valid + invalid)
- [ ] Interface contracts between subsystems verified

### B. Boundary Conditions — Railway-Specific Parameters

Test boundary values for all applicable parameters below. For each parameter, generate tests at: below-minimum, minimum, typical, maximum, above-maximum.

**Speed thresholds**: Service speed limit, shunting speed limit, overspeed trigger, emergency brake trigger, crawl speed, zero-speed detection tolerance
**Distance thresholds**: Safe braking distance, overlap distance, approach locking distance, platform stopping accuracy tolerance, block section length
**Time thresholds**: Signal approach time, route release time, heartbeat timeout, communication polling interval, flashing frequency, door open/close time, emergency brake response time, route-setting timeout
**Temperature**: Operating range (e.g. -40°C to +70°C for trackside, -25°C to +55°C for onboard), de-rating thresholds
**Voltage / Power**: Nominal supply ±tolerance (e.g. 110V DC ±20%), undervoltage trip, overvoltage trip, brownout recovery, battery backup switchover
**Message / Telegram**: Maximum telegram length, sequence numbering wrap-around, CRC/checksum mismatch, telegram age/freshness, retransmission count limit

### C. Stress & Load Testing

| Scenario | What to Test |
|----------|-------------|
| Normal load | System at typical train density and message rate |
| Peak load | Maximum simultaneous train movements, route requests, signal changes |
| Stress (beyond peak) | 110%, 150%, 200% of peak capacity |
| Spike load | Sudden transition from idle to maximum load |
| Endurance / soak | Continuous operation at normal load for 24h, 72h, 7 days |
| Volume | Maximum track database size, route table entries, log file accumulation |
| Recovery under load | Failover / restart while processing peak load |
| Resource exhaustion | Memory full, disk full, connection pool drained, message queue overflow |
| Degraded mode | Partial infrastructure failure (lost redundant channel, fallback communication) |

### D. Railway Signaling & Safety Scenarios

Every rail software test plan must include scenarios for:

**Fail-safe behaviour**:
- [ ] System defaults to most restrictive state on any detected fault
- [ ] Loss of communication → signals to danger / trains held
- [ ] Watchdog timeout → safe shutdown initiated
- [ ] Vital output fail-safe: stuck relay, dark signal, point machine failure

**Interlocking logic** (if applicable):
- [ ] Route setting: all normal path conditions verified
- [ ] Route locking: conflicting routes rejected
- [ ] Route release: sequential / timed release after train passage
- [ ] Flank and overlap protection maintained
- [ ] Approach locking: route cannot be cancelled with train approaching
- [ ] Emergency route release under controlled conditions

**Train detection**:
- [ ] Track circuit: occupied, clear, failed (rail break, insulation fault)
- [ ] Axle counter: count-in, count-out, mismatch, reset procedure
- [ ] Train detection failure → restrictive fallback

**ATP/ATC**:
- [ ] Speed supervision: permitted speed, warning, intervention, service brake, emergency brake curves
- [ ] Movement authority: acknowledge, extend, shorten, revoke
- [ ] Override/staff responsible mode: entry, restrictions, exit
- [ ] Transition between control areas or levels
- [ ] Cold start / warm start of onboard unit with valid and expired data

**Communication**:
- [ ] Primary channel failure → fallback channel activation
- [ ] Dual-channel mismatch
- [ ] Message corruption / CRC failure → rejection and retransmission
- [ ] Session establishment, maintenance, termination
- [ ] Authentication and encryption handshake (per CLC/TS 50701 if applicable)

**Power and environment**:
- [ ] Primary power loss → UPS/battery switchover
- [ ] Power restoration and re-synchronization
- [ ] Voltage out of tolerance → graceful degradation
- [ ] EMI exposure within and beyond specified limits

### E. RAMS Verification (per EN 50126)

- [ ] **Reliability**: MTBF targets have test scenarios or are derived from component-level testing
- [ ] **Availability**: Failover time measured; system uptime targets verified via endurance tests
- [ ] **Maintainability**: Diagnostic self-test coverage verified; MTTR scenarios exercised
- [ ] **Safety**: All hazards from hazard log have corresponding test coverage; SIL targets met

### F. Safety Analysis Traceability

Verify the test plan traces back to safety analysis outputs:

- [ ] **FMEA/FMECA**: Every failure mode with RPN above threshold has a corresponding test
- [ ] **FTA**: Every minimal cut set has a test verifying mitigation
- [ ] **HAZOP**: Every identified deviation has a test for detection and safe response
- [ ] **Hazard Log**: Every hazard with mitigation "tested" or "verified by test" is covered

### G. Cybersecurity (per CLC/TS 50701)

- [ ] Authentication bypass attempts
- [ ] Unauthorized command injection
- [ ] Man-in-the-middle on communication links
- [ ] Replay attack on safety telegrams
- [ ] Denial of service on communication channels
- [ ] Firmware/software integrity verification at boot

### H. Regression & Compatibility

- [ ] All previously passed tests re-executed after modifications
- [ ] Backward compatibility with legacy systems at interfaces
- [ ] Multi-vendor interoperability at standardized interfaces (e.g. Eurobalise, RBC-to-RBC)
