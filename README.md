# Claude Commands for Software Engineering

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

A curated collection of Claude Code slash commands designed to streamline software engineering workflows. These commands leverage Claude's advanced capabilities to provide automated code analysis, design reviews, debugging assistance, and comprehensive documentation generation.

## Installation

1. **Clone or download this repository**:
   ```bash
   git clone https://github.com/yourusername/claude-commands.git
   ```

2. **Copy commands to your project** (Option A - Recommended):
   ```bash
   # Copy the entire .claude/commands directory to your project
   cp -r claude-commands/.claude/commands /path/to/your/project/.claude/
   ```

3. **Or use as a global command library** (Option B):
   ```bash
   # Link this repository to Claude Code's global commands directory
   # (Refer to Claude Code documentation for global command setup)
   ```

4. **Verify installation**:
   - Open your project in Claude Code
   - Type `/` to see available commands
   - Your installed commands should appear in the list

## Available Commands

### 📋 Code Review & Quality

#### `/code_review` - Pull Request Analysis
**File**: [`.claude/commands/code_review.md`](.claude/commands/code_review.md)

Performs comprehensive PR analysis against software engineering best practices including SOLID principles and GoF design patterns.

**Usage**:
```bash
/code_review <pr-number|pr-url|branch-name>
```

**Key Features**:
- Multi-dimensional analysis (quality, security, performance, tests)
- SOLID principles and design pattern evaluation
- Prioritized findings (CRITICAL/HIGH/MEDIUM/LOW)
- Before/after code examples for improvements
- Test coverage gap identification

---

#### `/refactor` - Refactoring Opportunities
**File**: [`.claude/commands/refactor.md`](.claude/commands/refactor.md)

Identifies code smells and refactoring opportunities using complexity metrics and design principles.

**Usage**:
```bash
/refactor <file-path|directory|class-name>
```

**Key Features**:
- Cyclomatic complexity analysis
- Code smell detection (god classes, long methods, feature envy)
- Duplicate code identification
- SOLID principles assessment
- Step-by-step refactoring plans with design pattern suggestions

---

### 🔒 Security & Performance

#### `/security_scan` - Vulnerability Detection
**File**: [`.claude/commands/security_scan.md`](.claude/commands/security_scan.md)

Scans codebase for security vulnerabilities based on OWASP Top 10 and security best practices.

**Usage**:
```bash
/security_scan <directory|file-pattern>
```

**Key Features**:
- OWASP Top 10 vulnerability detection
- Authentication and authorization flaw identification
- Cryptographic implementation analysis
- Dependency vulnerability scanning
- Prioritized security issues with remediation guidance

---

#### `/perf_analysis` - Performance Profiling
**File**: [`.claude/commands/perf_analysis.md`](.claude/commands/perf_analysis.md)

Analyzes application performance bottlenecks and provides optimization recommendations.

**Usage**:
```bash
/perf_analysis <profiling-data|log-file|class-name>
```

**Key Features**:
- CPU and memory bottleneck identification
- Database query optimization (N+1 detection)
- Caching opportunity analysis
- Algorithm efficiency review
- Before/after performance metrics

---

### 🐛 Debugging & Analysis

#### `/rca` - Root Cause Analysis
**File**: [`.claude/commands/rca.md`](.claude/commands/rca.md)

Analyzes exceptions and stack traces to identify root causes and generate comprehensive fixes with unit tests.

**Usage**:
```bash
# First, save your stack trace to a file (e.g., exceptions.txt)
/rca @exceptions.txt
```

**Key Features**:
- Exception parsing and call chain analysis
- Framework-specific issue identification (Spring Boot, JPA, etc.)
- Root cause identification vs symptom fixes
- Comprehensive code fixes with file paths and line numbers
- Unit test generation for reproduction and validation

---

### 🗄️ Database & Migration

#### `/db_migration` - Migration Safety Analysis
**File**: [`.claude/commands/db_migration.md`](.claude/commands/db_migration.md)

Analyzes database schema changes for migration safety and potential risks.

**Usage**:
```bash
/db_migration <migration-file|schema-diff>
```

**Key Features**:
- Breaking change identification
- Data loss risk assessment
- Performance impact analysis
- Safe migration strategy generation
- Rollback procedure recommendations

---

### 📐 Design & Architecture

#### `/design-doc` - Design Document Generation
**File**: [`.claude/commands/design-doc.md`](.claude/commands/design-doc.md)

Generates comprehensive developer design documents from product and business requirement documents.

**Usage**:
```bash
/design-doc <path/to/prd.md> <path/to/brd.md>
```

**Key Features**:
- Requirements analysis and traceability
- System architecture and component design
- API specifications and data models
- Testing strategy and quality requirements
- Task breakdown with priorities and dependencies
- Risk assessment and mitigation strategies

---

#### `/design_review` - Design Document Review
**File**: [`.claude/commands/design_review.md`](.claude/commands/design_review.md)

Conducts FAANG-level comprehensive design document reviews with Principal Engineer rigor.

**Usage**:
```bash
/design_review <design-doc-path>
```

**Key Features**:
- PRD alignment and requirements coverage verification
- Architecture pattern evaluation (SOLID, GoF patterns)
- Security analysis (OWASP, threat modeling)
- Scalability and performance assessment
- Operational readiness review
- Prioritized issues with actionable recommendations

---

### 📚 Documentation & Onboarding

#### `/onboard` - Codebase Onboarding
**File**: [`.claude/commands/onboard.md`](.claude/commands/onboard.md)

Generates comprehensive onboarding documentation for new developers joining the codebase.

**Usage**:
```bash
/onboard
```

**Key Features**:
- Deep codebase analysis with architecture diagrams
- Technology stack documentation
- Key concepts and design patterns identification
- Development workflow setup instructions
- Prioritized issues and improvement opportunities
- Concise, actionable onboarding guide (1-2 pages)

---

### 💼 Additional Tools

#### `/dd_startup` - Startup Evaluation
**File**: [`.claude/commands/dd_startup.md`](.claude/commands/dd_startup.md)

Comprehensive startup company analysis for job seekers conducting due diligence.

**Usage**:
```bash
# Edit the file to add company information, then run:
/dd_startup
```

**Key Features**:
- Financial stability and funding analysis
- Founder and leadership team evaluation
- Product-market fit assessment
- Growth potential and career opportunity analysis
- Risk matrix and SWOT analysis
- Interview questions based on identified gaps

---

## Command Structure

All commands follow a consistent, systematic approach:

1. **Input Validation**: Ensures required parameters and context are available
2. **Context Gathering**: Collects relevant information from codebase, git history, or documentation
3. **Systematic Analysis**: Applies domain expertise and best practices
4. **Structured Output**: Provides prioritized, actionable recommendations
5. **Verification**: Includes validation steps and success criteria

## Benefits

- **⚡ Productivity**: Automate time-consuming analysis and documentation tasks
- **🎯 Consistency**: Standardized analysis approaches across all scenarios
- **📊 Thoroughness**: Comprehensive coverage of quality, security, and performance dimensions
- **✅ Actionability**: Prioritized recommendations with specific code examples
- **🤝 Collaboration**: Structured outputs perfect for team reviews and discussions
- **📚 Best Practices**: Incorporates industry standards and framework-specific expertise

## Usage Tips

1. **File References**: Use `@filename` to reference files in your prompts (e.g., `/rca @exceptions.txt`)
2. **Combine Commands**: Use multiple commands in sequence for comprehensive analysis
3. **Customize**: Edit command files to adapt them to your team's specific needs
4. **Iterate**: Commands are designed for iterative refinement based on initial output

## Repository Structure

```
claude-commands/
├── .claude/
│   └── commands/          # Slash commands for Claude Code
│       ├── code_review.md
│       ├── db_migration.md
│       ├── design-doc.md
│       ├── design_review.md
│       ├── onboard.md
│       ├── perf_analysis.md
│       ├── rca.md
│       ├── refactor.md
│       ├── security_scan.md
│       └── dd_startup.md
├── prompts/               # Reusable prompt templates
│   ├── analyze_paper.md
│   └── design_document.md
├── LICENSE
└── README.md
```

## Contributing

We welcome contributions! When adding new commands:

1. **Follow the structure**: Use the established format and style
2. **Be comprehensive**: Include detailed analysis steps and examples
3. **Provide clear usage**: Document parameters, usage patterns, and expected outputs
4. **Test thoroughly**: Validate commands with real-world scenarios
5. **Update README**: Add documentation for new commands to this file
6. **Include examples**: Show sample inputs and outputs where helpful

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/yourusername/claude-commands/issues)
- **Documentation**: See [Claude Code documentation](https://docs.anthropic.com/claude/docs) for platform details
- **Community**: Share your custom commands and improvements!

---

**Made with ❤️ for the engineering community**
