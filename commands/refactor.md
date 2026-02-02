# Refactoring Analysis Command for Code Improvement
# Usage: Analyze code for refactoring opportunities: <FILE_PATH|DIRECTORY|CLASS_NAME>

# Parse and validate the target identifier
Set TARGET to $Arguments
Validate that TARGET is provided, otherwise error "Please provide a file path, directory, or class name to analyze"

# Step 1: Initial Code Scan
Execute these analyses in parallel:
- Calculate cyclomatic complexity for each method
- Measure lines of code per method/class
- Count method parameters
- Identify class dependencies and coupling
- Map inheritance hierarchies

# Step 2: Code Smell Detection

### Bloaters (Code that has grown too large)
- **Long Method**: Methods > 20 lines or cyclomatic complexity > 10
- **Large Class**: Classes with > 10 methods or > 300 lines
- **Long Parameter List**: Methods with > 4 parameters
- **Data Clumps**: Groups of data appearing together repeatedly
- **Primitive Obsession**: Overuse of primitives instead of objects

### Object-Orientation Abusers
- **Switch Statements**: Complex switch/case that should be polymorphic
- **Parallel Inheritance**: Subclass in one hierarchy requires subclass in another
- **Refused Bequest**: Subclass uses little of parent's behavior
- **Alternative Classes**: Different classes with similar interfaces

### Change Preventers
- **Divergent Change**: One class changed for multiple unrelated reasons
- **Shotgun Surgery**: Single change requires edits in many classes
- **Parallel Inheritance Hierarchies**: Adding subclass requires adding to another hierarchy

### Dispensables
- **Dead Code**: Unreachable or unused code
- **Speculative Generality**: Unused abstractions "for the future"
- **Duplicate Code**: Identical or very similar code blocks
- **Lazy Class**: Classes that don't do enough to justify existence
- **Data Class**: Classes with only fields and getters/setters

### Couplers
- **Feature Envy**: Method uses another class's data more than its own
- **Inappropriate Intimacy**: Classes too dependent on each other's internals
- **Message Chains**: Long chains of method calls (a.b().c().d())
- **Middle Man**: Class delegates most work to another class

# Step 3: SOLID Principles Assessment

### Single Responsibility (SRP)
- Does each class have one reason to change?
- Are concerns properly separated?

### Open/Closed (OCP)
- Can behavior be extended without modification?
- Are extension points identified?

### Liskov Substitution (LSP)
- Can subclasses substitute for base classes?
- Are contracts maintained?

### Interface Segregation (ISP)
- Are interfaces focused and cohesive?
- Are clients forced to depend on unused methods?

### Dependency Inversion (DIP)
- Do high-level modules depend on abstractions?
- Are dependencies injectable?

# Step 4: Categorize Refactoring Opportunities

## CRITICAL (Immediate refactoring needed)
- God classes with > 20 responsibilities
- Methods with cyclomatic complexity > 15
- Duplicate code blocks > 10 lines appearing 3+ times
- Circular dependencies between modules
- Tight coupling preventing unit testing

## HIGH (Should refactor soon)
- Long parameter lists (> 5 parameters)
- Feature envy patterns
- Switch statements that should be polymorphic
- Data clumps that should be value objects
- Methods > 50 lines

## MEDIUM (Consider refactoring)
- Minor code duplication (< 10 lines)
- Slightly long methods (20-50 lines)
- Missing interface abstractions
- Shallow inheritance that could use composition
- Inconsistent naming conventions

## LOW (Nice to have)
- Minor formatting inconsistencies
- Overly verbose code that could be simplified
- Opportunities for more expressive naming
- Documentation improvements

# Step 5: Suggest Design Patterns

For each identified issue, suggest applicable patterns:
- **Strategy**: Replace conditional logic with polymorphism
- **Factory**: Centralize object creation
- **Builder**: Simplify complex object construction
- **Decorator**: Add behavior without inheritance
- **Facade**: Simplify complex subsystem interfaces
- **Observer**: Decouple event producers from consumers
- **Template Method**: Define algorithm skeleton with customizable steps
- **Command**: Encapsulate requests as objects

# Step 6: Generate Output

## Output Format

### Refactoring Analysis Summary
**Target**: [File/Directory/Class analyzed]
**Analysis Date**: [Date]
**Overall Code Health**: [Good/Fair/Poor]
**Technical Debt Score**: [1-10, where 10 is worst]

### Executive Summary
[2-3 paragraphs on code quality, main concerns, and recommended priorities]

### Code Metrics
| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Avg Cyclomatic Complexity | [X] | < 10 | [OK/WARN/CRIT] |
| Max Method Length | [X] lines | < 50 | [OK/WARN/CRIT] |
| Avg Class Size | [X] lines | < 300 | [OK/WARN/CRIT] |
| Duplicate Code | [X]% | < 5% | [OK/WARN/CRIT] |

### Refactoring Inventory
| ID | Smell | Severity | Location | Suggested Pattern |
|----|-------|----------|----------|-------------------|
| R1 | [Code smell] | [CRIT/HIGH/MED/LOW] | [file:line] | [Pattern/Technique] |

### Detailed Findings

#### [R1] [Issue Title]
- **Code Smell**: [Type of smell]
- **Severity**: [CRITICAL/HIGH/MEDIUM/LOW]
- **Location**: `[file:line]`
- **Description**: [Why this is a problem]
- **SOLID Violation**: [If applicable, which principle]

**Before**:
```
[current problematic code]
```

**After**:
```
[refactored code]
```

**Refactoring Steps**:
1. [Step-by-step guide]
2. [How to safely make the change]
3. [What tests to run]

**Risk Level**: [Low/Medium/High]
**Estimated Effort**: [Small/Medium/Large]

### Refactoring Roadmap
1. **Immediate** (This sprint): [List critical items]
2. **Short-term** (Next sprint): [List high items]
3. **Medium-term** (Backlog): [List medium items]

### Testing Strategy During Refactoring
- Tests to write before refactoring
- Tests to verify refactoring success
- Regression testing approach

### Dependencies
[List any blockers or dependencies between refactoring tasks]
