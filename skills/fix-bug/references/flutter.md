# Flutter / Dart — Test & Fix Reference

## Detecting the Test Setup

1. **pubspec.yaml** — look for `dev_dependencies`:
   - `flutter_test` (included by default in Flutter projects)
   - `test` (for pure Dart packages)
   - `mockito` + `build_runner` → Mockito for mocking
   - `mocktail` → Mocktail (no code generation, simpler)
   - `bloc_test` → Bloc testing utilities
2. **test/ directory** — Flutter/Dart convention is a top-level `test/` folder
3. **Existing test files** — check imports and patterns to identify conventions

## Project Structure

```
my_app/
├── lib/
│   └── src/
│       ├── models/
│       │   └── user.dart
│       └── services/
│           └── auth_service.dart
├── test/
│   ├── models/
│   │   └── user_test.dart          ← Mirrors lib/src structure
│   ├── services/
│   │   └── auth_service_test.dart
│   └── helpers/                     ← Shared test utilities
│       └── mocks.dart
└── pubspec.yaml
```

Test files mirror the `lib/` source structure inside `test/` and are named `<source_file>_test.dart`.

## flutter_test Conventions

### File and Naming

- Test files: `<source_file>_test.dart`
- Group descriptions: describe the class or feature being tested
- Test descriptions: describe the specific behavior in lowercase natural language
- Every test file needs `import 'package:flutter_test/flutter_test.dart';` (or `package:test/test.dart` for pure Dart)

### Unit Test Patterns

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/src/models/user.dart';

void main() {
  group('User', () {
    group('fromJson', () {
      test('parses valid JSON correctly', () {
        final json = {'name': 'Alice', 'age': 30};
        final user = User.fromJson(json);
        expect(user.name, equals('Alice'));
        expect(user.age, equals(30));
      });

      test('throws FormatException for missing name', () {
        final json = {'age': 30};
        expect(
          () => User.fromJson(json),
          throwsA(isA<FormatException>()),
        );
      });

      test('defaults age to 0 when not provided', () {
        final json = {'name': 'Bob'};
        final user = User.fromJson(json);
        expect(user.age, isZero);
      });
    });
  });
}
```

### Widget Test Patterns

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/src/widgets/counter_widget.dart';

void main() {
  group('CounterWidget', () {
    testWidgets('displays initial count of 0', (WidgetTester tester) async {
      await tester.pumpWidget(const MaterialApp(home: CounterWidget()));
      expect(find.text('0'), findsOneWidget);
    });

    testWidgets('increments count on button tap', (WidgetTester tester) async {
      await tester.pumpWidget(const MaterialApp(home: CounterWidget()));
      await tester.tap(find.byIcon(Icons.add));
      await tester.pump();
      expect(find.text('1'), findsOneWidget);
    });
  });
}
```

### Mocking with Mockito

Mockito requires code generation in Dart. Check if the project uses the `@GenerateMocks` annotation pattern:

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:my_app/src/services/auth_service.dart';
import 'package:my_app/src/services/api_client.dart';

@GenerateMocks([ApiClient])
import 'auth_service_test.mocks.dart';

void main() {
  late AuthService authService;
  late MockApiClient mockApiClient;

  setUp(() {
    mockApiClient = MockApiClient();
    authService = AuthService(apiClient: mockApiClient);
  });

  group('AuthService', () {
    test('login returns user on success', () async {
      when(mockApiClient.post(any, body: anyNamed('body')))
          .thenAnswer((_) async => {'token': 'abc123'});

      final result = await authService.login('user', 'pass');
      expect(result.token, equals('abc123'));
    });

    test('login throws on invalid credentials', () async {
      when(mockApiClient.post(any, body: anyNamed('body')))
          .thenThrow(UnauthorizedException());

      expect(
        () => authService.login('user', 'wrong'),
        throwsA(isA<UnauthorizedException>()),
      );
    });
  });
}
```

After adding `@GenerateMocks`, run:
```bash
dart run build_runner build --delete-conflicting-outputs
```

### Mocking with Mocktail (no code generation)

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:my_app/src/services/api_client.dart';

class MockApiClient extends Mock implements ApiClient {}

void main() {
  late MockApiClient mockApiClient;

  setUp(() {
    mockApiClient = MockApiClient();
  });

  test('fetches data successfully', () async {
    when(() => mockApiClient.get(any())).thenAnswer(
      (_) async => Response(data: 'ok', statusCode: 200),
    );

    // ... test logic
  });
}
```

### setUp and tearDown

```dart
void main() {
  late Database db;

  setUp(() {
    db = Database.inMemory();
  });

  tearDown(() {
    db.close();
  });

  // setUpAll / tearDownAll for one-time setup across all tests in a group
  setUpAll(() {
    // expensive one-time initialization
  });

  group('Database', () {
    test('inserts a record', () {
      db.insert({'id': 1, 'name': 'test'});
      expect(db.count, equals(1));
    });
  });
}
```

## Running Tests

```bash
# Run all tests
flutter test

# Run a specific test file
flutter test test/models/user_test.dart

# Run with verbose output
flutter test --verbose test/models/user_test.dart

# Run tests matching a name pattern
flutter test --name "parses valid JSON"

# For pure Dart packages (no Flutter dependency)
dart test
dart test test/models/user_test.dart

# Run Mockito code generation (if project uses @GenerateMocks)
dart run build_runner build --delete-conflicting-outputs
```

## Common Pitfalls

- **Mockito code generation:** If you add a new `@GenerateMocks` annotation or modify an existing one, you must run `build_runner` before the tests will compile. The generated `.mocks.dart` file will be missing or stale otherwise.
- **pump vs pumpAndSettle:** `tester.pump()` processes one frame. `tester.pumpAndSettle()` pumps until no more frames are scheduled (animations complete). Use `pump` for immediate state changes, `pumpAndSettle` when animations or timers are involved. Be careful with `pumpAndSettle` on infinite animations — it will time out.
- **MaterialApp wrapper:** Widget tests usually need the widget under test to be wrapped in `MaterialApp` (or `CupertinoApp`) to provide `MediaQuery`, `Directionality`, and other inherited widgets. Match the wrapper that existing tests use.
- **Async tests:** Dart tests support `async` natively. Just declare the test callback as `async` and `await` as needed.
- **Package imports:** Always use `package:` imports (e.g., `import 'package:my_app/src/models/user.dart';`), not relative paths, in test files. This matches how the source code resolves imports.
- **State management tests:** If the project uses Bloc, Riverpod, or Provider, check for specialized test utilities (`bloc_test`, `ProviderScope.overrides`, etc.) and follow the existing patterns.
