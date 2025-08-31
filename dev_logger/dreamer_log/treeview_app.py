import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os

import datetime
try:
    from tkcalendar import DateEntry
except ImportError:
    DateEntry = None

class MetasChildDialog(tk.Toplevel):
    def __init__(self, parent, sonhos_children, initial=None):
        super().__init__(parent)
        self.title("Add/Edit Metas Child")
        self.resizable(False, False)
        self.result = None

        self.fields = {}

        # Name
        ttk.Label(self, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.fields["name"] = self.name_entry

        # Title
        ttk.Label(self, text="Title:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.title_entry = ttk.Entry(self)
        self.title_entry.grid(row=1, column=1, padx=10, pady=5)
        self.fields["title"] = self.title_entry

        # Description
        ttk.Label(self, text="Description:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.description_entry = ttk.Entry(self)
        self.description_entry.grid(row=2, column=1, padx=10, pady=5)
        self.fields["description"] = self.description_entry

        # Dream selection (Combobox)
        ttk.Label(self, text="Link to Dream:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.dream_id_map = []
        dream_display_list = []
        for i, dream in enumerate(sonhos_children):
            dream_id = i + 1  # Assign DreamID as index+1 (or use a field if present)
            display = f"{dream_id}: {dream.get('name', '')} ({dream.get('title', '')})"
            dream_display_list.append(display)
            self.dream_id_map.append(dream_id)
        self.dream_var = tk.StringVar()
        self.dream_combobox = ttk.Combobox(self, textvariable=self.dream_var, values=dream_display_list, state="readonly")
        self.dream_combobox.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.fields["dream_id"] = self.dream_combobox

        # Start Date
        ttk.Label(self, text="Start Date:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.start_date_var = tk.StringVar()
        if DateEntry is not None:
            self.start_date_entry = DateEntry(self, textvariable=self.start_date_var, date_pattern="yyyy-mm-dd")
        else:
            self.start_date_entry = ttk.Entry(self, textvariable=self.start_date_var)
        self.start_date_entry.grid(row=4, column=1, padx=10, pady=5)
        self.fields["start_date"] = self.start_date_entry

        # Supervision Frequency (Radio Buttons)
        ttk.Label(self, text="Supervision Frequency:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.freq_var = tk.StringVar(value="biweekly")
        freq_frame = ttk.Frame(self)
        freq_frame.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        options = [("biweekly", "Biweekly"), ("monthly", "Monthly"), ("bi-monthly", "Bi-monthly")]
        for value, text in options:
            ttk.Radiobutton(freq_frame, text=text, variable=self.freq_var, value=value, command=self.update_end_date).pack(side="left")
        self.fields["supervision_frequency"] = self.freq_var

        # End Date (read-only)
        ttk.Label(self, text="End Date:").grid(row=6, column=0, padx=10, pady=5, sticky="e")
        self.end_date_var = tk.StringVar()
        self.end_date_entry = ttk.Entry(self, textvariable=self.end_date_var, state="readonly")
        self.end_date_entry.grid(row=6, column=1, padx=10, pady=5)
        self.fields["end_date"] = self.end_date_var

        # Bind events for dynamic end date calculation
        self.start_date_var.trace_add("write", lambda *args: self.update_end_date())

        # Pre-fill if editing
        if initial:
            self.name_entry.insert(0, initial.get("name", ""))
            self.title_entry.insert(0, initial.get("title", ""))
            self.description_entry.insert(0, initial.get("description", ""))
            if "dream_id" in initial and initial["dream_id"] in self.dream_id_map:
                idx = self.dream_id_map.index(initial["dream_id"])
                self.dream_combobox.current(idx)
            self.start_date_var.set(initial.get("start_date", ""))
            self.freq_var.set(initial.get("supervision_frequency", "biweekly"))
            self.end_date_var.set(initial.get("end_date", ""))

        button_frame = ttk.Frame(self)
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="OK", command=self.on_ok).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.on_cancel).pack(side="left", padx=5)

        self.bind("<Return>", lambda e: self.on_ok())
        self.bind("<Escape>", lambda e: self.on_cancel())
        self.grab_set()
        self.name_entry.focus_set()

    def update_end_date(self):
        start_date_str = self.start_date_var.get().strip()
        freq = self.freq_var.get()
        try:
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
            if freq == "biweekly":
                days = 14
                end_date = start_date + datetime.timedelta(days=days)
            elif freq == "monthly":
                # Add 1 month
                month = start_date.month + 1
                year = start_date.year + (month - 1) // 12
                month = (month - 1) % 12 + 1
                day = start_date.day
                try:
                    end_date = datetime.date(year, month, day)
                except ValueError:
                    import calendar
                    last_day = calendar.monthrange(year, month)[1]
                    end_date = datetime.date(year, month, last_day)
            elif freq == "bi-monthly":
                # Add 2 months
                month = start_date.month + 2
                year = start_date.year + (month - 1) // 12
                month = (month - 1) % 12 + 1
                day = start_date.day
                try:
                    end_date = datetime.date(year, month, day)
                except ValueError:
                    import calendar
                    last_day = calendar.monthrange(year, month)[1]
                    end_date = datetime.date(year, month, last_day)
            else:
                end_date = None
            if end_date:
                self.end_date_var.set(end_date.strftime("%Y-%m-%d"))
            else:
                self.end_date_var.set("")
        except Exception:
            self.end_date_var.set("")

    def on_ok(self):
        name = self.name_entry.get().strip()
        title = self.title_entry.get().strip()
        description = self.description_entry.get().strip()
        idx = self.dream_combobox.current()
        start_date = self.start_date_var.get().strip()
        end_date = self.end_date_var.get().strip()
        supervision_frequency = self.freq_var.get()
        if not name:
            messagebox.showerror("Error", "Name is required.", parent=self)
            return
        if idx == -1:
            messagebox.showerror("Error", "Please select a Dream to link.", parent=self)
            return
        if not start_date:
            messagebox.showerror("Error", "Start date is required and must be valid (YYYY-MM-DD).", parent=self)
            return
        if not end_date:
            messagebox.showerror("Error", "End date could not be calculated. Please check start date and frequency.", parent=self)
            return
        dream_id = self.dream_id_map[idx]
        self.result = {
            "name": name,
            "title": title,
            "description": description,
            "dream_id": dream_id,
            "start_date": start_date,
            "end_date": end_date,
            "supervision_frequency": supervision_frequency
        }
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()

class ObjetivosChildDialog(tk.Toplevel):
    def __init__(self, parent, metas_children, initial=None):
        super().__init__(parent)
        self.title("Add/Edit Objetivos Child")
        self.resizable(False, False)
        self.result = None

        self.fields = {}

        # Name
        ttk.Label(self, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.fields["name"] = self.name_entry

        # Title
        ttk.Label(self, text="Title:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.title_entry = ttk.Entry(self)
        self.title_entry.grid(row=1, column=1, padx=10, pady=5)
        self.fields["title"] = self.title_entry

        # Description
        ttk.Label(self, text="Description:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.description_entry = ttk.Entry(self)
        self.description_entry.grid(row=2, column=1, padx=10, pady=5)
        self.fields["description"] = self.description_entry

        # Metas selection (Combobox)
        ttk.Label(self, text="Link to Meta:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.metas_id_map = []
        metas_display_list = []
        for i, meta in enumerate(metas_children):
            metas_id = i + 1  # Assign metas_id as index+1 (or use a field if present)
            display = f"{metas_id}: {meta.get('name', '')} ({meta.get('title', '')})"
            metas_display_list.append(display)
            self.metas_id_map.append(metas_id)
        self.metas_var = tk.StringVar()
        self.metas_combobox = ttk.Combobox(self, textvariable=self.metas_var, values=metas_display_list, state="readonly")
        self.metas_combobox.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.fields["metas_id"] = self.metas_combobox

        # Start Date
        ttk.Label(self, text="Start Date:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.start_date_var = tk.StringVar()
        if DateEntry is not None:
            self.start_date_entry = DateEntry(self, textvariable=self.start_date_var, date_pattern="yyyy-mm-dd")
        else:
            self.start_date_entry = ttk.Entry(self, textvariable=self.start_date_var)
        self.start_date_entry.grid(row=4, column=1, padx=10, pady=5)
        self.fields["start_date"] = self.start_date_entry

        # Week Number Label
        self.week_label_var = tk.StringVar()
        ttk.Label(self, text="Week Number:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.week_label = ttk.Label(self, textvariable=self.week_label_var)
        self.week_label.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # End Date (read-only)
        ttk.Label(self, text="End Date:").grid(row=6, column=0, padx=10, pady=5, sticky="e")
        self.end_date_var = tk.StringVar()
        self.end_date_entry = ttk.Entry(self, textvariable=self.end_date_var, state="readonly")
        self.end_date_entry.grid(row=6, column=1, padx=10, pady=5)
        self.fields["end_date"] = self.end_date_var

        # Bind events for dynamic week/end date calculation
        self.start_date_var.trace_add("write", lambda *args: self.update_week_and_end_date())

        # Pre-fill if editing
        if initial:
            self.name_entry.insert(0, initial.get("name", ""))
            self.title_entry.insert(0, initial.get("title", ""))
            self.description_entry.insert(0, initial.get("description", ""))
            if "metas_id" in initial and initial["metas_id"] in self.metas_id_map:
                idx = self.metas_id_map.index(initial["metas_id"])
                self.metas_combobox.current(idx)
            self.start_date_var.set(initial.get("start_date", ""))
            self.end_date_var.set(initial.get("end_date", ""))
            # Week number will be set by update_week_and_end_date

        button_frame = ttk.Frame(self)
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="OK", command=self.on_ok).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.on_cancel).pack(side="left", padx=5)

        self.bind("<Return>", lambda e: self.on_ok())
        self.bind("<Escape>", lambda e: self.on_cancel())
        self.grab_set()
        self.name_entry.focus_set()

    def update_week_and_end_date(self):
        start_date_str = self.start_date_var.get().strip()
        try:
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
            week_number = start_date.isocalendar()[1]
            self.week_label_var.set(str(week_number))
            end_date = start_date + datetime.timedelta(days=7)
            self.end_date_var.set(end_date.strftime("%Y-%m-%d"))
        except Exception:
            self.week_label_var.set("")
            self.end_date_var.set("")

    def on_ok(self):
        name = self.name_entry.get().strip()
        title = self.title_entry.get().strip()
        description = self.description_entry.get().strip()
        idx = self.metas_combobox.current()
        start_date = self.start_date_var.get().strip()
        end_date = self.end_date_var.get().strip()
        week_number = self.week_label_var.get()
        if not name:
            messagebox.showerror("Error", "Name is required.", parent=self)
            return
        if idx == -1:
            messagebox.showerror("Error", "Please select a Meta to link.", parent=self)
            return
        if not start_date:
            messagebox.showerror("Error", "Start date is required and must be valid (YYYY-MM-DD).", parent=self)
            return
        if not end_date:
            messagebox.showerror("Error", "End date could not be calculated. Please check start date.", parent=self)
            return
        metas_id = self.metas_id_map[idx]
        self.result = {
            "name": name,
            "title": title,
            "description": description,
            "metas_id": metas_id,
            "start_date": start_date,
            "end_date": end_date,
            "week_number": week_number
        }
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()

class SonhosChildDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Sonhos Child")
        self.resizable(False, False)
        self.result = None

        self.fields = {}

        # Name, Title, Description
        labels = [
            ("name", "Name:"),
            ("title", "Title:"),
            ("description", "Description:"),
        ]
        for i, (key, label) in enumerate(labels):
            ttk.Label(self, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = ttk.Entry(self)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.fields[key] = entry

        # Start Date
        ttk.Label(self, text="Start Date:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.start_date_var = tk.StringVar()
        if DateEntry is not None:
            self.start_date_entry = DateEntry(self, textvariable=self.start_date_var, date_pattern="yyyy-mm-dd")
        else:
            self.start_date_entry = ttk.Entry(self, textvariable=self.start_date_var)
        self.start_date_entry.grid(row=3, column=1, padx=10, pady=5)
        self.fields["start_date"] = self.start_date_entry

        # Supervision Frequency (Radio Buttons)
        ttk.Label(self, text="Supervision Frequency:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.freq_var = tk.StringVar(value="Yearly")
        freq_frame = ttk.Frame(self)
        freq_frame.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        options = [("Yearly", "Yearly"), ("Semi-annual", "Semi-annual"), ("Quarterly", "Quarterly")]
        for text, value in options:
            ttk.Radiobutton(freq_frame, text=text, variable=self.freq_var, value=value, command=self.update_end_date).pack(side="left")
        self.fields["supervision_frequency"] = self.freq_var

        # End Date (read-only)
        ttk.Label(self, text="End Date:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.end_date_var = tk.StringVar()
        self.end_date_entry = ttk.Entry(self, textvariable=self.end_date_var, state="readonly")
        self.end_date_entry.grid(row=5, column=1, padx=10, pady=5)
        self.fields["end_date"] = self.end_date_var

        # Bind events for dynamic end date calculation
        self.start_date_var.trace_add("write", lambda *args: self.update_end_date())

        button_frame = ttk.Frame(self)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="OK", command=self.on_ok).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.on_cancel).pack(side="left", padx=5)

        self.bind("<Return>", lambda e: self.on_ok())
        self.bind("<Escape>", lambda e: self.on_cancel())
        self.grab_set()
        self.fields["name"].focus_set()

    def update_end_date(self):
        start_date_str = self.start_date_var.get().strip()
        freq = self.freq_var.get()
        try:
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
            if freq == "Yearly":
                months = 12
            elif freq == "Semi-annual":
                months = 6
            elif freq == "Quarterly":
                months = 3
            else:
                months = 0
            # Calculate end date
            year = start_date.year + (start_date.month + months - 1) // 12
            month = (start_date.month + months - 1) % 12 + 1
            day = start_date.day
            # Handle month-end overflow
            try:
                end_date = datetime.date(year, month, day)
            except ValueError:
                # If day is out of range for month, use last day of month
                import calendar
                last_day = calendar.monthrange(year, month)[1]
                end_date = datetime.date(year, month, last_day)
            self.end_date_var.set(end_date.strftime("%Y-%m-%d"))
        except Exception:
            self.end_date_var.set("")

    def on_ok(self):
        values = {
            "name": self.fields["name"].get().strip(),
            "title": self.fields["title"].get().strip(),
            "description": self.fields["description"].get().strip(),
            "start_date": self.start_date_var.get().strip(),
            "end_date": self.end_date_var.get().strip(),
            "supervision_frequency": self.freq_var.get()
        }
        allowed_freqs = {"Yearly", "Semi-annual", "Quarterly"}
        if not values["name"]:
            messagebox.showerror("Error", "Name is required.", parent=self)
            return
        if not values["start_date"]:
            messagebox.showerror("Error", "Start date is required and must be valid (YYYY-MM-DD).", parent=self)
            return
        if not values["end_date"]:
            messagebox.showerror("Error", "End date could not be calculated. Please check start date and frequency.", parent=self)
            return
        if values["supervision_frequency"] not in allowed_freqs:
            messagebox.showerror("Error", "Supervision frequency must be one of: Yearly, Semi-annual, Quarterly.", parent=self)
            return
        self.result = values
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()

class TreeItem:
    def __init__(self, name):
        self.name = name
        self.children = []
        
    def add_child(self, child):
        self.children.append(child)
        return child
    
    def remove_child(self, child):
        if child in self.children:
            self.children.remove(child)

class TreeviewApp:
    def edit_objetivos_child(self, item_id, parent_id):
        # Load current values from JSON
        data_path = os.path.join(os.path.dirname(__file__), "tree_data.json")
        with open(data_path, "r", encoding="utf-8") as f:
            tree_data = json.load(f)
        child_name = self.tree.item(item_id, 'text')
        # Find the child in the JSON
        values = None
        for spot in tree_data["spots"]:
            if spot["name"] == "objetivos":
                for child in spot["children"]:
                    if child.get("name") == child_name:
                        values = child.copy()
                        break
        if not values:
            messagebox.showerror("Error", "Could not find child data.", parent=self.root)
            return
        # Get metas children for Meta selection
        metas_children = []
        for spot in tree_data["spots"]:
            if spot["name"] == "metas":
                metas_children = spot["children"]
                break
        dialog = ObjetivosChildDialog(self.root, metas_children, initial=values)
        self.root.wait_window(dialog)
        new_values = dialog.result
        if new_values:
            # Update JSON
            for spot in tree_data["spots"]:
                if spot["name"] == "objetivos":
                    for child in spot["children"]:
                        if child.get("name") == child_name:
                            child.update({
                                "name": new_values.get("name", ""),
                                "title": new_values.get("title", ""),
                                "description": new_values.get("description", ""),
                                "metas_id": new_values.get("metas_id", None),
                                "start_date": new_values.get("start_date", ""),
                                "end_date": new_values.get("end_date", ""),
                                "supervision_frequency": new_values.get("supervision_frequency", ""),
                            })
                            break
            with open(data_path, "w", encoding="utf-8") as f:
                json.dump(tree_data, f, indent=2, ensure_ascii=False)
            # Update treeview display
            self.tree.item(item_id, text=new_values.get("name", ""))

    def edit_metas_child(self, item_id, parent_id):
        # Load current values from JSON
        data_path = os.path.join(os.path.dirname(__file__), "tree_data.json")
        with open(data_path, "r", encoding="utf-8") as f:
            tree_data = json.load(f)
        child_name = self.tree.item(item_id, 'text')
        # Find the child in the JSON
        values = None
        for spot in tree_data["spots"]:
            if spot["name"] == "metas":
                for child in spot["children"]:
                    if child.get("name") == child_name:
                        values = child.copy()
                        break
        if not values:
            messagebox.showerror("Error", "Could not find child data.", parent=self.root)
            return
        # Get sonhos children for Dream selection
        sonhos_children = []
        for spot in tree_data["spots"]:
            if spot["name"] == "sonhos":
                sonhos_children = spot["children"]
                break
        dialog = MetasChildDialog(self.root, sonhos_children, initial=values)
        self.root.wait_window(dialog)
        new_values = dialog.result
        if new_values:
            # Update JSON
            for spot in tree_data["spots"]:
                if spot["name"] == "metas":
                    for child in spot["children"]:
                        if child.get("name") == child_name:
                            child.update({
                                "name": new_values.get("name", ""),
                                "dream_id": new_values.get("dream_id", None),
                            })
                            break
            with open(data_path, "w", encoding="utf-8") as f:
                json.dump(tree_data, f, indent=2, ensure_ascii=False)
            # Update treeview display
            self.tree.item(item_id, text=new_values.get("name", ""))

    def edit_sonhos_child(self, item_id, parent_id):
        # Load current values from JSON
        data_path = os.path.join(os.path.dirname(__file__), "tree_data.json")
        with open(data_path, "r", encoding="utf-8") as f:
            tree_data = json.load(f)
        child_name = self.tree.item(item_id, 'text')
        # Find the child in the JSON
        values = None
        for spot in tree_data["spots"]:
            if spot["name"] == "sonhos":
                for child in spot["children"]:
                    if child.get("name") == child_name:
                        values = child.copy()
                        break
        if not values:
            messagebox.showerror("Error", "Could not find child data.", parent=self.root)
            return
        # Ensure backward compatibility for supervision_frequency
        allowed_freqs = {"Yearly", "Semi-annual", "Quarterly"}
        if values.get("supervision_frequency") not in allowed_freqs:
            values["supervision_frequency"] = "Yearly"
        # Show dialog pre-filled
        dialog = SonhosChildDialog(self.root)
        for k, entry in dialog.fields.items():
            if k == "supervision_frequency":
                dialog.freq_var.set(values.get("supervision_frequency", "Yearly"))
            elif k == "end_date":
                dialog.end_date_var.set(values.get("end_date", ""))
            elif k == "start_date":
                dialog.start_date_var.set(values.get("start_date", ""))
            else:
                entry.delete(0, tk.END)
                entry.insert(0, values.get(k, ""))
        self.root.wait_window(dialog)
        new_values = dialog.result
        if new_values:
            # Update JSON
            for spot in tree_data["spots"]:
                if spot["name"] == "sonhos":
                    for child in spot["children"]:
                        if child.get("name") == child_name:
                            child.update({
                                "name": new_values.get("name", ""),
                                "title": new_values.get("title", ""),
                                "description": new_values.get("description", ""),
                                "start_date": new_values.get("start_date", ""),
                                "end_date": new_values.get("end_date", ""),
                                "supervision_frequency": new_values.get("supervision_frequency", ""),
                            })
                            break
            with open(data_path, "w", encoding="utf-8") as f:
                json.dump(tree_data, f, indent=2, ensure_ascii=False)
            # Update treeview display
            self.tree.item(item_id, text=new_values.get("name", ""))
    def __init__(self, root):
        self.root = root
        self.root.title("Treeview Menu")

        # Initialize data model
        self.data_model = {}  # Store TreeItem objects by their tree IDs

        # Create button frame
        button_frame = ttk.Frame(root)
        button_frame.pack(fill='x', padx=5, pady=5)

        # Add expand/collapse buttons
        ttk.Button(button_frame, text="Expand All", command=self.expand_all).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Collapse All", command=self.collapse_all).pack(side='left')

        # Create the treeview
        self.tree = ttk.Treeview(root, columns=("periodo", "n_tarefas"))

        # Configure columns
        self.tree.heading("#0", text="Nível")  # Add label for the tree column
        self.tree.heading("periodo", text="Período")
        self.tree.heading("n_tarefas", text="N. Tarefas")

        # Set column widths
        self.tree.column("#0", width=200)  # Width for the tree column
        self.tree.column("periodo", width=150)
        self.tree.column("n_tarefas", width=150)

        # Pack the treeview
        self.tree.pack(expand=True, fill='both')

        # Bind right-click event
        self.tree.bind("<Button-3>", self.show_context_menu)

        # Populate the treeview
        self.populate_tree()

    def show_context_menu(self, event):
        """Show context menu on right click"""
        item_id = self.tree.identify_row(event.y)
        if item_id:
            self.tree.selection_set(item_id)
            menu = tk.Menu(self.root, tearoff=0)
            node = self.data_model.get(item_id)
            allowed_for_children = ["sonhos", "metas", "objetivos"]
            parent_id = self.tree.parent(item_id)
            parent_name = self.tree.item(parent_id, 'text') if parent_id else None
            # If this is a top-level spot
            if node and node.name in allowed_for_children:
                menu.add_command(label="Add Child", command=lambda: self.add_child_node(item_id))
            # If this is a child of "sonhos", offer Edit Child
            elif parent_name == "sonhos":
                menu.add_command(label="Edit Child", command=lambda: self.edit_sonhos_child(item_id, parent_id))
            # If this is a child of "metas", offer Edit Child for metas
            elif parent_name == "metas":
                menu.add_command(label="Edit Child", command=lambda: self.edit_metas_child(item_id, parent_id))
            # If this is a child of "objetivos", offer Edit Child for objetivos
            elif parent_name == "objetivos":
                menu.add_command(label="Edit Child", command=lambda: self.edit_objetivos_child(item_id, parent_id))
            else:
                menu.add_command(label="Edit Name", command=lambda: self.edit_node_name(item_id))
            menu.post(event.x_root, event.y_root)

    def add_child_node(self, parent_id):
        """Add a new child node (label) to the selected spot, updating tree and JSON"""
        spot_name = self.tree.item(parent_id, 'text')
        if spot_name == "sonhos":
            dialog = SonhosChildDialog(self.root)
            self.root.wait_window(dialog)
            values = dialog.result
            if values:
                new_item = TreeItem(values["name"])
                parent_item = self.data_model.get(parent_id)
                if parent_item:
                    parent_item.add_child(new_item)
                children = self.tree.get_children(parent_id)
                if children:
                    last_child = children[-1]
                    item_id = self.tree.insert(parent_id, self.tree.index(last_child) + 1, text=values["name"], values=("", ""))
                else:
                    item_id = self.tree.insert(parent_id, 0, text=values["name"], values=("", ""))
                self.data_model[item_id] = new_item
                self.update_json_add_child_by_spot(parent_id, values)
        elif spot_name == "metas":
            # Get sonhos children from JSON
            data_path = os.path.join(os.path.dirname(__file__), "tree_data.json")
            with open(data_path, "r", encoding="utf-8") as f:
                tree_data = json.load(f)
            sonhos_children = []
            for spot in tree_data["spots"]:
                if spot["name"] == "sonhos":
                    sonhos_children = spot["children"]
                    break
            dialog = MetasChildDialog(self.root, sonhos_children)
            self.root.wait_window(dialog)
            values = dialog.result
            if values:
                new_item = TreeItem(values["name"])
                parent_item = self.data_model.get(parent_id)
                if parent_item:
                    parent_item.add_child(new_item)
                children = self.tree.get_children(parent_id)
                if children:
                    last_child = children[-1]
                    item_id = self.tree.insert(parent_id, self.tree.index(last_child) + 1, text=values["name"], values=("", ""))
                else:
                    item_id = self.tree.insert(parent_id, 0, text=values["name"], values=("", ""))
                self.data_model[item_id] = new_item
                self.update_json_add_child_by_spot(parent_id, values)
        elif spot_name == "objetivos":
            # Get metas children from JSON
            data_path = os.path.join(os.path.dirname(__file__), "tree_data.json")
            with open(data_path, "r", encoding="utf-8") as f:
                tree_data = json.load(f)
            metas_children = []
            for spot in tree_data["spots"]:
                if spot["name"] == "metas":
                    metas_children = spot["children"]
                    break
            dialog = ObjetivosChildDialog(self.root, metas_children)
            self.root.wait_window(dialog)
            values = dialog.result
            if values:
                new_item = TreeItem(values["name"])
                parent_item = self.data_model.get(parent_id)
                if parent_item:
                    parent_item.add_child(new_item)
                children = self.tree.get_children(parent_id)
                if children:
                    last_child = children[-1]
                    item_id = self.tree.insert(parent_id, self.tree.index(last_child) + 1, text=values["name"], values=("", ""))
                else:
                    item_id = self.tree.insert(parent_id, 0, text=values["name"], values=("", ""))
                self.data_model[item_id] = new_item
                self.update_json_add_child_by_spot(parent_id, values)
        else:
            name = simpledialog.askstring("New Label", "Enter label for new item:")
            if name:
                new_item = TreeItem(name)
                parent_item = self.data_model.get(parent_id)
                if parent_item:
                    parent_item.add_child(new_item)
                children = self.tree.get_children(parent_id)
                if children:
                    last_child = children[-1]
                    item_id = self.tree.insert(parent_id, self.tree.index(last_child) + 1, text=name, values=("", ""))
                else:
                    item_id = self.tree.insert(parent_id, 0, text=name, values=("", ""))
                self.data_model[item_id] = new_item
                self.update_json_add_child_by_spot(parent_id, name)

    def get_spot_name_from_id(self, item_id):
        # Returns the spot name ("sonhos", "metas", "objetivos") for a given item_id
        while item_id:
            parent = self.tree.parent(item_id)
            if not parent:
                return self.tree.item(item_id, 'text')
            item_id = parent
        return None

    def update_json_add_child_by_spot(self, parent_id, child_data):
        data_path = os.path.join(os.path.dirname(__file__), "tree_data.json")
        with open(data_path, "r", encoding="utf-8") as f:
            tree_data = json.load(f)
        spot_name = self.tree.item(parent_id, 'text')
        for spot in tree_data["spots"]:
            if spot["name"] == spot_name:
                if spot_name == "sonhos" and isinstance(child_data, dict):
                    spot["children"].append({
                        "name": child_data.get("name", ""),
                        "title": child_data.get("title", ""),
                        "description": child_data.get("description", ""),
                        "start_date": child_data.get("start_date", ""),
                        "end_date": child_data.get("end_date", ""),
                        "supervision_frequency": child_data.get("supervision_frequency", ""),
                        "children": []
                    })
                elif spot_name == "metas" and isinstance(child_data, dict) and "dream_id" in child_data:
                    spot["children"].append({
                        "name": child_data.get("name", ""),
                        "title": child_data.get("title", ""),
                        "description": child_data.get("description", ""),
                        "dream_id": child_data.get("dream_id", None),
                        "start_date": child_data.get("start_date", ""),
                        "end_date": child_data.get("end_date", ""),
                        "supervision_frequency": child_data.get("supervision_frequency", ""),
                        "children": []
                    })
                elif spot_name == "objetivos" and isinstance(child_data, dict) and "metas_id" in child_data:
                    spot["children"].append({
                        "name": child_data.get("name", ""),
                        "title": child_data.get("title", ""),
                        "description": child_data.get("description", ""),
                        "metas_id": child_data.get("metas_id", None),
                        "start_date": child_data.get("start_date", ""),
                        "end_date": child_data.get("end_date", ""),
                        "supervision_frequency": child_data.get("supervision_frequency", ""),
                        "children": []
                    })
                else:
                    # For fallback, child_data is just the name string
                    spot["children"].append({"name": child_data, "children": []})
                break
        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(tree_data, f, indent=2, ensure_ascii=False)

    def edit_node_name(self, item_id):
        node = self.data_model.get(item_id)
        if not node:
            return
        new_name = simpledialog.askstring("Edit Name", f"Enter new name for '{node.name}':")
        if new_name and new_name != node.name:
            old_name = node.name
            node.name = new_name
            self.tree.item(item_id, text=new_name)
            self.update_json_edit_name_by_path(item_id, new_name)

    def update_json_edit_name_by_path(self, item_id, new_name):
        data_path = os.path.join(os.path.dirname(__file__), "tree_data.json")
        with open(data_path, "r", encoding="utf-8") as f:
            tree_data = json.load(f)
        # Find the node in the spots structure and update its name
        path = []
        current_id = item_id
        while current_id:
            path.append(self.tree.item(current_id, 'text'))
            current_id = self.tree.parent(current_id)
        path = list(reversed(path))
        if len(path) == 1:
            # Editing a spot name
            for spot in tree_data["spots"]:
                if spot["name"] == path[0]:
                    spot["name"] = new_name
                    break
        elif len(path) == 2:
            # Editing a label under a spot
            spot_name, label_name = path
            for spot in tree_data["spots"]:
                if spot["name"] == spot_name:
                    for child in spot["children"]:
                        if child["name"] == label_name:
                            child["name"] = new_name
                            break
        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(tree_data, f, indent=2, ensure_ascii=False)

    def expand_all(self):
        """Expand all items in the tree"""
        for item in self.tree.get_children():
            self.tree.item(item, open=True)
            self._expand_children(item)

    def _expand_children(self, item):
        """Helper function to recursively expand all children"""
        for child in self.tree.get_children(item):
            self.tree.item(child, open=True)
            self._expand_children(child)

    def collapse_all(self):
        """Collapse all items in the tree"""
        for item in self.tree.get_children():
            self.tree.item(item, open=False)
            self._collapse_children(item)

    def _collapse_children(self, item):
        """Helper function to recursively collapse all children"""
        for child in self.tree.get_children(item):
            self.tree.item(child, open=False)
            self._collapse_children(child)

    def populate_tree(self):
        # Load data from JSON file
        data_path = os.path.join(os.path.dirname(__file__), "tree_data.json")
        with open(data_path, "r", encoding="utf-8") as f:
            tree_data = json.load(f)

        def add_items(parent_id, node):
            item = TreeItem(node["name"])
            item_id = self.tree.insert(parent_id, "end", text=node["name"], values=("", ""))
            self.data_model[item_id] = item
            for child in node.get("children", []):
                item.add_child(add_items(item_id, child))
            return item

        # Add each spot as a top-level node
        for spot in tree_data.get("spots", []):
            add_items("", spot)

def main():
    root = tk.Tk()
    root.geometry("600x500")  # Set window size
    
    # Configure style
    style = ttk.Style()
    style.configure("Treeview", 
                   indent=20,  # Increase indentation
                   rowheight=25)  # Increase row height
    
    # Configure Treeview padding
    style.configure("Treeview", padding=3)
    app = TreeviewApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
