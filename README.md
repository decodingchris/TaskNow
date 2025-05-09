# TaskNow

A terminal to-do app that helps you focus on one task at a time.

## Why use TaskNow?

- Stay focused by seeing just your current task
- Add, complete, and manage tasks easily from the terminal
- No accounts, no clutter — just your tasks

## Requirements

- **Python 3.10 or higher**
- Compatible with Ubuntu/Linux systems

## Installation

Install TaskNow directly from PyPI:

```bash
pip install tasknow
```

## Commands

Add a task:

```bash
tasknow add "Write report"
```

See your current task:

```bash
tasknow
```

Mark it done:

```bash
tasknow done
```

List all tasks:

```bash
tasknow list # Also shows each task id
```

Remove a task:

```bash
tasknow remove 2 # Remove task with id: 2
```

Show completed tasks:

```bash
tasknow completed
```

Un-complete a task:

```bash
tasknow undone 3 # Un-complete task with id: 3
```

Edit a task:

```bash
tasknow edit 4 "New task description" # Edit task with id: 4
```

Show help:

```bash
tasknow help
```

## License

This project is licensed under the **MIT License**. See the [LICENSE](https://opensource.org/licenses/MIT) file for details.
