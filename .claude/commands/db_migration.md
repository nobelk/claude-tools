# Database Migration Analysis Command
# Usage: Analyze database schema changes for migration safety: <MIGRATION_FILE|SCHEMA_DIFF>

# Parse migration target
Set MIGRATION_TARGET to $Arguments
Validate that MIGRATION_TARGET is provided, otherwise error "Please provide migration file or schema diff"

# Step 1: Migration Analysis
## Analyze schema changes
- Identify breaking changes (column drops, type changes)
- Check for data loss risks
- Analyze index and constraint impacts
- Review foreign key dependencies
- Assess performance implications of changes

# Step 2: Risk Assessment
## CRITICAL RISKS (Require immediate attention)
- Data loss operations without backup strategy
- Breaking changes affecting existing queries
- Performance degradation on large tables

# Step 3: Generate Migration Strategy
- Provide safe migration steps
- Suggest rollback procedures
- Recommend data backup strategies
- Include performance optimization suggestions
- Generate validation queries
