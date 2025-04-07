# TaskNow

A minimalist terminal task manager that helps you focus on one task at a time, while still providing full task management capabilities.

## Features

- Single-task focus by default
- Simple command-based interface
- Full task list visibility when needed
- Completion tracking
- JSON-based data storage
- Linux/Ubuntu compatible

## Installation

### Using pip and setup.py

1. Clone or download this repository.
2. Navigate to the project directory.
3. Run:

```bash
pip install .
```

This will install TaskNow and make the `tasknow` command available globally.

### Requirements

- Python 3.10 or higher
- `setuptools` (installed automatically with pip)

## Usage

Add a new task:

```bash
tasknow add "Write documentation"
```

View your current task:

```bash
tasknow
```

Mark the current task as done:

```bash
tasknow done
```

List all tasks:

```bash
tasknow list
```

Remove a task:

```bash
tasknow remove 3
```

Show completed tasks:

```bash
tasknow completed
```

Un-complete a task:

```bash
tasknow undone 3
```

Edit a task:

```bash
tasknow edit 2 "New task description"
```

## Development

Run tests with:

```bash
pytest
```

Generate coverage report:

```bash
pytest --cov=.
```

## License

MIT License © Decoding Chris
