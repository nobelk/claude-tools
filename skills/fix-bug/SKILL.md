---
name: bugfix
description: >
  Fix a bug in a user-specified file using a test-driven approach. Claude writes
  failing unit tests that reproduce the bug, fixes the code, verifies the tests
  pass, runs the full test suite to catch regressions, then clears context and
  reviews all changes for accuracy and optimality. Supports C#, Python, and
  Flutter/Dart codebases. Use this skill whenever the user reports a bug, defect,
  or unexpected behavior in their code and wants it fixed — even if they don't
  explicitly say "bug." Also trigger when a user says things like "this isn't
  working," "I'm getting an error," "this test is failing," "something broke,"
  or "can you fix this."
---

# Bugfix Skill — Test-Driven Bug Fixing

Fix bugs through a disciplined, test-driven workflow: reproduce first, fix second, verify third, review last.

## Overview

This skill follows a strict sequence to ensure high-quality, regression-free bug fixes:

1. **Understand** the bug and the codebase
2. **Reproduce** the bug with failing unit tests
3. **Fix** the bug in the source code
4. **Verify** the fix by running the new tests
5. **Regression-check** by running the full test suite
6. **Review** all changes with fresh context

## Supported Languages

Read the appropriate reference file for language-specific conventions before writing any tests or code:

| Language | Reference | Test Frameworks |
|----------|-----------|-----------------|
| C# / .NET | `references/csharp.md` | xUnit, NUnit, MSTest |
| Python | `references/python.md` | pytest, unittest |
| Flutter / Dart | `references/flutter.md` | flutter_test, mockito |

**Always read the relevant reference file before proceeding.** It contains critical details about test discovery, project structure, and common pitfalls for each language.

---

## Workflow

### Phase 1 — Understand the Bug

Before writing any code, build a mental model of the problem.

1. **Locate the file.** The user will specify the buggy file. Open it and read it fully.
2. **Understand the bug.** Ask the user to describe the bug if they haven't already. Clarify:
   - What is the expected behavior?
   - What is the actual behavior?
   - Are there steps to reproduce, error messages, or stack traces?
3. **Explore the surrounding code.** Read imports, callers, and related modules to understand context. Identify the root cause — don't just treat the symptom.
4. **Detect the language.** Determine whether the project is C#, Python, or Flutter/Dart based on file extensions, project files, and directory structure.
5. **Read the language reference.** Call `view` on the appropriate `references/<language>.md` file for framework-specific guidance.

### Phase 2 — Discover Existing Test Conventions

The new tests must blend seamlessly with the existing test suite. Before writing anything:

1. **Find the test directory.** Look for common test locations:
   - Python: `tests/`, `test/`, `*_test.py`, `test_*.py` files alongside source
   - C#: `*.Tests` or `*.UnitTests` project directories
   - Flutter: `test/` directory at the project root
2. **Read 2–3 existing test files.** Note:
   - Which test framework and assertion library is used
   - Naming conventions for test files, classes, and methods
   - How fixtures, setup/teardown, and mocks are structured
   - Import patterns and any shared test utilities or helpers
   - How test data is organized (inline, fixtures, factories)
3. **Identify the test runner command.** Find how the team runs tests — look for CI configs, Makefiles, scripts, or `README` instructions. Fall back to standard commands if nothing is found:
   - Python: `pytest` or `python -m pytest`
   - C#: `dotnet test`
   - Flutter: `flutter test`

### Phase 3 — Write Failing Unit Tests

Write tests that **fail because of the bug** and will **pass once the bug is fixed**. This is the most important phase — it proves the bug exists and defines the fix's success criteria.

1. **Place tests correctly.** Put the new test file (or add to an existing test file) in the location and with the naming convention that matches the project's existing patterns.
2. **Follow existing conventions exactly.** Mirror the framework, style, naming, imports, and structure you observed in Phase 2. The new tests should look like a natural part of the codebase.
3. **Write focused, minimal tests.** Each test should target one specific aspect of the bug:
   - A test for the primary failure case
   - A test for edge cases or boundary conditions related to the bug, if applicable
   - A test for the expected correct behavior
4. **Name tests descriptively.** The test name should communicate what behavior is being verified, e.g., `test_parse_returns_none_for_empty_input` or `CalculateTotal_WithNegativeDiscount_ThrowsArgumentException`.
5. **Run the new tests to confirm they fail.**
   ```
   Execute the test runner targeting ONLY the new tests.
   Verify the output shows failures for the right reasons.
   If the tests pass, the tests don't actually capture the bug — revise them.
   If the tests fail for the wrong reasons (import errors, syntax issues),
   fix the tests before proceeding.
   ```

### Phase 4 — Fix the Bug

Now, and only now, fix the actual source code.

1. **Make the minimal change necessary.** Don't refactor, don't clean up unrelated code, don't "improve" adjacent logic. Scope the change tightly to the bug.
2. **Explain the root cause.** Before editing, state in a concise comment or message:
   - What the root cause is
   - Why the current code is wrong
   - What the fix does and why it's correct
3. **Edit the source file.** Use `str_replace` for surgical edits. Prefer small, targeted changes over rewrites.

### Phase 5 — Verify the Fix

1. **Re-run the new tests.** Execute the same test command from Phase 3. All new tests must now pass.
2. **If any new test still fails**, re-examine the fix. Either the fix is incomplete or the test expectation is wrong. Iterate until all new tests pass.

### Phase 6 — Run the Full Test Suite

Run the entire project's test suite to catch regressions.

1. **Execute the full test runner.** Use the project-wide test command.
2. **Analyze any failures.**
   - If a pre-existing test fails and it's clearly unrelated to the change (e.g., a flaky test, environment issue), note it for the user but don't try to fix it.
   - If a test fails because of the change, the fix introduced a regression. Revise the fix and re-run until the full suite passes.
3. **Report results.** State how many tests ran, how many passed, and whether any pre-existing failures were observed.

### Phase 7 — Context Reset and Review

This step catches errors that are easy to miss when you've been deep in the code. The goal is to look at the changes with fresh eyes.

1. **Clear your working context.** Take a step back. Re-read the user's original bug description.
2. **Review every changed file.** For each file that was modified or created:
   - Re-read the full diff (use `git diff` or compare the before/after)
   - Verify the change is correct and complete
   - Check for accidental side effects, leftover debug code, or style inconsistencies
3. **Review the new tests.** Confirm:
   - Tests actually exercise the buggy code path
   - Assertions are correct and not tautological
   - Tests would fail if the fix were reverted
   - Test names and structure follow project conventions
4. **Assess optimality.** Consider:
   - Is the fix the simplest correct solution?
   - Are there edge cases the tests don't cover?
   - Could the fix break anything the tests don't check?
5. **Report to the user.** Summarize:
   - Root cause of the bug
   - What was changed and why
   - Test results (new tests + full suite)
   - Any concerns, edge cases, or follow-up recommendations

---

## Error Recovery

Things won't always go smoothly. Here's how to handle common issues:

- **Can't find existing tests:** Ask the user where tests live. If there are truly no tests, create a new test file following standard conventions for the language (see the reference file).
- **Test framework not installed:** Inform the user and suggest the install command. Don't install frameworks without asking.
- **Flaky or slow tests:** If the full suite takes too long or has known flaky tests, ask the user if you should run a subset. Always run at least the tests in the same module/directory as the change.
- **Multiple bugs entangled:** If you discover the reported bug is actually multiple issues, fix the one the user described and note the others. Don't scope-creep.
- **Ambiguous root cause:** If there are multiple plausible causes, write tests that distinguish between them. The failing test pattern will clarify which cause is real.

---

## Key Principles

- **Test first, fix second.** Never fix the bug before you have a failing test. The test is your proof that the bug existed and that you fixed it.
- **Match the codebase.** New tests and code should look like they were written by the same team. Follow existing patterns for style, naming, and structure.
- **Minimal changes.** The best bug fix is the smallest correct one. Resist the urge to refactor.
- **Verify twice.** Run the new tests AND the full suite. A fix that introduces a regression is not a fix.
- **Fresh-eyes review.** The context reset in Phase 7 catches mistakes that tunnel vision misses. Don't skip it.
