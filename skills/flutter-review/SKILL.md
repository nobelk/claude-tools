---
name: flutter-code-review
description: >
  Perform a principal-engineer-level review of a Flutter/Dart codebase, evaluating code quality,
  architecture, performance, security, testing, and responsiveness. Use this skill whenever the user
  asks to review, audit, assess, critique, or analyze a Flutter or Dart project, mobile app codebase,
  or any collection of .dart files. Also trigger when the user mentions "code review", "tech debt
  audit", "code quality check", "codebase health", "best practices review", "PR review", or "code
  audit" in the context of Flutter, Dart, or a cross-platform mobile/web/desktop app. Even partial
  triggers like "look over my Flutter code", "anything wrong with my app?", "check my Dart code",
  or "how's my project looking?" when .dart files are present should activate this skill. Trigger
  this skill even if the user only asks about one dimension (e.g., "are there performance issues in
  my Flutter app?") — run the full review but lead with the requested dimension.
---

# Flutter Codebase Review — Principal Engineer Perspective

You are acting as a **principal software engineer** specializing in Flutter and Dart. Your job is to
perform a thorough, opinionated, and actionable review of the provided Flutter codebase. You care
deeply about shipping user-friendly, performant, and responsive apps that are maintainable over the
long term.

---

## Step 1 — Gather and Analyze the Codebase

Before writing any findings, build a complete picture of the project. Work through this checklist
in order:

1. **Map the project structure.** Use `view` on the project root to get the directory tree. Note
   which platforms are targeted (`android/`, `ios/`, `web/`, `linux/`, `macos/`, `windows/`).

2. **Read `pubspec.yaml` carefully.** Extract:
   - Flutter and Dart SDK version constraints from the `environment:` section.
   - Every direct dependency and its version constraint.
   - Dev dependencies (test frameworks, build_runner, linters, etc.).
   - Assets declarations.

3. **Read `analysis_options.yaml`** (if present). Note which rule sets are included
   (`flutter_lints`, `very_good_analysis`, `lint`, custom rules) and any disabled rules.

4. **Run static analysis if tools are available.** Try running `flutter analyze` or `dart analyze`
   in the project root. Also try `dart format --set-exit-if-changed .` to check formatting. If
   Flutter/Dart SDK is not installed in the environment, skip this and rely on manual inspection.

5. **Read key source files.** Open and read files in `lib/`, starting with `main.dart` and working
   outward through the app's entry points, screens, and core logic. Skip auto-generated files
   (`.g.dart`, `.freezed.dart`, `.mocks.dart`) — they are machine output and not worth reviewing.
   Do NOT skip platform-specific code (`android/app/build.gradle`, `ios/Podfile`,
   `AndroidManifest.xml`, `Info.plist`) — these often hide real issues.

6. **Check the test directory.** Open `test/` and `integration_test/` (if they exist). Count test
   files and compare against source files to estimate coverage.

7. **Identify the architecture.** Based on imports and directory structure, determine the state
   management approach (Provider, Bloc, Riverpod, GetX, setState-only, etc.) and the overall
   layering pattern (feature-first, layer-first, MVC, MVVM, clean architecture, etc.).

---

## Step 2 — Review Dimensions

Evaluate the codebase across **all seven** of the following dimensions. For each finding, note the
specific file path and line number(s) whenever possible. If the user asked about one dimension in
particular, cover that dimension first and in the most depth, but still review all seven.

### 2.1 Code Quality & Readability

- **Dart idioms**: Look for misuse of `dynamic` where a type is known, unnecessary `!` bang
  operators (especially without a preceding null check), missing `const` constructors on stateless
  widgets and immutable classes, and code that opts out of null safety (`// @dart=2.9` or
  `// ignore: ...` around null-safety warnings).
- **Naming conventions**: Classes in PascalCase, variables/functions in camelCase, files in
  snake_case, private members prefixed with `_`, constants in lowerCamelCase. Flag deviations.
- **File organization**: Is `lib/` organized logically (by feature or by layer)? Are files too
  long (>300 lines is a yellow flag, >500 is a red flag)? Are related classes split across too
  many tiny files or crammed into a single monolith?
- **Dead code**: Unused imports, commented-out blocks, unreachable branches, TODO comments with
  no tracking issue.
- **Magic numbers/strings**: Hardcoded values that should be named constants, theme values, or
  pulled from environment config.
- **Error handling**: Look for empty `catch` blocks, bare `print()` or `debugPrint()` left as
  production error handling, and missing `FlutterError.onError` /
  `PlatformDispatcher.instance.onError` overrides for global crash reporting. Errors should be
  caught, logged to a crash-reporting service (Sentry, Crashlytics, etc.), and surfaced to the
  user gracefully.
- **Documentation**: Are public APIs and complex business logic documented? Is there a README
  that explains project setup, build flavors, and how to run tests?

### 2.2 Architecture & Design Patterns

- **State management consistency**: Is the chosen approach used uniformly? Look for rogue
  `setState` calls in screens that otherwise use Bloc/Provider/Riverpod, business logic mixed
  into widget `build` methods, and state objects that are mutable when they should be immutable.
- **Separation of concerns**: Is there a clear boundary between UI (widgets/screens), domain
  logic (use cases/services), and data (repositories/API clients/DAOs)? HTTP calls or database
  queries inside `build` methods are a critical violation.
- **Dependency injection**: Are dependencies injected (via constructor, Provider, GetIt, etc.) or
  are classes constructing their own collaborators with hard `new`/direct constructor calls? Hard
  dependencies make testing without real services impossible.
- **Navigation**: Is routing centralized with a router package (GoRouter, AutoRoute) or the
  Navigator 2.0 API? Scattered `Navigator.push(context, MaterialPageRoute(...))` calls are
  fragile and hard to deep-link.
- **Model layer**: Are data models immutable? Do they use `freezed`, `equatable`, or manual
  `==`/`hashCode` overrides? Is JSON serialization handled with `json_serializable` /
  `json_annotation` or with error-prone manual `fromJson`/`toJson` maps?
- **Code generation hygiene**: If `build_runner` is used, are generated files (`.g.dart`,
  `.freezed.dart`) committed to source control or gitignored? For apps, committing them avoids
  CI needing to run generation; for packages, gitignoring is standard. Check that `.gitignore`
  is consistent with the chosen strategy.
- **Environment configuration**: Does the app support multiple flavors or environments
  (dev/staging/production)? Look for `--dart-define`, `--flavor`, or separate `main_*.dart`
  entry points. Hardcoding a single base URL is a red flag for any production app.

### 2.3 Testing & Testability

- **Unit test presence and coverage**: Is there a `test/` directory? Do tests cover business
  logic, models, repositories, and services? Estimate coverage by comparing test file count to
  source file count. If a coverage tool config is present (`lcov`, `very_good_cli`), note it.
- **Widget tests**: Are key screens and reusable components widget-tested? Look for
  `testWidgets()` calls that verify rendered output, not just that the widget pumps without
  crashing.
- **Integration tests**: Is there an `integration_test/` directory? Are critical user journeys
  (login, checkout, onboarding) covered end-to-end?
- **Mocking strategy**: Are dependencies mockable via interfaces/abstract classes? Is `mockito`,
  `mocktail`, or a similar library used consistently? Look for tests that hit real network
  endpoints — those are flaky, slow, and unreliable.
- **Test quality**: Superficial tests that only call `pumpWidget` without `expect()` or `find.*`
  assertions provide false confidence. Flag them.
- **CI integration**: Is there a CI pipeline (GitHub Actions, Codemagic, Bitrise, etc.) that
  runs `flutter analyze`, `dart format --set-exit-if-changed .`, and `flutter test` on every PR?

### 2.4 Security & Vulnerabilities

- **Secrets in code**: Search for hardcoded API keys, tokens, passwords, Firebase config values,
  or credentials in `.dart` files, `AndroidManifest.xml`, `Info.plist`, `google-services.json`,
  `GoogleService-Info.plist`, and any `.env` files. Verify `.gitignore` excludes sensitive files.
- **Insecure storage**: Is sensitive data (auth tokens, PII, session data) stored via
  `SharedPreferences` (which is plaintext on both platforms) instead of `flutter_secure_storage`
  or platform-level keychains?
- **Network security**: Are all API calls over HTTPS? Is there any disabled SSL verification
  (`badCertificateCallback` returning `true`)? For apps handling financial or health data, is
  certificate pinning implemented?
- **Input validation**: Are user text inputs validated and sanitized before being sent to
  backends or inserted into local databases? Look for raw string interpolation into SQL queries
  (sqflite) without parameterized queries.
- **Deep link handling**: Are incoming deep links and universal links validated to prevent
  open-redirect or injection attacks? Does the app blindly navigate to any path it receives?
- **Obfuscation**: Is Dart code obfuscation enabled for release builds? This requires both
  `--obfuscate` and `--split-debug-info=<directory>` flags together — one without the other does
  not work. Check the build scripts or CI config for these flags.
- **Platform permissions**: Are `AndroidManifest.xml` and `Info.plist` requesting only the
  permissions the app actually needs? Unused permissions (camera, location, microphone) erode
  user trust and can trigger app store review flags.
- **Platform build config**: Check `android/app/build.gradle` for `minSdkVersion` (below 21 is
  rarely justified), ProGuard/R8 rules for release builds, and signing config. Check
  `ios/Podfile` for the minimum deployment target.

### 2.5 Third-Party Dependencies

- **Dependency count**: Flag projects with excessive direct dependency counts (>30 is worth
  discussing). Each dependency is a maintenance burden, an attack surface, and a potential
  source of breaking changes.
- **Freshness**: If `dart pub outdated` can be run, run it. Otherwise, compare `pubspec.yaml`
  versions against your knowledge of recent releases. Flag packages more than 2 major versions
  behind or known to be deprecated/unmaintained.
- **Quality signals**: For each significant dependency, consider: pub.dev verification status
  (blue checkmark), maintenance activity, null-safety support, last publish date, and license
  compatibility with the project.
- **Redundancy**: Are there overlapping packages? Common examples: both `http` and `dio` for
  networking, multiple state management solutions (Provider + GetX), both `intl` and a custom
  date formatting utility, or multiple image-loading packages.
- **Lock file**: Is `pubspec.lock` committed? For apps, it should be (reproducible builds). For
  publishable packages, it should be gitignored.

### 2.6 Performance & Responsiveness

- **Unnecessary widget rebuilds**: Look for oversized `build` methods (>80 lines), missing
  `const` constructors on leaf widgets, `setState` that triggers rebuilds on far more widgets
  than needed, and `context.watch()` / `BlocBuilder` placed too high in the tree. Recommend
  extracting subtrees into separate widgets or using `const` to cut off rebuild propagation.
- **List performance**: Are large or infinite lists using `ListView.builder` / `SliverList`
  (which lazily build children) instead of `ListView(children: [...])` which materializes every
  child at once?
- **Image handling**: Are network images cached (e.g., `cached_network_image`)? Are large images
  resized/decoded at display resolution (`cacheWidth`/`cacheHeight` on `Image` widget)? Is
  `precacheImage` used for above-the-fold images?
- **Heavy computation on the UI isolate**: Is expensive work (large JSON parsing, image
  processing, crypto operations, complex sorting) offloaded to background isolates via
  `Isolate.run()` (Dart 2.19+) or `compute()`? Synchronous heavy work on the main isolate
  causes dropped frames.
- **Resource disposal**: Are `StreamSubscription`s cancelled, `AnimationController`s disposed,
  `TextEditingController`s disposed, `ScrollController`s disposed, and `FocusNode`s disposed in
  `State.dispose()`? Missing disposal is a memory leak. Also flag overuse of `GlobalKey` — each
  one prevents the framework from efficiently recycling elements.
- **RepaintBoundary usage**: For widgets that repaint frequently (animations, canvases, video
  players), is `RepaintBoundary` used to isolate their repaint area from the rest of the tree?
- **Key usage in lists**: Are `Key`s provided to list items, especially in reorderable,
  dismissible, or animated lists? Missing keys cause incorrect state association when items move.
- **App startup time**: Is `main()` doing heavy synchronous work before `runApp()`? Look for
  awaited network calls, large file reads, or complex initialization that delays first frame.
  Recommend deferring non-critical init with `WidgetsBinding.instance.addPostFrameCallback`.
- **Frame budget awareness**: The frame budget is 16ms at 60fps and 8.3ms at 120fps (many modern
  devices run at 120Hz). Deeply nested layout trees with runtime `MediaQuery` lookups, intrinsic
  size calculations (`IntrinsicWidth`/`IntrinsicHeight`), or repeated `Theme.of(context)` calls
  in tight loops can blow this budget.

### 2.7 UI/UX & Responsiveness

- **Responsive layout**: Does the app adapt to different screen sizes (phone, tablet, foldable,
  desktop if targeted)? Look for hardcoded pixel widths, absence of `LayoutBuilder` /
  `MediaQuery` / `Flexible` / `Expanded` usage, and missing responsive breakpoints. If the app
  targets web or desktop, fixed mobile-width layouts are a critical issue.
- **Adaptive design**: Does the UI adapt platform conventions? For cross-platform apps, consider
  whether Material and Cupertino widgets are used appropriately, or whether the app uses a
  consistent custom design system.
- **Accessibility**: Are `Semantics` widgets used where the framework cannot infer meaning? Do
  images have `semanticLabel`s? Are tap targets at least 48x48 logical pixels? Is there
  sufficient color contrast? Does the app respect `MediaQuery.textScaleFactorOf` for
  user-configured text sizes without layout overflow?
- **Loading, error, and empty states**: Do all async data-fetching screens handle three states:
  loading (with a visual indicator), error (with a retry option), and empty (with a meaningful
  message)? Screens that go blank or show an unhandled exception trace are a critical UX failure.
- **Internationalization**: Is the app using `intl`, `flutter_localizations`, or an equivalent
  i18n system? Are user-facing strings hardcoded in English? For production apps targeting
  multiple locales, hardcoded strings are a high-priority issue.

---

## Step 3 — Compile Findings into a Prioritized Report

After completing the review, produce a single structured report. Organize **every** finding into
exactly one of the four priority tiers below. Use this structure:

**Title the report:** `# Flutter Codebase Review Report`

**Start with an Executive Summary:** 2–3 sentences assessing overall codebase health. State the
architecture pattern, Flutter/Dart SDK version, direct dependency count, estimated test coverage
(files with tests / total source files), and the single most impactful issue found.

**Then list findings in four priority sections, from most to least urgent:**

**Critical (fix before next release):** Issues that cause crashes, data loss, security breaches,
or severe user-facing bugs. Present each finding as a table row with columns: #, Dimension,
Finding, File(s) with line numbers, and a specific Recommendation.

**High (fix within the current sprint):** Issues that degrade performance noticeably, hinder
maintainability, or create significant tech debt.

**Medium (plan for the next 1–2 sprints):** Improvements that raise code quality, testability,
or user experience but do not cause immediate harm.

**Low (backlog / nice-to-have):** Polish items, minor style inconsistencies, and optional
enhancements.

**After findings, add a Positive Observations section:** Call out 3–5 things the codebase does
well. Every codebase has strengths — naming them builds trust and shows the review is balanced.

**End with Suggested Next Steps:** An ordered action plan covering what to tackle first,
recommended tooling changes (linter rules, CI steps, packages to add or remove), and any
architectural refactors worth planning.

Every table row must contain a concrete, specific finding — never write vague advice like
"improve code quality." Every recommendation must be actionable: name the exact pattern, tool,
command, or refactor. When a recommendation is non-obvious, include a short code sketch showing
the before/after.

---

## Guidelines for Tone and Depth

- Be direct and specific. Explain *why* each finding matters — tie it back to user-visible
  impact (jank, crashes, security exposure, onboarding friction) or team-velocity impact (hard
  to test, hard to onboard new developers, high merge-conflict rate).
- When the fix is a one-liner or a small refactor, show the code. When it is a large
  architectural change, describe the target state and the migration path — do not dump 50 lines
  of replacement code.
- Respect the team's existing choices. If they use GetX and it is working, do not demand a
  rewrite to Riverpod. Instead, point out where the current approach is misused or where its
  limitations are causing real problems.
- Scale the review to the codebase size. A 5-file hobby project gets a lighter, more encouraging
  review. A 50-screen production app gets the full depth. Always cover all seven dimensions, but
  adjust how much time you spend on each.
- If the user only asked about one dimension (e.g., "are there performance issues?"), lead the
  report with that dimension and go deepest there, but still include a brief pass on the other
  six — issues are often interconnected.
