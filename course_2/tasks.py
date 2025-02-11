tasks = []

def add_task(task):
    tasks.append(task)
    return f"Task '{task}' added."

def remove_task(task):
    if task in tasks:
        tasks.remove(task)
        return f"Task '{task}' removed."
    else:
        return "Task not found."

def list_tasks():
    return tasks

# Example usage
print(add_task("Buy groceries"))
print(add_task("Read a book"))
print(list_tasks())
print(remove_task("Read a book"))
print(list_tasks())


# Exploratory Test cases
# Add task
# Delete task
# Remove non-existent task
# List tasks
# Add multiple tasks
# Delete multiple tasks
# Remove all tasks
# Add task with empty string
# Add task with special characters
# Add task with URL encoded characters
# Add task with script injection
# Add task with long name
# Add task with multiple spaces
# Add task with leading/trailing spaces