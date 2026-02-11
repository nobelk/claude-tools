# C# / .NET — Test & Fix Reference

## Detecting the Test Framework

Check in this order:

1. **Test project `.csproj` files** — look for package references:
   - `xunit` / `xunit.runner.visualstudio` → xUnit
   - `NUnit` / `NUnit3TestAdapter` → NUnit
   - `MSTest.TestFramework` / `MSTest.TestAdapter` → MSTest
2. **Using statements in existing tests** — `using Xunit;` vs `using NUnit.Framework;` vs `using Microsoft.VisualStudio.TestTools.UnitTesting;`
3. **Solution structure** — look for `*.Tests.csproj` or `*.UnitTests.csproj` projects

## Project Structure

C# test projects are separate projects that reference the source project:

```
Solution/
├── src/
│   └── MyApp/
│       ├── MyApp.csproj
│       └── Services/
│           └── Calculator.cs
└── tests/
    └── MyApp.Tests/
        ├── MyApp.Tests.csproj      ← References MyApp.csproj
        └── Services/
            └── CalculatorTests.cs   ← Mirrors source structure
```

When adding tests, place the test file in the location that mirrors the source file's path within the existing test project. If no test project exists, inform the user — creating a new test project requires `dotnet new xunit` (or nunit/mstest) and adding a project reference.

## xUnit Conventions

xUnit is the most common framework in modern .NET projects.

### Naming

- Test classes: `<ClassUnderTest>Tests` (e.g., `CalculatorTests`)
- Test methods: `<Method>_<Scenario>_<Expected>` (e.g., `Add_WithNegativeNumbers_ReturnsCorrectSum`)
- No `[TestClass]` attribute needed — xUnit discovers classes automatically

### Common Patterns

```csharp
using Xunit;

public class CalculatorTests
{
    // Simple fact (single case)
    [Fact]
    public void Divide_ByZero_ThrowsDivideByZeroException()
    {
        var calc = new Calculator();
        Assert.Throws<DivideByZeroException>(() => calc.Divide(1, 0));
    }

    // Theory with inline data (parameterized)
    [Theory]
    [InlineData(2, 3, 5)]
    [InlineData(-1, 1, 0)]
    [InlineData(0, 0, 0)]
    public void Add_WithValidInputs_ReturnsExpectedSum(int a, int b, int expected)
    {
        var calc = new Calculator();
        Assert.Equal(expected, calc.Add(a, b));
    }

    // Testing with constructor injection (xUnit creates new instance per test)
    private readonly Calculator _calc;

    public CalculatorTests()
    {
        _calc = new Calculator();
    }

    [Fact]
    public void Multiply_TwoPositives_ReturnsPositive()
    {
        var result = _calc.Multiply(3, 4);
        Assert.Equal(12, result);
    }
}
```

### Mocking with Moq (most common) or NSubstitute

```csharp
using Moq;
using Xunit;

public class OrderServiceTests
{
    [Fact]
    public void PlaceOrder_WithInvalidItem_ReturnsFalse()
    {
        var mockRepo = new Mock<IInventoryRepository>();
        mockRepo.Setup(r => r.IsInStock(It.IsAny<string>())).Returns(false);

        var service = new OrderService(mockRepo.Object);
        var result = service.PlaceOrder("invalid-item");

        Assert.False(result);
        mockRepo.Verify(r => r.IsInStock("invalid-item"), Times.Once);
    }
}
```

### Shared Setup with IClassFixture

```csharp
public class DatabaseTests : IClassFixture<DatabaseFixture>
{
    private readonly DatabaseFixture _fixture;

    public DatabaseTests(DatabaseFixture fixture)
    {
        _fixture = fixture;
    }

    [Fact]
    public void Query_ReturnsResults()
    {
        var results = _fixture.Db.Query("SELECT 1");
        Assert.NotEmpty(results);
    }
}
```

## NUnit Conventions

### Naming and Attributes

```csharp
using NUnit.Framework;

[TestFixture]
public class CalculatorTests
{
    private Calculator _calc;

    [SetUp]
    public void SetUp()
    {
        _calc = new Calculator();
    }

    [Test]
    public void Add_WithNegativeNumbers_ReturnsCorrectSum()
    {
        Assert.That(_calc.Add(-1, -2), Is.EqualTo(-3));
    }

    [TestCase(1, 2, 3)]
    [TestCase(-1, 1, 0)]
    public void Add_WithVariousInputs_ReturnsExpected(int a, int b, int expected)
    {
        Assert.That(_calc.Add(a, b), Is.EqualTo(expected));
    }

    [Test]
    public void Divide_ByZero_ThrowsException()
    {
        Assert.Throws<DivideByZeroException>(() => _calc.Divide(1, 0));
    }
}
```

## MSTest Conventions

### Naming and Attributes

```csharp
using Microsoft.VisualStudio.TestTools.UnitTesting;

[TestClass]
public class CalculatorTests
{
    private Calculator _calc;

    [TestInitialize]
    public void Setup()
    {
        _calc = new Calculator();
    }

    [TestMethod]
    public void Add_WithPositiveNumbers_ReturnsSum()
    {
        Assert.AreEqual(5, _calc.Add(2, 3));
    }

    [DataTestMethod]
    [DataRow(1, 2, 3)]
    [DataRow(-1, 1, 0)]
    public void Add_WithVariousInputs_ReturnsExpected(int a, int b, int expected)
    {
        Assert.AreEqual(expected, _calc.Add(a, b));
    }

    [TestMethod]
    [ExpectedException(typeof(DivideByZeroException))]
    public void Divide_ByZero_ThrowsException()
    {
        _calc.Divide(1, 0);
    }
}
```

## Running Tests

```bash
# Run all tests in the solution
dotnet test

# Run tests in a specific project
dotnet test tests/MyApp.Tests/MyApp.Tests.csproj

# Run with verbose output
dotnet test --verbosity normal

# Filter to specific tests
dotnet test --filter "FullyQualifiedName~CalculatorTests"
dotnet test --filter "FullyQualifiedName~Add_WithNegativeNumbers"

# Run and show detailed results
dotnet test --logger "console;verbosity=detailed"
```

## Common Pitfalls

- **Missing project reference:** The test project must have a `<ProjectReference>` to the source project in its `.csproj`. If you get "type or namespace not found" errors, check this first.
- **Internal visibility:** If the class under test is `internal`, the source project needs `[assembly: InternalsVisibleTo("MyApp.Tests")]` in an `AssemblyInfo.cs` or in the `.csproj` as `<InternalsVisibleTo Include="MyApp.Tests" />`.
- **Async tests:** For async methods, the test method should return `Task` and use `await`. In xUnit: `[Fact] public async Task MyTest()`. In NUnit: `[Test] public async Task MyTest()`.
- **Moq vs NSubstitute:** Don't mix mocking libraries. Check which one the project uses in its `.csproj` package references.
- **Build before test:** If the source code change doesn't compile, `dotnet test` will fail with build errors, not test errors. Run `dotnet build` first if unsure.
