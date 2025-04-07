"""Integration tests for TaskNow CLI."""
import pytest
import os
from main import main as cli_main, TASKS_FILE
from unittest.mock import patch

@pytest.fixture(autouse=True)
def cleanup_files():
    """Cleanup test files after each test."""
    yield
    if os.path.exists(TASKS_FILE):
        os.remove(TASKS_FILE)

def test_show_command_no_tasks(capsys):
    """Test 'show' command with no tasks."""
    with patch('sys.argv', ['main.py', 'show']):
        cli_main()
    captured = capsys.readouterr()
    assert "No current task" in captured.out

def test_add_command(capsys):
    """Test adding a task."""
    with patch('sys.argv', ['main.py', 'add', 'Test', 'task']):
        cli_main()
    captured = capsys.readouterr()
    assert "Added task: Test task" in captured.out

def test_add_command_empty_description(capsys):
    """Test adding a task with empty description."""
    with patch('sys.argv', ['main.py', 'add']):
        cli_main()
    captured = capsys.readouterr()
    assert "Added task: " in captured.out

def test_show_command_with_task(capsys):
    """Test 'show' command with existing task."""
    with patch('sys.argv', ['main.py', 'add', 'Test', 'task']):
        cli_main()
    with patch('sys.argv', ['main.py', 'show']):
        cli_main()
    captured = capsys.readouterr()
    assert "Current task: Test task" in captured.out

def test_done_command(capsys):
    """Test completing the current task."""
    with patch('sys.argv', ['main.py', 'add', 'Task', '1']):
        cli_main()
    with patch('sys.argv', ['main.py', 'done']):
        cli_main()
    captured = capsys.readouterr()
    assert "Completed task: Task 1" in captured.out

def test_done_command_no_current_task(capsys):
    """Test 'done' command with no current task."""
    with patch('sys.argv', ['main.py', 'done']):
        cli_main()
    captured = capsys.readouterr()
    assert "No current task to complete" in captured.out

def test_list_command_empty(capsys):
    """Test 'list' command with no tasks."""
    with patch('sys.argv', ['main.py', 'list']):
        cli_main()
    captured = capsys.readouterr()
    assert "No tasks" in captured.out

def test_list_command_with_tasks(capsys):
    """Test 'list' command with tasks."""
    with patch('sys.argv', ['main.py', 'add', 'Task', '1']):
        cli_main()
    with patch('sys.argv', ['main.py', 'add', 'Task', '2']):
        cli_main()
    with patch('sys.argv', ['main.py', 'list']):
        cli_main()
    captured = capsys.readouterr()
    assert "1. [ ] Task 1" in captured.out
    assert "2. [ ] Task 2" in captured.out

def test_completed_command_empty(capsys):
    """Test 'completed' command with no completed tasks."""
    with patch('sys.argv', ['main.py', 'completed']):
        cli_main()
    captured = capsys.readouterr()
    assert "No completed tasks" in captured.out

def test_completed_command_with_tasks(capsys):
    """Test 'completed' command with completed tasks."""
    with patch('sys.argv', ['main.py', 'add', 'Task', '1']):
        cli_main()
    with patch('sys.argv', ['main.py', 'done']):
        cli_main()
    with patch('sys.argv', ['main.py', 'completed']):
        cli_main()
    captured = capsys.readouterr()
    assert "1. Task 1" in captured.out

def test_remove_command(capsys):
    """Test removing a task."""
    with patch('sys.argv', ['main.py', 'add', 'Task', '1']):
        cli_main()
    with patch('sys.argv', ['main.py', 'remove', '1']):
        cli_main()
    captured = capsys.readouterr()
    assert "Removed task 1" in captured.out

def test_remove_nonexistent_task(capsys):
    """Test removing a non-existent task."""
    with patch('sys.argv', ['main.py', 'remove', '999']):
        cli_main()
    captured = capsys.readouterr()
    assert "Error: Task 999 not found" in captured.out

def test_edit_command(capsys):
    """Test editing a task."""
    with patch('sys.argv', ['main.py', 'add', 'Original']):
        cli_main()
    with patch('sys.argv', ['main.py', 'edit', '1', 'Updated']):
        cli_main()
    captured = capsys.readouterr()
    assert "Updated task 1" in captured.out

def test_edit_nonexistent_task(capsys):
    """Test editing a non-existent task."""
    with patch('sys.argv', ['main.py', 'edit', '999', 'New']):
        cli_main()
    captured = capsys.readouterr()
    assert "Error: Task 999 not found" in captured.out

def test_undone_command(capsys):
    """Test marking a task as undone."""
    with patch('sys.argv', ['main.py', 'add', 'Task', '1']):
        cli_main()
    with patch('sys.argv', ['main.py', 'done']):
        cli_main()
    with patch('sys.argv', ['main.py', 'undone', '1']):
        cli_main()
    captured = capsys.readouterr()
    assert "Marked task 1 as undone" in captured.out

def test_undone_nonexistent_task(capsys):
    """Test marking a non-existent task as undone."""
    with patch('sys.argv', ['main.py', 'undone', '999']):
        cli_main()
    captured = capsys.readouterr()
    assert "Error: Task 999 not found" in captured.out