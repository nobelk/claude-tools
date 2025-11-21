# Refactoring Analysis Command for Code Improvement
# Usage: Analyze code for refactoring opportunities: <FILE_PATH|DIRECTORY|CLASS_NAME>

# Parse and validate the target identifier
Set TARGET to $Arguments
Validate that TARGET is provided, otherwise error "Please provide a file path, directory, or class name to analyze"

# Step 1: Code Analysis
## Identify refactoring opportunities
- Analyze code complexity using cyclomatic complexity metrics
- Detect code smells (long methods, large classes, feature envy, data clumps)
- Identify duplicate code blocks and similar patterns
- Review coupling and cohesion metrics
- Assess adherence to SOLID principles

# Step 2: Categorize Refactoring Opportunities
## CRITICAL (Immediate refactoring needed)
- God classes with excessive responsibilities
- Methods with high cyclomatic complexity (>15)
- Critical code duplication
- Tight coupling between unrelated modules

## HIGH (Should refactor soon)
- Long parameter lists (>5 parameters)
- Feature envy patterns
- Switch statement patterns that should be polymorphic
- Data clumps that should be objects

# Step 3: Generate Refactoring Plan
- Provide step-by-step refactoring approach
- Include before/after code examples
- Suggest design patterns to apply
- Estimate effort and risk levels
- Recommend testing strategy during refactoring
