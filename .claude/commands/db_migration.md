# Database Migration Analysis Command
# Usage: Analyze database schema changes for migration safety: <MIGRATION_FILE|SCHEMA_DIFF>

# Parse migration target
Set MIGRATION_TARGET to $Arguments
Validate that MIGRATION_TARGET is provided, otherwise error "Please provide migration file or schema diff"

# Step 1: Migration Discovery
Execute these analyses in parallel:
- Read and parse migration file(s)
- Identify the database type (PostgreSQL, MySQL, SQLite, etc.)
- Extract all DDL statements (CREATE, ALTER, DROP)
- Identify affected tables and columns
- Check for data manipulation (INSERT, UPDATE, DELETE)
- Review any stored procedures or triggers

# Step 2: Change Classification

### Schema Changes
- **Tables**: CREATE TABLE, DROP TABLE, RENAME TABLE
- **Columns**: ADD COLUMN, DROP COLUMN, MODIFY COLUMN, RENAME COLUMN
- **Indexes**: CREATE INDEX, DROP INDEX, CREATE UNIQUE INDEX
- **Constraints**: ADD CONSTRAINT, DROP CONSTRAINT (FK, PK, UNIQUE, CHECK)
- **Views**: CREATE VIEW, ALTER VIEW, DROP VIEW
- **Triggers**: CREATE TRIGGER, DROP TRIGGER

### Data Changes
- INSERT statements (seeding, backfilling)
- UPDATE statements (data transformation)
- DELETE statements (cleanup)

# Step 3: Risk Assessment

## CRITICAL RISKS (Require immediate attention)

### Data Loss Operations
- DROP TABLE without backup verification
- DROP COLUMN containing data
- TRUNCATE statements
- DELETE without WHERE clause

### Breaking Changes
- Column type changes that may lose data (VARCHAR(100) -> VARCHAR(50))
- NOT NULL constraints on columns with NULL values
- Removing columns used by application code
- Changing primary keys

### Performance Risks
- Adding indexes on large tables (table locks)
- ALTER TABLE on tables with millions of rows
- Missing indexes on new foreign keys
- Full table scans during migration

### Availability Risks
- Long-running migrations blocking writes
- Migrations requiring exclusive locks
- Downtime-requiring schema changes

## HIGH RISKS (Should address before deployment)
- Foreign key changes affecting multiple tables
- Index changes on frequently queried columns
- Enum/type modifications
- Default value changes

## MEDIUM RISKS (Monitor during deployment)
- Adding nullable columns
- Creating new indexes on small tables
- Adding new tables
- Creating views

## LOW RISKS (Standard changes)
- Adding columns with defaults
- Creating indexes on empty tables
- Documentation/comment changes

# Step 4: Compatibility Analysis

### Backward Compatibility Check
- Can the old application version work with new schema?
- Are there breaking API changes?
- Do existing queries still work?

### Forward Compatibility Check
- Can the new application version work with old schema?
- Is the migration reversible?

### Zero-Downtime Assessment
- Can this migration run while the application is serving traffic?
- Are there lock contentions to consider?
- What's the estimated migration duration?

# Step 5: Generate Migration Strategy

## Output Format

### Migration Analysis Summary
**Migration File**: [File name/path]
**Database Type**: [PostgreSQL/MySQL/etc.]
**Tables Affected**: [Count and list]
**Risk Level**: [CRITICAL/HIGH/MEDIUM/LOW]
**Estimated Duration**: [Based on table sizes]

### Executive Summary
[2-3 paragraphs describing the migration purpose, key changes, and overall risk assessment]

### Change Inventory
| Type | Operation | Object | Risk Level | Notes |
|------|-----------|--------|------------|-------|
| Table | CREATE | users | LOW | New table |
| Column | DROP | users.legacy_id | CRITICAL | Data loss |
| Index | CREATE | idx_users_email | MEDIUM | Large table |

### Detailed Analysis

#### [Change 1] [Operation Description]
- **Statement**: `[SQL statement]`
- **Risk Level**: [CRITICAL/HIGH/MEDIUM/LOW]
- **Affected Object**: [Table/Column/Index name]
- **Current State**: [What exists now]
- **Target State**: [What will exist after]

**Potential Issues**:
- [List specific concerns]

**Mitigation**:
- [How to safely execute this change]

### Pre-Migration Checklist
- [ ] Backup database before migration
- [ ] Verify backup can be restored
- [ ] Test migration on staging environment
- [ ] Estimate migration duration on production data
- [ ] Prepare rollback script
- [ ] Schedule maintenance window (if required)
- [ ] Notify stakeholders

### Safe Migration Steps

#### Phase 1: Pre-Migration
```sql
-- Backup commands
-- Verification queries
```

#### Phase 2: Execute Migration
```sql
-- Migration statements in safe order
-- With progress monitoring
```

#### Phase 3: Post-Migration Validation
```sql
-- Verification queries
SELECT COUNT(*) FROM affected_table;
-- Data integrity checks
```

### Rollback Procedure
```sql
-- Step-by-step rollback commands
-- In reverse order of migration
```

### Validation Queries
```sql
-- Queries to verify migration success
-- Data integrity checks
-- Performance verification
```

### Performance Recommendations
- Index recommendations for new columns
- Query optimization suggestions
- Partitioning considerations for large tables

### Zero-Downtime Strategy (if applicable)
1. **Expand**: Add new schema alongside old
2. **Migrate**: Backfill data to new structure
3. **Contract**: Remove old schema after verification

### Monitoring During Migration
- Key metrics to watch
- Alerting thresholds
- Signs of problems

### Post-Migration Tasks
- [ ] Verify application functionality
- [ ] Check query performance
- [ ] Monitor error rates
- [ ] Update documentation
- [ ] Clean up temporary objects
