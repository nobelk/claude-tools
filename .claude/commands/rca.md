# Analyze Exception and Provide Fix

## Objective
Analyze the exception details in `{{EXCEPTION_FILE}}` and identify the root cause bug in the codebase. Provide a comprehensive fix with unit tests.

## Instructions

### Step 1: Exception Analysis
1. Read the exception file: `{{EXCEPTION_FILE}}`
2. Extract and parse:
   - Exception type and message
   - Full stack trace
   - Any nested exceptions or root causes
   - Timestamp and context (if available)
   - Thread information
   - Request/response details (if HTTP exception)

### Step 2: Code Investigation
Based on the stack trace, systematically investigate:

1. **Primary failure point**:
   - Identify the exact line where the exception occurred
   - Read the method containing the failure
   - Examine the class and its dependencies
   - Check method parameters and return types

2. **Call chain analysis**:
   - Trace through each method in the stack trace
   - Read relevant source files in order of appearance
   - Note any data transformations or validations
   - Identify where invalid data originated

3. **Context gathering**:
   - Search for similar exception handling patterns
   - Check related configuration files (application.yml, etc.)
   - Review database migrations if data-related
   - Examine DTOs, entities, and mappers involved
   - Check recent commits affecting these files

### Step 3: Root Cause Identification
Determine the root cause by analyzing:

1. **Common patterns**:
   - Null pointer exceptions: Missing null checks or initialization
   - Type casting errors: Incorrect type assumptions
   - Database constraints: Foreign key or unique violations
   - Concurrency issues: Race conditions or deadlocks
   - Resource exhaustion: Memory, connections, or file handles
   - Configuration issues: Missing or invalid properties
   - Integration failures: External service connectivity

2. **Spring Boot specific**:
   - Bean initialization failures
   - Circular dependencies
   - Transaction management issues
   - Security/authentication problems
   - JPA/Hibernate lazy loading exceptions
   - REST API validation errors

3. **Project-specific considerations**:
   - Multi-tenancy (X-NISC-REALM) issues
   - AWS service integration problems
   - OpenSearch connectivity/query issues
   - JOOQ query generation problems
   - S3 file operations failures

### Step 4: Solution Development
Create a comprehensive fix:

1. **Code changes**:
   - Provide exact file paths and line numbers
   - Show before/after code snippets
   - Add appropriate error handling
   - Include validation and defensive programming
   - Consider performance implications
   - Ensure thread safety if applicable

2. **Fix principles**:
   - Fix the root cause, not just symptoms
   - Maintain existing code patterns and conventions
   - Follow Spring Boot best practices
   - Preserve backward compatibility
   - Add appropriate logging for future debugging
   - Consider configuration vs code changes

### Step 5: Test Creation
Generate comprehensive tests:

1. **Unit test to reproduce the issue**:
   ```java
   @Test
   void shouldReproduceExceptionScenario() {
       // Arrange: Set up conditions that cause the exception
       // Act: Execute the problematic code
       // Assert: Verify exception is thrown with expected details
   }
   ```

2. **Unit test to validate the fix**:
   ```java
   @Test
   void shouldHandleScenarioCorrectlyAfterFix() {
       // Arrange: Set up same conditions
       // Act: Execute fixed code
       // Assert: Verify correct behavior without exception
   }
   ```

3. **Edge case tests**:
   - Boundary conditions
   - Null/empty inputs
   - Invalid data scenarios
   - Concurrent access (if applicable)

4. **Integration test (if needed)**:
   - For database-related issues
   - For external service interactions
   - Using TestContainers for realistic environment

### Step 6: Verification Steps
Provide instructions to verify the fix:

1. How to run the specific tests
2. Expected behavior after the fix
3. Any configuration changes needed
4. Performance impact assessment
5. Rollback plan if issues arise

## Output Format

### 1. Exception Summary
- **Type**: [Exception class name]
- **Message**: [Exception message]
- **Location**: [File:line where it occurred]
- **Frequency**: [If available from logs]

### 2. Root Cause Analysis
- **Primary Cause**: [Clear explanation]
- **Contributing Factors**: [List any secondary issues]
- **Impact**: [What functionality is affected]

### 3. Proposed Fix
```java
// File: [path/to/file.java]
// Line: [line number]
// Before:
[original code]

// After:
[fixed code]
```

### 4. Unit Tests
```java
// File: [path/to/test/file.java]
[complete test class or methods]
```

### 5. Verification
- Run: `./gradlew test --tests "TestClassName"`
- Expected: [Description of correct behavior]
- Rollback: [If needed, how to revert]

## Additional Considerations
- Check if this is a regression from recent changes
- Consider if similar issues might exist elsewhere
- Document any assumptions made during analysis
- Note any temporary workarounds if immediate fix isn't possible
- Suggest monitoring/alerting improvements to catch this earlier

## Example Usage
To use this command, replace `{{EXCEPTION_FILE}}` with the actual file name:
```
Analyze the exception details in `exceptions.txt` and identify the root cause...
```
