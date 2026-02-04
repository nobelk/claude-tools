# Unit Test Strategy for Refactoring

## Table of Contents
1. [Pre-Refactoring: Characterization Tests](#pre-refactoring-characterization-tests)
2. [Mocking and Test Doubles](#mocking-and-test-doubles)
3. [Test Organization](#test-organization)
4. [Post-Refactoring: Test Updates](#post-refactoring-test-updates)
5. [Regression Verification Workflow](#regression-verification-workflow)

---

## Pre-Refactoring: Characterization Tests

Characterization tests capture existing behavior so refactoring can be verified against it. Write these for any public method that will be changed and lacks tests.

### Pattern

```csharp
[Fact]
public void CalculateTotal_ExistingBehavior_ReturnsExpectedResult()
{
    // Arrange — replicate production inputs
    var order = new Order
    {
        Items = new[] { new OrderItem { Price = 10m, Quantity = 2 } },
        DiscountCode = "SAVE10"
    };
    var sut = new OrderService(/* current real or stubbed deps */);

    // Act
    var result = sut.CalculateTotal(order);

    // Assert — lock in whatever the current output is
    Assert.Equal(18.0m, result);
}
```

### Guidelines
- Name these tests descriptively: `MethodName_Scenario_CurrentBehavior`.
- If the current behavior is buggy, still assert on it — fix the bug in a separate step after refactoring.
- Cover edge cases: null inputs, empty collections, boundary values, error paths.
- For methods with side effects (DB writes, HTTP calls), mock the external dependency and assert on the call pattern.

### Coverage Targets Before Refactoring
- Aim for test coverage of every public method that will be touched.
- Prioritize code with complex branching logic (high cyclomatic complexity).
- For legacy code that is hard to test directly, test at the nearest testable boundary (e.g., the calling service).

---

## Mocking and Test Doubles

### Preferred Framework
Use **Moq** or **NSubstitute** (match whatever the project already uses).

### When to Mock
- External services (HTTP clients, email senders, payment processors).
- Database access (repositories, DbContext).
- System clock (`TimeProvider`, `ISystemClock`).
- File system access.

### When NOT to Mock
- The class under test (never mock the SUT).
- Simple value objects and DTOs.
- Pure functions with no dependencies.
- In-memory alternatives exist (e.g., EF Core `InMemoryDatabase` for integration-level tests).

### Mock Setup Example

```csharp
[Fact]
public async Task ProcessOrder_ValidOrder_SendsConfirmationEmail()
{
    // Arrange
    var emailSender = new Mock<IEmailSender>();
    var repository = new Mock<IOrderRepository>();
    repository.Setup(r => r.SaveAsync(It.IsAny<Order>()))
              .ReturnsAsync(true);

    var sut = new OrderProcessor(repository.Object, emailSender.Object);

    // Act
    await sut.ProcessAsync(new Order { Id = 1, Total = 100m });

    // Assert
    emailSender.Verify(
        e => e.SendAsync(It.Is<EmailMessage>(m => m.Subject.Contains("confirmation"))),
        Times.Once);
}
```

---

## Test Organization

### Project Structure
```
Solution.sln
├── src/
│   ├── MyApp.Domain/
│   ├── MyApp.Application/
│   └── MyApp.Infrastructure/
└── tests/
    ├── MyApp.Domain.Tests/
    ├── MyApp.Application.Tests/
    └── MyApp.Infrastructure.Tests/
```

### File Naming
- Test file mirrors source file: `OrderService.cs` → `OrderServiceTests.cs`.
- One test class per production class.

### Test Method Naming
Use `MethodName_Scenario_ExpectedResult`:
- `CalculateTotal_WithDiscount_AppliesPercentageOff`
- `GetById_NonExistentId_ReturnsNull`
- `Validate_EmptyName_ThrowsArgumentException`

### Arrange-Act-Assert
- Separate each section with a blank line.
- One `Act` call per test.
- Prefer one logical assertion per test (multiple `Assert` calls are fine if they verify one outcome).

---

## Post-Refactoring: Test Updates

After each refactoring phase, tests may need updating. Follow these rules:

### Unchanged Behavior
- Existing characterization tests **must still pass without modification**.
- If a test breaks, the refactoring has changed behavior — investigate before updating the test.

### New Abstractions (Interfaces Extracted)
- Update test setup to mock the new interface instead of the old concrete class.
- The assertion logic should remain identical.

```csharp
// BEFORE refactoring — tested with concrete class
var sut = new OrderService(new FakeOrderRepository());

// AFTER refactoring — interface extracted, inject mock
var repo = new Mock<IOrderRepository>();
var sut = new OrderService(repo.Object);
```

### Design Pattern Introduction
- **Strategy pattern:** Add a test for each strategy implementation in isolation, plus a test that the context selects the right strategy.
- **Factory pattern:** Test that the factory returns the correct concrete type for each input.
- **Decorator pattern:** Test the decorator in isolation (verify it delegates to the inner instance and adds its behavior).
- **Mediator pattern:** Test each handler independently; test that the correct handler is invoked for each request type.

### Logging Verification
- Do not unit test log messages in most cases (they are an implementation detail).
- Exception: if a log message is a contractual part of observability (e.g., an audit log), verify it with a mock `ILogger<T>`.

### Deleted Code
- When dead code is removed, delete its corresponding tests.
- When a class is split into two, split its test class accordingly.

---

## Regression Verification Workflow

Execute this after every refactoring phase:

```bash
# 1. Build the solution — zero warnings
dotnet build /p:TreatWarningsAsErrors=true

# 2. Run all tests
dotnet test --logger "console;verbosity=detailed"

# 3. Check test count (should not decrease)
dotnet test --list-tests | wc -l

# 4. Optional: generate coverage report
dotnet test --collect:"XPlat Code Coverage"
reportgenerator -reports:**/coverage.cobertura.xml -targetdir:coveragereport
```

### Go/No-Go Criteria
- **Go:** All tests pass, test count same or higher, coverage same or higher.
- **No-Go:** Any test failure or coverage regression. Fix before proceeding to next phase.
- **Investigate:** Test count decreased — confirm tests were intentionally removed (dead code), not accidentally deleted.
