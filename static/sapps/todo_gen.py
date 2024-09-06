from openai import OpenAI, OpenAIError, RateLimitError, APIError, Timeout
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure the API key is loaded
try:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    exit(1)

# Dictionary to store goals and tasks
# Tasks will now be a tuple: (task_description, is_completed)
goals = {}

def view_goals():
    """View all goals and their tasks"""
    if not goals:
        print("No goals available.\n")
    else:
        for i, (goal, tasks) in enumerate(goals.items(), start=1):
            print(f"{i}. Goal: {goal}\n")
            for j, (task, is_completed) in enumerate(tasks, start=1):
                status = "[x]" if is_completed else "[ ]"
                print(f"  {j}. {status} {task}")
            print("\n")
    print("="*50, "\n")

def add_goal():
    """Add a new goal and generate tasks"""
    goal_name = input("Enter the goal: ").strip()
    num_tasks = input("Enter the number of tasks to generate (press Enter to leave it up to the AI): ").strip()

    if not num_tasks:
        num_tasks = "up to AI"
    else:
        try:
            num_tasks = int(num_tasks)
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return

    response = gpt_response(num_tasks, goal_name)

    if response.startswith("Error"):
        print(response)
    else:
        tasks = clean_task_output(response)
        goals[goal_name] = [(task, False) for task in tasks]  # Tasks are initially incomplete
        print(f"\nGoal '{goal_name}' added with the following tasks:\n")
        for i, task in enumerate(tasks, start=1):
            print(f"  [ ] Task {i}: {task}")
        print("\n" + "="*50)

def clean_task_output(response):
    """
    Clean the GPT response to remove any pre-existing numbering.
    """
    # Split the response by lines and remove the numbering at the start of each task
    cleaned_tasks = []
    for task in response.split("\n"):
        # Remove any leading numbering or bullet points like '1.', '2.', '-'
        cleaned_task = task.lstrip('0123456789.- ')
        if cleaned_task:  # Ensure it's not an empty line
            cleaned_tasks.append(cleaned_task)
    return cleaned_tasks

def select_goal():
    """Display a list of goals and allow user to select one by index"""
    if not goals:
        print("No goals available.\n")
        return None

    print("Select a goal:\n")
    for i, goal in enumerate(goals.keys(), start=1):
        print(f"{i}. {goal}")
    print()

    try:
        goal_index = int(input("Enter the goal number: ")) - 1
        if 0 <= goal_index < len(goals):
            return list(goals.keys())[goal_index]
        else:
            print("Invalid goal number.\n")
            return None
    except ValueError:
        print("Invalid input. Please enter a valid number.\n")
        return None

def edit_goal():
    """Edit tasks for a specific goal"""
    goal_name = select_goal()
    if not goal_name:
        return

    print(f"Editing tasks for '{goal_name}':\n")
    tasks = goals[goal_name]
    for i, (task, is_completed) in enumerate(tasks, start=1):
        status = "[x]" if is_completed else "[ ]"
        print(f"  {i}. {status} {task}")
    task_number = input("Enter the task number to edit: ")

    try:
        task_number = int(task_number)
        if 1 <= task_number <= len(tasks):
            new_task = input("Enter the new task description: ")
            tasks[task_number - 1] = (new_task, tasks[task_number - 1][1])  # Update the task description, keep completion status
            print("Task updated.\n")
        else:
            print("Invalid task number.\n")
    except ValueError:
        print("Invalid input. Please enter a valid number.\n")

def mark_task_complete():
    """Mark a specific task as completed"""
    goal_name = select_goal()
    if not goal_name:
        return

    print(f"Marking tasks for '{goal_name}':\n")
    tasks = goals[goal_name]
    for i, (task, is_completed) in enumerate(tasks, start=1):
        status = "[x]" if is_completed else "[ ]"
        print(f"  {i}. {status} {task}")

    task_number = input("Enter the task number to mark complete: ")

    try:
        task_number = int(task_number)
        if 1 <= task_number <= len(tasks):
            tasks[task_number - 1] = (tasks[task_number - 1][0], True)  # Mark the task as complete
            print("Task marked as complete.\n")
        else:
            print("Invalid task number.\n")
    except ValueError:
        print("Invalid input. Please enter a valid number.\n")

def delete_goal():
    """Delete a goal"""
    goal_name = select_goal()
    if not goal_name:
        return

    del goals[goal_name]
    print(f"Goal '{goal_name}' deleted.\n")

def gpt_response(num_tasks, goal_name):
    print("Generating tasks...")
    """
    Generate tasks for a given goal using OpenAI API.
    """
    try:
        # Customizing the AI's instruction based on whether num_tasks is provided
        if num_tasks == "up to AI":
            prompt = f"Generate tasks for the goal: {goal_name}. You decide how many tasks to generate."
        else:
            prompt = f"Generate {num_tasks} tasks for the goal: {goal_name}."

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": """You are a task generator for goals. keep each task short and concise"""},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    except RateLimitError:
        return "Error: Rate limit exceeded. Try again later."
    except Timeout:
        return "Error: Request timed out. Try again."
    except APIError as e:
        return f"Error: OpenAI API error: {e}"
    except OpenAIError as e:
        return f"Error: Unable to communicate with OpenAI API: {e}"


if __name__ == "__main__":

    while True:
        print("\n==================== AI TO-DO LIST ====================")
        print("1. View Goals")
        print("2. Add Goal")
        print("3. Edit Task")
        #TODO: edit goal
        print("4. Mark Task Complete")
        print("5. Delete Goal")
        print("6. Exit")
        print("="*50)
        user_input = input("Enter: ").strip()

        if user_input == "1":
            view_goals()
        elif user_input == "2":
            add_goal()
        elif user_input == "3":
            edit_goal()
        elif user_input == "4":
            mark_task_complete()
        elif user_input == "5":
            delete_goal()
        elif user_input == "6":
            print("Exiting program.")
            sys.exit()
        else:
            print("Invalid input. Please try again.\n")
