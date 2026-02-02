---
name: tdd-bugfix
description: Fix bugs in code using test-driven development methodology. Use when a user reports a bug in a function or file and wants it fixed safely. This skill ensures bug fixes are verified by first writing failing unit tests that expose the bug, running them to confirm failure, fixing the code, then re-running tests to verify the fix, and finally running all project tests to catch regressions. All new code strictly follows the existing project's build method, coding style, testing conventions, folder structure, test libraries, and mocking patterns — discovered entirely from the codebase itself.
---

# TDD Bug Fix

Fix bugs using a test-driven approach. All new code and tests MUST match the existing project's conventions — discovered from the codebase, never assumed.

## Workflow

1. **Discover project conventions** - Survey the codebase to learn its build system, coding style, and testing patterns
2. **Understand the bug** - Analyze the reported bug and identify affected code
3. **Write failing tests** - Create tests using the project's own test libraries, mocks, and style that fail due to the bug
4. **Confirm test failure** - Run new tests using the project's own build/test command to verify failure
5. **Fix the bug** - Modify code following project conventions to resolve the issue
6. **Verify fix** - Re-run the new tests to confirm they now pass
7. **Run full test suite** - Execute all project tests using the project's build system to ensure no regressions

## Step 1: Discover Project Conventions

Before writing any code, perform these three discovery activities.

### 1a. Explore the project structure and build system

List the project root directory and identify:
- **Directory layout**: How is source code organized? Where do tests live relative to source?
- **Build/task configuration**: Read config files at the project root to determine the build tool, task runner, and available commands. Look for predefined build, test, and lint commands or targets.
- **Dependency manifest**: Read the project's dependency file to identify installed test libraries, assertion libraries, mocking frameworks, linters, and formatters. These are the libraries to use — do not introduce new ones.
- **Linter/formatter config**: Check for linter or formatter configuration files at the project root. If a formatter is configured, plan to run it on modified files after changes. Note any style rules that constrain new code.
- **CI configuration**: Check for CI pipeline files that reveal the canonical build and test commands.

### 1b. Read source files to learn coding style

Read the buggy file and 2–3 neighboring source files in the same directory. Note:
- **Naming**: Casing convention for functions, variables, classes, and constants
- **Formatting**: Indentation style and width, line length, brace/bracket placement, trailing commas
- **Type system**: Whether type annotations are present and their style
- **Documentation**: What comment and docstring format is used, and how heavily — sparse or detailed
- **Error handling**: What patterns the code uses for errors and edge cases
- **Imports/modules**: How imports are structured, ordered, and whether they are relative or absolute

### 1c. Read existing tests to learn testing patterns

Find 2–3 existing test files, prioritizing tests for code near the bug. If uncertain where tests live, use the directory layout from 1a or search for files matching common test naming patterns. Note:
- **File location & naming**: What directory are tests in? What is the test file naming pattern?
- **Framework & assertions**: What test framework is being used? What assertion style do existing tests use?
- **Structure**: Are tests standalone functions, grouped in classes, or nested in describe/context blocks?
- **Setup & teardown**: What patterns are used for test setup, shared fixtures, and cleanup?
- **Mocking & stubbing**: What mocking library and patterns do existing tests use? These are the patterns to follow — do not introduce a different mocking approach.
- **Imports & utilities**: How do tests import the code under test? Are there shared test helpers, factories, or fixture files? Use these same utilities.

## Step 2: Understand the Bug

- Read the buggy file and the specific function(s) affected
- Determine expected behavior vs. actual behavior
- Identify inputs and edge cases that trigger the bug
- Check if related tests already exist that should have caught this — understand why they didn't

## Step 3: Write Failing Unit Tests

Create tests that expose the bug. Every aspect of the new test code must be derived from what was discovered in Step 1.

Checklist — verify each item against existing test files before proceeding:
- [ ] Test file placed in the same directory and naming pattern as existing tests
- [ ] Same test framework and assertion library — no new test dependencies
- [ ] Same structural pattern as neighboring tests (function-based, class-based, describe blocks, etc.)
- [ ] Same setup/teardown and fixture patterns
- [ ] Same import style for the module under test, using the same shared test utilities if they exist
- [ ] Same mocking library and mocking patterns — no new mocking dependencies
- [ ] Comments/docstrings in the same format and density as existing tests (omit if existing tests omit them)
- [ ] Naming follows the exact test naming convention visible in existing test files

Write 1–3 focused tests targeting the bug. Include edge cases closely related to the bug.

**If no tests exist in the project**: Check if the dependency manifest includes any test libraries or if there is any test configuration. If so, follow those conventions. If the project has zero test infrastructure, ask the user what approach they prefer before proceeding.

## Step 4: Confirm Test Failure

Run the new tests using the project's own test command discovered in Step 1a. Target only the new test file or specific test names to isolate the results.

Verify that:
- Tests fail with assertion errors that clearly demonstrate the bug
- The failure messages confirm the tests are exercising the right code path

If tests pass unexpectedly, the tests are not targeting the bug — revise them before proceeding.

## Step 5: Fix the Bug

Apply the minimal change to resolve the bug. The fix must be indistinguishable in style from the surrounding code:
- Same naming, formatting, and indentation as the rest of the file
- Same error handling patterns as surrounding code
- Type annotations present if and only if the surrounding code uses them, in the same style
- Comments added only if the surrounding code uses comments at similar complexity — do not add comments to a codebase that avoids them
- No reformatting, renaming, or refactoring of adjacent code

If a formatter was identified in Step 1a, run it on the changed file after editing.

## Step 6: Verify Fix

Re-run the exact same test command from Step 4. All new tests must pass. If any fail, revisit the fix.

## Step 7: Run Full Test Suite

Run the project's full test suite using the canonical test command discovered in Step 1a.

All existing tests plus new tests must pass. If any existing tests fail, the fix introduced a regression — narrow the change and retest.

## Troubleshooting

**Tests won't run:** Check for missing dependencies using the project's package manager (identified in Step 1a). Check for required environment variables, test databases, or setup scripts documented in the project.

**Tests pass when they should fail:** The test is not exercising the buggy code path. Verify inputs actually trigger the bug. Add temporary logging to the buggy function to confirm the test reaches it.

**Fix causes other tests to fail:** The fix is too broad or changes behavior that other code depends on. Narrow the change. Check if the failing tests have incorrect expectations that masked the original bug.

**No existing tests to reference for style:** Ask the user for their preferred approach. Set up minimal test scaffolding consistent with any test libraries already in the project's dependencies.
