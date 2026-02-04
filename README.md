# Claude Code Skills & Prompts

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

A curated collection of Claude Code skills and prompt templates designed to streamline software engineering workflows. These skills leverage Claude's advanced capabilities to provide automated code analysis, design reviews, security scanning, and comprehensive documentation generation.

## Installation

1. **Clone or download this repository**:
   ```bash
   git clone https://github.com/yourusername/claude-tools.git
   ```

2. **Copy skills to your Claude Code settings** (Option A - Per Project):
   ```bash
   # Copy the skills directory to your project
   cp -r claude-tools/skills /path/to/your/project/.claude/
   ```

3. **Or use as a global skills library** (Option B):
   ```bash
   # Copy to your global Claude Code directory
   cp -r claude-tools/skills ~/.claude/
   ```

4. **Verify installation**:
   - Open your project in Claude Code
   - The skills should be available based on context triggers or explicit invocation

## Available Skills

### Code Review & Quality

#### `code-review` - Pull Request Analysis
**Directory**: [`skills/code-review/`](skills/code-review/)

Performs senior-engineer-grade PR code reviews covering correctness, security, performance, testing, design, and observability.

**Triggers**: Review a pull request, PR, merge request, diff, branch, or code changes

**Key Features**:
- Multi-dimensional analysis (correctness, security, performance, design)
- File prioritization by risk (P0-P4)
- Severity classification (CRITICAL/HIGH/MEDIUM/LOW/PRAISE)
- Actionable recommendations with code suggestions

---

#### `codebase-review` - Codebase Audit
**Directory**: [`skills/codebase-review/`](skills/codebase-review/)

Performs a thorough codebase review and produces a prioritized `to_do.md` listing all bug fixes, improvements, and action items.

**Triggers**: Review, audit, or analyze a codebase for bugs, code quality issues, missing tests, TODOs, technical debt

**Key Features**:
- Systematic file-by-file review
- Bug detection (logical, security, performance)
- Test coverage gap identification
- .NET/C#-specific checks included
- Prioritized action item list

---

#### `dotnet-refactor` - .NET Refactoring
**Directory**: [`skills/dotnet-refactor/`](skills/dotnet-refactor/)

Principal-level C#/.NET codebase refactoring with phased plans and regression safety.

**Triggers**: Refactor, restructure, clean up, or improve C#/.NET code quality

**Key Features**:
- Discovery of code smells and coupling hotspots
- Baseline unit test safety net
- Phased refactoring plan generation
- SOLID principles and design pattern guidance
- Logging and cross-cutting concern improvements

---

### Security & Performance

#### `security-scan` - Vulnerability Detection
**Directory**: [`skills/security-scan/`](skills/security-scan/)

Comprehensive security vulnerability assessment aligned with OWASP, CWE, and CVSS standards.

**Triggers**: Scan code for security issues, perform security review/audit, find vulnerabilities, check for OWASP Top 10 issues

**Key Features**:
- OWASP Top 10 vulnerability detection
- Multi-language support (JS/TS, Python, Java, Go, C/C++, Ruby, PHP, C#, Rust, Swift, Kotlin)
- Automated pattern scanning with manual deep-dive
- Dependency audit for known CVEs
- CVSS-aligned severity classification

---

#### `performance-analysis` - Performance Profiling
**Directory**: [`skills/performance-analysis/`](skills/performance-analysis/)

Analyzes application performance bottlenecks with focus on .NET diagnostics.

**Triggers**: Performance analysis, profiling, optimization recommendations

**Key Features**:
- Anti-pattern detection
- .NET-specific diagnostics
- Structured output template
- Actionable optimization recommendations

---

### Architecture & Design

#### `architecture-review` - Architecture Analysis
**Directory**: [`skills/architecture-review/`](skills/architecture-review/)

Generates industry-standard architecture design documents by analyzing codebases across structure, patterns, principles, and quality attributes.

**Triggers**: Review or analyze code architecture, create architecture overview, assess code quality, identify architectural strengths/weaknesses

**Key Features**:
- Systematic codebase exploration
- Design pattern identification (creational, structural, behavioral, architectural)
- Clean code principles assessment (SOLID, DRY, KISS, YAGNI)
- Quality attribute ratings (1-5 scale)
- Mermaid diagram generation

---

#### `design-doc-review` - Design Document Review
**Directory**: [`skills/design-doc-review/`](skills/design-doc-review/)

Principal-engineer-level design document review against PRD requirements.

**Triggers**: Review, critique, or evaluate a design document, technical design, architecture proposal

**Key Features**:
- PRD alignment verification
- 11 review dimensions (architecture, security, scalability, availability, etc.)
- Severity-based issue classification (P0-P3)
- Actionable recommendations

---

#### `prd-to-design-doc` - PRD to Design Document
**Directory**: [`skills/prd-to-design-doc/`](skills/prd-to-design-doc/)

Transforms Product Requirements Documents into Developer Design Documents following RFC conventions used by Google, Uber, Airbnb, Stripe, and others.

**Triggers**: Create a design document from a PRD, generate an RFC, create technical design doc

**Key Features**:
- Trade-off focused analysis
- Alternatives considered with comparison
- Cross-cutting concerns (security, privacy, observability)
- Phased rollout planning
- Mermaid architecture diagrams

---

### Documentation & Requirements

#### `prd-generator` / `code-to-prd-doc` - PRD from Codebase
**Directory**: [`skills/prd-generator/`](skills/prd-generator/) | [`skills/code-to-prd-doc/`](skills/code-to-prd-doc/)

Reverse-engineers a codebase into a formal Product Requirements Document structured for Jira work item creation.

**Triggers**: Generate PRD, analyze codebase, document requirements, reverse-engineer features, prepare Jira epics from code

**Key Features**:
- Feature extraction by category
- Gap and technical debt identification
- Jira-ready epic/story/task breakdown
- .NET/C# specific analysis patterns
- Fibonacci story point estimation

---

### Testing & Bug Fixing

#### `tdd-bugfix` - Test-Driven Bug Fixing
**Directory**: [`skills/tdd-bugfix/`](skills/tdd-bugfix/)

Fixes bugs using test-driven development methodology with strict adherence to project conventions.

**Triggers**: Fix a bug using TDD, safe bug fix with tests

**Key Features**:
- Project convention discovery
- Failing test creation before fix
- Project test framework/style matching
- Full regression test verification

---

#### `qa-test-plan-review` - Railway QA Test Plan Review
**Directory**: [`skills/qa-test-plan-review/`](skills/qa-test-plan-review/)

Railway QA Lead Engineer skill for reviewing test plans against CENELEC EN 50716/EN 50128, EN 50126, and EN 50129 standards.

**Triggers**: Railway test plan review, CENELEC compliance testing, signaling test coverage, safety-critical test case generation

**Key Features**:
- SIL-graded requirement analysis
- Gap analysis against railway standards
- CSV test case generation matching input format
- Safety/fail-safe scenario coverage

---

### Utilities

#### `git-rebase-main` - Git Rebase Helper
**Directory**: [`skills/git-rebase-main/`](skills/git-rebase-main/)

Fetches and rebases current branch onto main/master with automatic stash handling.

**Triggers**: Update branch with main, sync with default branch, pull and rebase

**Key Features**:
- Auto-detects main vs master
- Automatic stash/unstash via `--autostash`
- Conflict resolution guidance

---

#### `keybindings-help` - Keyboard Shortcuts Help
**Directory**: [`skills/keybindings-help/`](skills/keybindings-help/)

Helps customize Claude Code keyboard shortcuts by editing `~/.claude/keybindings.json`.

**Triggers**: Rebind keys, add chord bindings, customize keybindings, change submit key

**Key Features**:
- Complete keybindings.json reference
- All contexts and actions documented
- Chord binding support
- Common customization examples

---

## Prompt Templates

Reusable prompt templates in the `prompts/` directory:

| File | Purpose |
|------|---------|
| [`analyze_paper.md`](prompts/analyze_paper.md) | Academic paper analysis template |
| [`architecture_analysis.md`](prompts/architecture_analysis.md) | Comprehensive codebase architecture review |
| [`design_document.md`](prompts/design_document.md) | Design document generation template |
| [`engineering_brief.md`](prompts/engineering_brief.md) | Daily engineering brief from Jira data |

---

## Repository Structure

```
claude-tools/
├── skills/                          # Claude Code skills
│   ├── architecture-review/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── code-review/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── code-to-prd-doc/
│   │   ├── SKILL.md
│   │   ├── assets/
│   │   └── references/
│   ├── codebase-review/
│   │   └── SKILL.md
│   ├── design-doc-review/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── dotnet-refactor/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── git-rebase-main/
│   │   ├── SKILL.md
│   │   └── scripts/
│   ├── keybindings-help/
│   │   └── SKILL.md
│   ├── performance-analysis/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   └── scripts/
│   ├── prd-generator/
│   │   ├── SKILL.md
│   │   ├── assets/
│   │   └── references/
│   ├── prd-to-design-doc/
│   │   └── SKILL.md
│   ├── qa-test-plan-review/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── security-scan/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   └── scripts/
│   └── tdd-bugfix/
│       └── SKILL.md
├── prompts/                         # Reusable prompt templates
│   ├── analyze_paper.md
│   ├── architecture_analysis.md
│   ├── design_document.md
│   └── engineering_brief.md
├── workflow/                        # Workflow documentation & assets
├── LICENSE
└── README.md
```

## Skill Structure

Each skill follows a consistent structure:

```
skill-name/
├── SKILL.md          # Main skill definition with frontmatter and workflow
├── references/       # Supporting documentation and checklists
├── assets/           # Templates and output formats
└── scripts/          # Automation scripts (if applicable)
```

The `SKILL.md` file contains:
- **Frontmatter**: Name, description, and trigger conditions
- **Workflow**: Step-by-step execution process
- **References**: Links to supporting materials

## Benefits

- **Productivity**: Automate time-consuming analysis and documentation tasks
- **Consistency**: Standardized analysis approaches across all scenarios
- **Thoroughness**: Comprehensive coverage of quality, security, and performance dimensions
- **Actionability**: Prioritized recommendations with specific code examples
- **Collaboration**: Structured outputs perfect for team reviews and discussions
- **Best Practices**: Incorporates industry standards (OWASP, SOLID, CENELEC, etc.)

## Usage Tips

1. **Context Triggers**: Skills activate automatically based on your request context
2. **Reference Files**: Skills use supporting references for comprehensive analysis
3. **Customization**: Edit SKILL.md files to adapt to your team's specific needs
4. **Iteration**: Skills are designed for iterative refinement based on initial output
5. **Headless/CI Automation**: Run the full agentic workflow non-interactively.

```bash
# Run the full workflow non-interactively
claude -p "
  Implement rate limiting middleware on the ASP.NET Core API using
  System.Threading.RateLimiting. Apply a fixed-window policy of
  100 requests per minute per client IP on all /api/* endpoints.
  Follow this workflow:
  1. Use software-architect agent to produce implementation plan.
  2. Use principal-engineer agent to review plan and implement with tests.
  3. Use code-reviewer agent to review and fix all issues. If BLOCKED,
     use principal-engineer to rework, then re-run code-reviewer.
  4. Use test-runner agent to run all four test tiers.
  5. If any tier fails, use principal-engineer to fix, then code-reviewer
     to verify, then test-runner to re-test. Repeat until green.
  Print WORKFLOW_SUCCESS if everything passes, WORKFLOW_FAILED otherwise.
" --allowedTools "Read,Write,Edit,Bash,Grep,Glob,MultiEdit" --output-format json

```

## Multiagent Workflow Prompt

> I need to add rate limiting middleware to the ASP.NET Core API using
  the built-in System.Threading.RateLimiting. Apply a fixed-window
  policy of 100 requests per minute per client IP on all /api/* endpoints.
  Please follow this workflow:
  1. Use the software-architect agent to analyze the codebase and produce
     a detailed implementation plan with unit test strategy.
  2. Use the principal-engineer agent to review and refine the plan, then
     implement the code changes with unit tests. Unit tests must pass.
  3. Use the code-reviewer agent to review the implementation and fix any
     issues directly. Build and unit tests must pass after fixes.
     If the verdict is BLOCKED, use the principal-engineer agent to rework
     the implementation, then re-run the code-reviewer agent.
  4. Use the test-runner agent to run all four test tiers (unit, functional,
     integration, pact).
  5. If any tests fail due to the change, use the principal-engineer agent
     to fix them, then the code-reviewer agent to verify the fixes, then
     re-run the test-runner agent. Repeat until all tiers pass.
  6. Summarize the final result.




## Contributing

We welcome contributions! When adding new skills:

1. **Follow the structure**: Use the established SKILL.md format with frontmatter
2. **Be comprehensive**: Include detailed workflow steps and references
3. **Provide clear triggers**: Document what user requests activate the skill
4. **Include references**: Add supporting documentation in a `references/` subdirectory
5. **Test thoroughly**: Validate skills with real-world scenarios
6. **Update README**: Add documentation for new skills to this file

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/yourusername/claude-tools/issues)
- **Documentation**: See [Claude Code documentation](https://docs.anthropic.com/claude/docs) for platform details
- **Community**: Share your custom skills and improvements!

---

**Made for the engineering community**
