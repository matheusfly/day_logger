import tkinter as tk
from tkinter import ttk, messagebox
import json
import csv
import os

# Load and save functions for each dataset
def load_data(filename):
    if not os.path.exists(filename):
        return {}
    with open(filename, 'r') as file:
        return json.load(file)

def save_data(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def load_tasks(filename='data/tasks.csv'):
    tasks = []
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["IsObligation"] = row["IsObligation"] == "true"
                tasks.append(row)
    return tasks

def save_tasks(tasks, filename='data/tasks.csv'):
    with open(filename, 'w', newline='') as file:
        fieldnames = ["TaskID", "ReportID", "Title", "Description", "IsObligation", "Status", "RelatedDreamID", "RelatedObjectiveID", "RelatedGoalID"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for task in tasks:
            task["IsObligation"] = "true" if task["IsObligation"] else "false"
            writer.writerow(task)

# Main GUI class
class DayLoggerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Day Logger")
        self.geometry("600x400")
        
        # Load data
        self.dreams = load_data('data/dreams.json').get("dreams", [])
        self.objectives = load_data('data/objectives.json').get("objectives", [])
        self.goals = load_data('data/goals.json').get("goals", [])
        self.daily_reports = load_data('data/daily_reports.json').get("daily_reports", [])
        self.tasks = load_tasks()

        # Initialize notebook and tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')
        
        self.create_dreams_tab()
        self.create_objectives_tab()
        self.create_goals_tab()
        self.create_tasks_tab()
        self.create_daily_reports_tab()

    def create_dreams_tab(self):
        self.dreams_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dreams_tab, text='Dreams')
        
        ttk.Label(self.dreams_tab, text="Title:").grid(row=0, column=0, padx=10, pady=5)
        self.dream_title = ttk.Entry(self.dreams_tab)
        self.dream_title.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.dreams_tab, text="Description:").grid(row=1, column=0, padx=10, pady=5)
        self.dream_description = ttk.Entry(self.dreams_tab)
        self.dream_description.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.dreams_tab, text="Start Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5)
        self.dream_start_date = ttk.Entry(self.dreams_tab)
        self.dream_start_date.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self.dreams_tab, text="End Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5)
        self.dream_end_date = ttk.Entry(self.dreams_tab)
        self.dream_end_date.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(self.dreams_tab, text="Supervision Frequency:").grid(row=4, column=0, padx=10, pady=5)
        self.dream_supervision_frequency = ttk.Entry(self.dreams_tab)
        self.dream_supervision_frequency.grid(row=4, column=1, padx=10, pady=5)

        self.add_dream_button = ttk.Button(self.dreams_tab, text="Add Dream", command=self.add_dream)
        self.add_dream_button.grid(row=5, column=0, columnspan=2, pady=10)
    
    def add_dream(self):
        title = self.dream_title.get()
        description = self.dream_description.get()
        start_date = self.dream_start_date.get()
        end_date = self.dream_end_date.get()
        supervision_frequency = self.dream_supervision_frequency.get()

        new_dream_id = max([dream["DreamID"] for dream in self.dreams], default=0) + 1
        new_dream = {
            "DreamID": new_dream_id,
            "Title": title,
            "Description": description,
            "StartDate": start_date,
            "EndDate": end_date,
            "SupervisionFrequency": supervision_frequency
        }

        self.dreams.append(new_dream)
        save_data('data/dreams.json', {"dreams": self.dreams})
        messagebox.showinfo("Success", "Dream added successfully")

        # Clear inputs
        self.dream_title.delete(0, tk.END)
        self.dream_description.delete(0, tk.END)
        self.dream_start_date.delete(0, tk.END)
        self.dream_end_date.delete(0, tk.END)
        self.dream_supervision_frequency.delete(0, tk.END)

    def create_objectives_tab(self):
        self.objectives_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.objectives_tab, text='Objectives')
        
        ttk.Label(self.objectives_tab, text="Dream ID:").grid(row=0, column=0, padx=10, pady=5)
        self.objective_dream_id = ttk.Entry(self.objectives_tab)
        self.objective_dream_id.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.objectives_tab, text="Title:").grid(row=1, column=0, padx=10, pady=5)
        self.objective_title = ttk.Entry(self.objectives_tab)
        self.objective_title.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.objectives_tab, text="Description:").grid(row=2, column=0, padx=10, pady=5)
        self.objective_description = ttk.Entry(self.objectives_tab)
        self.objective_description.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self.objectives_tab, text="Start Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5)
        self.objective_start_date = ttk.Entry(self.objectives_tab)
        self.objective_start_date.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(self.objectives_tab, text="End Date (YYYY-MM-DD):").grid(row=4, column=0, padx=10, pady=5)
        self.objective_end_date = ttk.Entry(self.objectives_tab)
        self.objective_end_date.grid(row=4, column=1, padx=10, pady=5)

        ttk.Label(self.objectives_tab, text="Review Frequency:").grid(row=5, column=0, padx=10, pady=5)
        self.objective_review_frequency = ttk.Entry(self.objectives_tab)
        self.objective_review_frequency.grid(row=5, column=1, padx=10, pady=5)

        self.add_objective_button = ttk.Button(self.objectives_tab, text="Add Objective", command=self.add_objective)
        self.add_objective_button.grid(row=6, column=0, columnspan=2, pady=10)

    def add_objective(self):
        dream_id = int(self.objective_dream_id.get())
        title = self.objective_title.get()
        description = self.objective_description.get()
        start_date = self.objective_start_date.get()
        end_date = self.objective_end_date.get()
        review_frequency = self.objective_review_frequency.get()

        new_objective_id = max([obj["ObjectiveID"] for obj in self.objectives], default=0) + 1
        new_objective = {
            "ObjectiveID": new_objective_id,
            "DreamID": dream_id,
            "Title": title,
            "Description": description,
            "StartDate": start_date,
            "EndDate": end_date,
            "ReviewFrequency": review_frequency
        }

        self.objectives.append(new_objective)
        save_data('data/objectives.json', {"objectives": self.objectives})
        messagebox.showinfo("Success", "Objective added successfully")

        # Clear inputs
        self.objective_dream_id.delete(0, tk.END)
        self.objective_title.delete(0, tk.END)
        self.objective_description.delete(0, tk.END)
        self.objective_start_date.delete(0, tk.END)
        self.objective_end_date.delete(0, tk.END)
        self.objective_review_frequency.delete(0, tk.END)

    def create_goals_tab(self):
        self.goals_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.goals_tab, text='Goals')
        
        ttk.Label(self.goals_tab, text="Objective ID:").grid(row=0, column=0, padx=10, pady=5)
        self.goal_objective_id = ttk.Entry(self.goals_tab)
        self.goal_objective_id.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.goals_tab, text="Title:").grid(row=1, column=0, padx=10, pady=5)
        self.goal_title = ttk.Entry(self.goals_tab)
        self.goal_title.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.goals_tab, text="Description:").grid(row=2, column=0, padx=10, pady=5)
        self.goal_description = ttk.Entry(self.goals_tab)
        self.goal_description.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self.goals_tab, text="Start Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5)
        self.goal_start_date = ttk.Entry(self.goals_tab)
        self.goal_start_date.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(self.goals_tab, text="End Date (YYYY-MM-DD):").grid(row=4, column=0, padx=10, pady=5)
        self.goal_end_date = ttk.Entry(self.goals_tab)
        self.goal_end_date.grid(row=4, column=1, padx=10, pady=5)

        ttk.Label(self.goals_tab, text="Review Frequency:").grid(row=5, column=0, padx=10, pady=5)
        self.goal_review_frequency = ttk.Entry(self.goals_tab)
        self.goal_review_frequency.grid(row=5, column=1, padx=10, pady=5)

        self.add_goal_button = ttk.Button(self.goals_tab, text="Add Goal", command=self.add_goal)
        self.add_goal_button.grid(row=6, column=0, columnspan=2, pady=10)

    def add_goal(self):
        objective_id = int(self.goal_objective_id.get())
        title = self.goal_title.get()
        description = self.goal_description.get()
        start_date = self.goal_start_date.get()
        end_date = self.goal_end_date.get()
        review_frequency = self.goal_review_frequency.get()

        new_goal_id = max([goal["GoalID"] for goal in self.goals], default=0) + 1
        new_goal = {
            "GoalID": new_goal_id,
            "ObjectiveID": objective_id,
            "Title": title,
            "Description": description,
            "StartDate": start_date,
            "EndDate": end_date,
            "ReviewFrequency": review_frequency
        }

        self.goals.append(new_goal)
        save_data('data/goals.json', {"goals": self.goals})
        messagebox.showinfo("Success", "Goal added successfully")

        # Clear inputs
        self.goal_objective_id.delete(0, tk.END)
        self.goal_title.delete(0, tk.END)
        self.goal_description.delete(0, tk.END)
        self.goal_start_date.delete(0, tk.END)
        self.goal_end_date.delete(0, tk.END)
        self.goal_review_frequency.delete(0, tk.END)

    def create_tasks_tab(self):
        self.tasks_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.tasks_tab, text='Tasks')
        
        ttk.Label(self.tasks_tab, text="Report ID:").grid(row=0, column=0, padx=10, pady=5)
        self.task_report_id = ttk.Entry(self.tasks_tab)
        self.task_report_id.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.tasks_tab, text="Title:").grid(row=1, column=0, padx=10, pady=5)
        self.task_title = ttk.Entry(self.tasks_tab)
        self.task_title.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.tasks_tab, text="Description:").grid(row=2, column=0, padx=10, pady=5)
        self.task_description = ttk.Entry(self.tasks_tab)
        self.task_description.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self.tasks_tab, text="Is Obligation:").grid(row=3, column=0, padx=10, pady=5)
        self.task_is_obligation = ttk.Checkbutton(self.tasks_tab)
        self.task_is_obligation.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(self.tasks_tab, text="Status:").grid(row=4, column=0, padx=10, pady=5)
        self.task_status = ttk.Entry(self.tasks_tab)
        self.task_status.grid(row=4, column=1, padx=10, pady=5)

        ttk.Label(self.tasks_tab, text="Related Dream ID:").grid(row=5, column=0, padx=10, pady=5)
        self.task_related_dream_id = ttk.Entry(self.tasks_tab)
        self.task_related_dream_id.grid(row=5, column=1, padx=10, pady=5)

        ttk.Label(self.tasks_tab, text="Related Objective ID:").grid(row=6, column=0, padx=10, pady=5)
        self.task_related_objective_id = ttk.Entry(self.tasks_tab)
        self.task_related_objective_id.grid(row=6, column=1, padx=10, pady=5)

        ttk.Label(self.tasks_tab, text="Related Goal ID:").grid(row=7, column=0, padx=10, pady=5)
        self.task_related_goal_id = ttk.Entry(self.tasks_tab)
        self.task_related_goal_id.grid(row=7, column=1, padx=10, pady=5)

        self.add_task_button = ttk.Button(self.tasks_tab, text="Add Task", command=self.add_task)
        self.add_task_button.grid(row=8, column=0, columnspan=2, pady=10)

    def add_task(self):
        report_id = int(self.task_report_id.get())
        title = self.task_title.get()
        description = self.task_description.get()
        is_obligation = self.task_is_obligation.instate(['selected'])
        status = self.task_status.get()
        related_dream_id = int(self.task_related_dream_id.get())
        related_objective_id = int(self.task_related_objective_id.get())
        related_goal_id = int(self.task_related_goal_id.get())

        new_task_id = max([int(task["TaskID"]) for task in self.tasks], default=0) + 1
        new_task = {
            "TaskID": new_task_id,
            "ReportID": report_id,
            "Title": title,
            "Description": description,
            "IsObligation": is_obligation,
            "Status": status,
            "RelatedDreamID": related_dream_id,
            "RelatedObjectiveID": related_objective_id,
            "RelatedGoalID": related_goal_id
        }

        self.tasks.append(new_task)
        save_tasks(self.tasks)
        messagebox.showinfo("Success", "Task added successfully")

        # Clear inputs
        self.task_report_id.delete(0, tk.END)
        self.task_title.delete(0, tk.END)
        self.task_description.delete(0, tk.END)
        self.task_is_obligation.state(['!selected'])
        self.task_status.delete(0, tk.END)
        self.task_related_dream_id.delete(0, tk.END)
        self.task_related_objective_id.delete(0, tk.END)
        self.task_related_goal_id.delete(0, tk.END)

    def create_daily_reports_tab(self):
        self.daily_reports_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.daily_reports_tab, text='Daily Reports')
        
        ttk.Label(self.daily_reports_tab, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=5)
        self.report_date = ttk.Entry(self.daily_reports_tab)
        self.report_date.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.daily_reports_tab, text="Morning Questions:").grid(row=1, column=0, padx=10, pady=5)
        self.report_morning_questions = tk.Text(self.daily_reports_tab, height=5, width=50)
        self.report_morning_questions.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.daily_reports_tab, text="Evening Questions:").grid(row=2, column=0, padx=10, pady=5)
        self.report_evening_questions = tk.Text(self.daily_reports_tab, height=5, width=50)
        self.report_evening_questions.grid(row=2, column=1, padx=10, pady=5)

        self.add_daily_report_button = ttk.Button(self.daily_reports_tab, text="Add Daily Report", command=self.add_daily_report)
        self.add_daily_report_button.grid(row=3, column=0, columnspan=2, pady=10)

    def add_daily_report(self):
        date = self.report_date.get()
        morning_questions = self.report_morning_questions.get("1.0", tk.END).strip()
        evening_questions = self.report_evening_questions.get("1.0", tk.END).strip()

        new_report_id = max([report["ReportID"] for report in self.daily_reports], default=0) + 1
        new_report = {
            "ReportID": new_report_id,
            "Date": date,
            "MorningQuestions": morning_questions,
            "EveningQuestions": evening_questions,
            "Tasks": []
        }

        self.daily_reports.append(new_report)
        save_data('data/daily_reports.json', {"daily_reports": self.daily_reports})
        messagebox.showinfo("Success", "Daily Report added successfully")

        # Clear inputs
        self.report_date.delete(0, tk.END)
        self.report_morning_questions.delete("1.0", tk.END)
        self.report_evening_questions.delete("1.0", tk.END)

if __name__ == "__main__":
    app = DayLoggerApp()
    app.mainloop()