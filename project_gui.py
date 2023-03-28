import tkinter as tk
from tkinter import messagebox
from project import Project
from dynamodb import dynamodb_controller
import uuid


class ProjectManagerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.client = dynamodb_controller()
        self.title("Project Management Tool (Group 11)")
        self.geometry("800x600")

        self.projects = []

        self.create_widgets()
        self.update_project_list()

    def create_widgets(self):
        # 项目列表框
        self.project_list = tk.Listbox(self, width=100, height=20)
        self.project_list.grid(row=0, column=0, padx=10, pady=10)

        # 添加项目按钮
        self.add_button = tk.Button(self, text="New Project", command=self.add_project)
        self.add_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # 修改项目按钮
        self.edit_button = tk.Button(self, text="Edit Project", command=self.edit_project)
        self.edit_button.grid(row=1, column=0, padx=10, pady=10)

        # 删除项目按钮
        self.delete_button = tk.Button(self, text="Delete Project", command=self.delete_project)
        self.delete_button.grid(row=1, column=0, padx=10, pady=10, sticky="e")

    def update_project_list(self):
        self.project_list.delete(0, tk.END)
        self.projects.clear()
        response = self.client.scan_table()
        for rstr in response:
            self.projects.append(Project(rstr['id'], rstr['name'], rstr['description'], rstr['progress'], rstr['dueDate']))
            self.project_list.insert(tk.END, f"{rstr['name']} - {rstr['description']} - {rstr['progress']}% - {rstr['dueDate']}")

    def add_project(self):
        project_details = self.get_project_details()
        if project_details:
            uid, name, description, progress, dueDate = project_details
            self.client.save_plan(uid, name, description, progress, dueDate)
            self.projects.append(Project(uid, name, description, progress, dueDate))
            self.update_project_list()

    def edit_project(self):
        selected_index = self.project_list.curselection()
        if not selected_index:
            messagebox.showerror("You haven't select a project!")
            return
        project = self.projects[selected_index[0]]
        updated_project_details = self.get_project_details(project)
        if updated_project_details:
            uid, name, description, progress, dueDate = updated_project_details
            self.client.edit_plan(uid, name, description, progress, dueDate)
            project.update(uid, name, description, progress, dueDate)

            self.update_project_list()

    def delete_project(self):
        selected_index = self.project_list.curselection()
        if not selected_index:
            messagebox.showerror("You haven't select a project!!")
            return
        uid = self.projects[selected_index[0]].uid
        self.client.delete_plan(uid)
        self.projects.pop(selected_index[0])
        self.update_project_list()

    def get_project_details(self, project=None):
        dialog = ProjectDialog(self, project, self.client)
        self.wait_window(dialog)
        return dialog.result


class ProjectDialog(tk.Toplevel):
    def __init__(self, parent, project=None, client=None):
        super().__init__(parent)
        self.client = client
        self.title("Project Detail")
        self.geometry("400x300")

        self.result = None

        self.create_widgets()

        if project:
            self.uid = project.uid
            self.name_var.set(project.name)
            self.description_var.set(project.description)
            self.progress_var.set(project.progress)
            self.due_date_var.set(project.dueDate)
        else:
            self.uid = uuid.uuid4()

    def create_widgets(self):
        # 项目名称
        tk.Label(self, text="Project Name：").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.name_var = tk.StringVar()
        tk.Entry(self, textvariable=self.name_var).grid(row=0, column=1, padx=10, pady=10)

        # 项目描述
        tk.Label(self, text="Project Description：").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.description_var = tk.StringVar()
        tk.Entry(self, textvariable=self.description_var).grid(row=1, column=1, padx=10, pady=10)

        # 项目进度
        tk.Label(self, text="Project Progress（%）：").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.progress_var = tk.IntVar()
        tk.Entry(self, textvariable=self.progress_var).grid(row=2, column=1, padx=10, pady=10)

        # 截止日期
        tk.Label(self, text="Due Date：").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.due_date_var = tk.StringVar()
        tk.Entry(self, textvariable=self.due_date_var).grid(row=3, column=1, padx=10, pady=10)

        # 操作按钮
        self.save_button = tk.Button(self, text="Save", command=self.save_project)
        self.save_button.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        self.cancel_button = tk.Button(self, text="Cancel", command=self.cancel)
        self.cancel_button.grid(row=4, column=1, padx=10, pady=10, sticky="e")

    def save_project(self):
        name = self.name_var.get()
        description = self.description_var.get()
        progress = self.progress_var.get()
        dueDate = self.due_date_var.get()
        if not name or not description or progress < 0 or progress > 100:
            messagebox.showerror("Please check you input!")
            return
        self.result = (self.uid, name, description, progress, dueDate)

        self.destroy()
    def cancel(self):
        self.destroy()
