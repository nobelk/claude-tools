# Python — Test & Fix Reference

## Detecting the Test Framework

Check in this order:

1. **pyproject.toml** — look for `[tool.pytest]`, `[tool.pytest.ini_options]`, or a `pytest` dependency
2. **setup.cfg** — look for `[tool:pytest]`
3. **pytest.ini** or **conftest.py** — presence indicates pytest
4. **requirements.txt / requirements-dev.txt** — look for `pytest`, `unittest`, `nose`
5. **Existing test files** — `import pytest` vs `import unittest` vs `from unittest import`

If no framework is detected, default to **pytest** — it's the most common and requires the least boilerplate.

## pytest Conventions

### File and Naming

- Test files: `test_<module>.py` or `<module>_test.py` (match whichever the project uses)
- Test functions: `test_<description>` (snake_case)
- Test classes (if used): `Test<ClassName>` with methods `test_<description>`
- Place tests to mirror source structure: `src/utils/parser.py` → `tests/utils/test_parser.py`

### Common Patterns

```python
# Simple test function — the most common pattern
def test_parse_handles_empty_string():
    result = parse("")
    assert result is None

# Parameterized tests for multiple inputs
import pytest

@pytest.mark.parametrize("input_val,expected", [
    ("", None),
    ("  ", None),
    ("valid", "valid"),
])
def test_parse_various_inputs(input_val, expected):
    assert parse(input_val) == expected

# Fixtures for setup
@pytest.fixture
def sample_config():
    return {"key": "value", "nested": {"a": 1}}

def test_config_lookup(sample_config):
    assert lookup(sample_config, "nested.a") == 1

# Testing exceptions
def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

# Mocking
from unittest.mock import patch, MagicMock

def test_fetch_data_retries_on_failure():
    with patch("module.requests.get") as mock_get:
        mock_get.side_effect = [ConnectionError(), MagicMock(status_code=200)]
        result = fetch_data("http://example.com")
        assert mock_get.call_count == 2
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_parser.py

# Run specific test function
pytest tests/test_parser.py::test_parse_handles_empty_string

# Run with verbose output (useful for verifying failures)
pytest -v tests/test_parser.py

# Run tests matching a keyword
pytest -k "parse" -v
```

### conftest.py

If the project uses `conftest.py` for shared fixtures, check for existing fixtures you can reuse before creating new ones. Add new shared fixtures to `conftest.py` only if they'll be used across multiple test files.

## unittest Conventions

### File and Naming

- Test files: `test_<module>.py`
- Test classes: `class Test<Feature>(unittest.TestCase)`
- Test methods: `def test_<description>(self)`

### Common Patterns

```python
import unittest

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_parse_returns_none_for_empty_input(self):
        self.assertIsNone(self.parser.parse(""))

    def test_parse_raises_on_invalid_input(self):
        with self.assertRaises(ValueError):
            self.parser.parse(None)

    def tearDown(self):
        self.parser.close()
```

### Running Tests

```bash
# Run all tests
python -m unittest discover

# Run specific test file
python -m unittest tests.test_parser

# Run specific test class or method
python -m unittest tests.test_parser.TestParser.test_parse_returns_none_for_empty_input
```

## Common Pitfalls

- **Import paths:** Python import issues are the #1 cause of "test fails for the wrong reason." Make sure the test can import the module under test. Check for `__init__.py` files, `sys.path` manipulation in conftest, or `src` layout configurations in `pyproject.toml`.
- **Mocking the wrong target:** Always mock where the name is *looked up*, not where it's *defined*. If `module_a.py` does `from module_b import helper`, mock `module_a.helper`, not `module_b.helper`.
- **Fixture scope:** pytest fixtures default to `function` scope (recreated per test). If existing tests use `session` or `module` scope, respect that.
- **Async tests:** If the code under test is async, use `pytest-asyncio` with `@pytest.mark.asyncio` or the project's async test pattern.
