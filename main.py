"""A small command-line to-do list with CSV persistence."""

import csv
from pathlib import Path


class ToDoList:
	"""Manage tasks in memory and save/load them as a CSV file."""

	def __init__(self, filename="todos.csv"):
		self.tasks = []
		self.filename = Path(filename)

	def add_one_task(self, title):
		"""Append a task title to the active list."""
		self.tasks.append(str(title))

	def print_list(self):
		"""Print the tasks with 1-based positions for user reference."""
		if not self.tasks:
			print("Your to-do list is empty.")
			return

		print("Your to-do list:")
		for position, title in enumerate(self.tasks, start=1):
			print(f"{position}. {title}")

	def delete_task(self, number_to_delete):
		"""Remove the task at a 1-based list position.

		Returns True when a task was removed, or False for an invalid position.
		"""
		try:
			position = int(number_to_delete)
		except (TypeError, ValueError):
			print("Please enter a valid task number.")
			return False

		if position < 1 or position > len(self.tasks):
			print("That task number is not in the list.")
			return False

		removed_task = self.tasks.pop(position - 1)
		print(f'Removed: "{removed_task}"')
		return True

	def save_todos(self):
		"""Write all tasks to a CSV file, replacing its previous contents."""
		with self.filename.open("w", newline="", encoding="utf-8") as todo_file:
			writer = csv.writer(todo_file)
			writer.writerow(["title"])
			writer.writerows([[task] for task in self.tasks])
		print(f"Saved {len(self.tasks)} task(s) to {self.filename}.")

	def load_todos(self):
		"""Load tasks from CSV, leaving the list unchanged if no file exists."""
		try:
			with self.filename.open("r", newline="", encoding="utf-8") as todo_file:
				rows = list(csv.reader(todo_file))
		except FileNotFoundError:
			print(f"No saved to-do list found at {self.filename}.")
			return

		# Accept the titled format written above, as well as one-column CSVs
		# without a header for compatibility with simple existing todo files.
		if rows and rows[0] == ["title"]:
			rows = rows[1:]
		self.tasks = [row[0] for row in rows if row]
		print(f"Loaded {len(self.tasks)} task(s) from {self.filename}.")


def run_cli():
	"""Run the interactive command-line menu."""
	todo_list = ToDoList()
	print("Welcome to your To-Do List!")

	while True:
		print("\nChoose an option:")
		print("1. Add a task")
		print("2. Show tasks")
		print("3. Delete a task")
		print("4. Save tasks")
		print("5. Load tasks")
		print("6. Exit")

		choice = input("Enter your choice (1-6): ").strip()

		if choice == "1":
			title = input("Enter the task: ").strip()
			if title:
				todo_list.add_one_task(title)
				print("Task added.")
			else:
				print("A task cannot be empty.")
		elif choice == "2":
			todo_list.print_list()
		elif choice == "3":
			todo_list.print_list()
			if todo_list.tasks:
				number = input("Enter the number of the task to delete: ").strip()
				todo_list.delete_task(number)
		elif choice == "4":
			todo_list.save_todos()
		elif choice == "5":
			todo_list.load_todos()
		elif choice == "6":
			print("Goodbye!")
			break
		else:
			print("Please choose a number from 1 to 6.")


if __name__ == "__main__":
	run_cli()