"""Unit tests for TaskNow task manager."""
import pytest
import json
import os
import threading
from unittest.mock import mock_open, patch
from main import TaskManager, TASKS_FILE

@pytest.fixture
def task_manager(tmp_path):
    """Fixture providing a TaskManager instance with temp file."""
    original_file = TASKS_FILE
    temp_file = tmp_path / "tasks.json"
    
    # Patch the TASKS_FILE constant
    with patch('main.TASKS_FILE', str(temp_file)):
        yield TaskManager()
    
    # Cleanup
    if os.path.exists(original_file):
        os.remove(original_file)

def test_initialization_with_no_file(task_manager):
    """Test initialization when no tasks file exists."""
    assert task_manager.tasks == []
    assert task_manager.current_task_id is None

def test_initialization_with_empty_file(task_manager):
    """Test initialization with empty but valid JSON file."""
    with open(TASKS_FILE, 'w') as f:
        json.dump({"tasks": [], "current_task_id": None}, f)
    
    tm = TaskManager()
    assert tm.tasks == []
    assert tm.current_task_id is None

def test_initialization_with_corrupted_file(task_manager):
    """Test initialization with corrupted JSON file."""
    with open(TASKS_FILE, 'w') as f:
        f.write("invalid json")
    
    tm = TaskManager()
    assert tm.tasks == []
    assert tm.current_task_id is None

def test_add_task(task_manager):
    """Test adding a new task."""
    task_manager.add_task("Test task 1")
    assert len(task_manager.tasks) == 1
    assert task_manager.tasks[0]['description'] == "Test task 1"
    assert not task_manager.tasks[0]['completed']
    assert task_manager.current_task_id == 1

def test_add_multiple_tasks(task_manager):
    """Test adding multiple tasks."""
    task_manager.add_task("Task 1")
    task_manager.add_task("Task 2")
    assert len(task_manager.tasks) == 2
    assert task_manager.tasks[0]['id'] == 1
    assert task_manager.tasks[1]['id'] == 2
    assert task_manager.current_task_id == 1  # First task remains current

def test_complete_current_task(task_manager):
    """Test completing the current task."""
    task_manager.add_task("Task 1")
    task_manager.add_task("Task 2")
    task_manager.complete_current_task()
    
    # Verify task 1 is completed
    assert task_manager.tasks[0]['completed']
    # Current task should now be task 2
    assert task_manager.current_task_id == 2

def test_complete_last_task(task_manager):
    """Test completing the last task."""
    task_manager.add_task("Task 1")
    task_manager.complete_current_task()
    
    assert task_manager.tasks[0]['completed']
    assert task_manager.current_task_id is None

def test_complete_with_no_current_task(task_manager, capsys):
    """Test completing when no current task exists."""
    task_manager.complete_current_task()
    captured = capsys.readouterr()
    assert "No current task to complete" in captured.out

def test_edit_task(task_manager):
    """Test editing a task description."""
    task_manager.add_task("Original description")
    task_manager.edit_task(1, "Updated description")
    assert task_manager.tasks[0]['description'] == "Updated description"

def test_edit_nonexistent_task(task_manager, capsys):
    """Test editing a task that doesn't exist."""
    task_manager.edit_task(999, "New description")
    captured = capsys.readouterr()
    assert "Error: Task 999 not found" in captured.out

def test_get_current_task(task_manager):
    """Test getting the current task."""
    task_manager.add_task("Task 1")
    task_manager.add_task("Task 2")
    current = task_manager.get_current_task()
    assert current['id'] == 1
    assert current['description'] == "Task 1"

def test_get_current_task_when_none(task_manager):
    """Test getting current task when none exists."""
    assert task_manager.get_current_task() is None

def test_list_tasks(task_manager):
    """Test listing incomplete tasks."""
    task_manager.add_task("Task 1")
    task_manager.add_task("Task 2")
    task_manager.complete_current_task()  # Complete task 1
    incomplete = task_manager.list_tasks()
    assert len(incomplete) == 1
    assert incomplete[0]['id'] == 2

def test_remove_task(task_manager):
    """Test removing a task."""
    task_manager.add_task("Task 1")
    task_manager.add_task("Task 2")
    task_manager.remove_task(1)
    assert len(task_manager.tasks) == 1
    assert task_manager.tasks[0]['id'] == 2

def test_remove_current_task(task_manager):
    """Test removing the current task."""
    task_manager.add_task("Task 1")
    task_manager.add_task("Task 2")
    task_manager.remove_task(1)
    assert task_manager.current_task_id == 2

def test_remove_nonexistent_task(task_manager, capsys):
    """Test removing a task that doesn't exist."""
    task_manager.remove_task(999)
    captured = capsys.readouterr()
    assert "Error: Task 999 not found" in captured.out

def test_list_completed_tasks(task_manager):
    """Test listing completed tasks."""
    task_manager.add_task("Task 1")
    task_manager.add_task("Task 2")
    task_manager.complete_current_task()
    completed = task_manager.list_completed_tasks()
    assert len(completed) == 1
    assert completed[0]['id'] == 1

def test_reopen_task(task_manager):
    """Test reopening a completed task."""
    task_manager.add_task("Task 1")
    task_manager.complete_current_task()
    task_manager.reopen_task(1)
    assert not task_manager.tasks[0]['completed']
    assert task_manager.current_task_id == 1

def test_reopen_nonexistent_task(task_manager, capsys):
    """Test reopening a task that doesn't exist."""
    task_manager.reopen_task(999)
    captured = capsys.readouterr()
    assert "Error: Task 999 not found" in captured.out

def test_reopen_uncompleted_task(task_manager, capsys):
    """Test reopening a task that isn't completed."""
    task_manager.add_task("Task 1")
    task_manager.reopen_task(1)
    captured = capsys.readouterr()
    assert "Error: Task 1 is not completed" in captured.out

def test_load_tasks_with_first_incomplete(tmp_path):
    """Test _load_tasks sets first incomplete task as current."""
    corrupted_file = tmp_path / "tasks.json"
    test_data = {
        "tasks": [
            {"id": 1, "description": "Task 1", "completed": True},
            {"id": 2, "description": "Task 2", "completed": False},
            {"id": 3, "description": "Task 3", "completed": False}
        ],
        "current_task_id": None
    }
    corrupted_file.write_text(json.dumps(test_data))
    
    with patch('main.TASKS_FILE', str(corrupted_file)):
        tm = TaskManager()
        # This should trigger line 33
        assert tm.current_task_id == 2

def test_complete_current_task_with_next_selection(task_manager):
    """Test completing current task selects next incomplete task."""
    task_manager.add_task("Task 1")
    task_manager.add_task("Task 2")
    task_manager.add_task("Task 3")
    task_manager.complete_current_task()  # Complete task 1
    assert task_manager.current_task_id == 2
    task_manager.complete_current_task()  # Complete task 2
    assert task_manager.current_task_id == 3

def test_get_current_task_updates_id(task_manager):
    """Test get_current_task updates current_task_id to earliest incomplete."""
    task_manager.add_task("Task 1")
    task_manager.add_task("Task 2")
    task_manager.complete_current_task()  # Complete task 1
    task_manager.current_task_id = 2  # Manually set to task 2
    
    # Should reset to earliest incomplete (task 2)
    current = task_manager.get_current_task()
    assert current['id'] == 2
    assert task_manager.current_task_id == 2

def test_remove_task_with_next_selection(task_manager):
    """Test removing current task selects next incomplete task."""
    task_manager.add_task("Task 1")
    task_manager.add_task("Task 2")
    task_manager.add_task("Task 3")
    task_manager.remove_task(1)
    assert task_manager.current_task_id == 2
    task_manager.remove_task(2)
    assert task_manager.current_task_id == 3

def test_cli_add_task(capsys):
    """Test CLI add task command."""
    with patch('sys.argv', ['main.py', 'add', 'Test', 'task']):
        from main import main
        main()
    
    captured = capsys.readouterr()
    assert "Added task: Test task" in captured.out
    assert os.path.exists(TASKS_FILE)

def test_cli_show_task(capsys, task_manager):
    """Test CLI show task command."""
    task_manager.add_task("Test task")
    with patch('sys.argv', ['main.py', 'show']):
        from main import main
        main()
    
    captured = capsys.readouterr()
    assert "Current task: Test task" in captured.out

def test_cli_complete_task(capsys, task_manager):
    """Test CLI complete task command."""
    task_manager.add_task("Test task")
    with patch('sys.argv', ['main.py', 'done']):
        from main import main
        main()
    
    captured = capsys.readouterr()
    assert "Completed task: Test task" in captured.out

def test_concurrent_add_tasks(task_manager):
    """Test concurrent task additions."""
    import threading
    
    def add_tasks(start, end):
        for i in range(start, end):
            task_manager.add_task(f"Task {i}")
    
    # Create two threads adding tasks concurrently
    t1 = threading.Thread(target=add_tasks, args=(1, 101))
    t2 = threading.Thread(target=add_tasks, args=(501, 601))
    
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
    # Verify all tasks were added without conflicts
    assert len(task_manager.tasks) == 200
    assert len(set(t['id'] for t in task_manager.tasks)) == 200  # All IDs unique

def test_concurrent_complete_tasks(task_manager):
    """Test concurrent task completions."""
    # Add initial tasks
    for i in range(1, 101):
        task_manager.add_task(f"Task {i}")
    
    def complete_tasks():
        while True:
            current = task_manager.get_current_task()
            if not current:
                break
            task_manager.complete_current_task()
    
    # Create multiple threads completing tasks
    threads = [threading.Thread(target=complete_tasks) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    # Verify all tasks were completed
    assert all(t['completed'] for t in task_manager.tasks)

def test_json_decode_error_handling(capsys, tmp_path):
    """Test handling of corrupted JSON file with detailed error message."""
    corrupted_file = tmp_path / "corrupted_tasks.json"
    corrupted_file.write_text("{invalid json}")
    
    # Patch TASKS_FILE to point to corrupted file
    with patch('main.TASKS_FILE', str(corrupted_file)):
        tm = TaskManager()
        captured = capsys.readouterr()
        print(f"Captured output: {captured.out}")  # Debug print
        assert "Error: Corrupted tasks file" in captured.out  # Check stdout
        assert tm.tasks == []
        assert tm.current_task_id is None
    assert tm.tasks == []
    assert tm.current_task_id is None

def test_complete_current_task_error_message(task_manager, capsys):
    """Test error message when current task doesn't exist."""
    # Set invalid current task ID
    task_manager.current_task_id = 999
    task_manager.complete_current_task()
    captured = capsys.readouterr()
    assert "Error: Current task not found" in captured.out

def test_get_current_task_updates_invalid_current(task_manager):
    """Test get_current_task updates invalid current_task_id."""
    task_manager.add_task("Task 1")
    task_manager.add_task("Task 2")
    task_manager.complete_current_task()  # Complete task 1
    task_manager.current_task_id = 999  # Set invalid ID
    
    # Should reset to earliest incomplete (task 2)
    current = task_manager.get_current_task()
    assert current['id'] == 2
    assert task_manager.current_task_id == 2

def test_cli_error_handling(capsys):
    """Test CLI error handling for invalid commands."""
    # Test invalid command and handle SystemExit
    with patch('sys.argv', ['main.py', 'invalid']):
        from main import main
        with pytest.raises(SystemExit):
            main()
    
    captured = capsys.readouterr()
    assert "invalid choice" in captured.err  # Check stderr for error message

def test_cli_exception_handling(capsys):
    """Test CLI generic exception handler coverage."""
    with patch('sys.argv', ['main.py', 'show']):
        from main import TaskManager, main
        # Patch get_current_task to raise error after TaskManager is created
        with patch.object(TaskManager, 'get_current_task', side_effect=RuntimeError("Simulated error")):
            main()
    
    captured = capsys.readouterr()
    combined_output = captured.out + captured.err
    assert "Error: Simulated error" in combined_output


def test_cli_default_to_show(capsys, tmp_path):
    """Test CLI defaults to showing current task when no command is given."""
    # Patch TASKS_FILE to use a temp file
    temp_file = tmp_path / "tasks.json"
    with patch('main.TASKS_FILE', str(temp_file)):
        from main import TaskManager, main as cli_main

        # Add a task so there is something to show
        manager = TaskManager()
        manager.add_task("Default show task")

        # Simulate running CLI with no arguments
        with patch('sys.argv', ['main.py']):
            cli_main()

        captured = capsys.readouterr()
        assert "Current task: Default show task" in captured.out


def test_cli_help_command(capsys):
    """Test the help command prints help message."""
    from main import main as cli_main

    # Simulate running 'tasknow help'
    with patch('sys.argv', ['main.py', 'help']):
        cli_main()

    captured = capsys.readouterr()
    assert "usage: main.py" in captured.out
    assert "Show current task" in captured.out
    assert "help" in captured.out