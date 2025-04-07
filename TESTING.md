# TaskNow Testing Documentation

## Running Tests

To run all tests:

```bash
pytest
```

To run tests with coverage report:

```bash
pytest --cov=.
```

To generate HTML coverage report:

```bash
pytest --cov=. --cov-report=html
```

## Test Organization

The test suite is organized into unit tests and integration tests:

### Unit Tests (`test_main.py`)

- Tests core `TaskManager` functionality
- Uses pytest fixtures for clean test environment
- Mocks file operations to prevent side effects
- Tests both success and error paths
- Includes concurrency testing

### Test Categories

1. **Initialization Tests**

   - Empty system initialization
   - Loading existing tasks
   - Handling corrupted files

2. **Task Management Tests**

   - Adding tasks
   - Completing tasks
   - Editing tasks
   - Removing tasks
   - Task listing
   - Task reopening

3. **Edge Cases**
   - Empty task list operations
   - Invalid task IDs
   - Concurrent access scenarios
   - File system errors

## Test Coverage

We maintain 100% test coverage. Coverage is monitored through:

1. Running coverage report:

   ```bash
   pytest --cov=. --cov-report=html
   ```

2. Viewing results:
   - Open `htmlcov/index.html` in browser
   - Review uncovered lines (highlighted in red)
   - Add tests for any uncovered code paths

## Writing New Tests

Follow these guidelines when adding new tests:

1. **Test Structure**

   - One behavior per test
   - Clear, descriptive test names
   - Detailed docstrings explaining purpose
   - Setup, action, assertion pattern

2. **Test Independence**

   - Use fixtures for setup/teardown
   - Don't rely on test execution order
   - Clean up all test artifacts

3. **Mocking**

   - Mock external dependencies
   - Use `@patch` for system calls
   - Verify mock interactions

4. **Edge Cases**
   - Test error conditions
   - Test boundary values
   - Test concurrent operations

## CI Integration

The test suite is designed for CI environments. Example GitHub Actions workflow:

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest --cov=. --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Concurrent Access Testing

The test suite includes tests for concurrent operations:

```python
def test_concurrent_access(task_manager):
    """Test concurrent task operations."""
    def add_tasks():
        for i in range(10):
            task_manager.add_task(f"Task {i}")

    def complete_tasks():
        for _ in range(10):
            if task_manager.get_current_task():
                task_manager.complete_current_task()

    # Run operations concurrently
    threads = [
        threading.Thread(target=add_tasks),
        threading.Thread(target=complete_tasks)
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()
```

## Test Environment Setup

1. Create virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure pytest in `pytest.ini`:

   ```ini
   [pytest]
   testpaths = test_main.py
   python_files = test_*.py
   python_functions = test_*
   ```

4. Configure coverage in `.coveragerc`:
   ```ini
   [run]
   source = .
   omit =
       venv/*
       .git/*
       */__pycache__/*
   ```
