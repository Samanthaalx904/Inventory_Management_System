import customtkinter as ctk
from tkinter import ttk, messagebox
import json
import os


class CategoryClass:
    def __init__(self, parent):
        self.parent = parent

        self.categories = []
        self.load_data()

        self.build_ui()

    # ======================
    # FILE HANDLING
    # ======================
    def load_data(self):
        if os.path.exists("categories.json"):
            try:
                with open("categories.json", "r") as f:
                    self.categories = json.load(f)
            except:
                self.categories = []

    def save_data(self):
        with open("categories.json", "w") as f:
            json.dump(self.categories, f)

    # ======================
    # UI (DASHBOARD STYLE FIX)
    # ======================
    def build_ui(self):
        # Main container (fits inside dashboard content frame)
        self.container = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=2)
        self.container.grid_rowconfigure(0, weight=1)

        # LEFT FORM PANEL
        self.form_frame = ctk.CTkFrame(
            self.container,
            fg_color="#1B1B3A",
            corner_radius=15
        )
        self.form_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # RIGHT TABLE PANEL
        self.table_frame = ctk.CTkFrame(
            self.container,
            fg_color="#1B1B3A",
            corner_radius=15
        )
        self.table_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.build_form()
        self.build_table()

    # ======================
    # FORM
    # ======================
    def build_form(self):
        ctk.CTkLabel(
            self.form_frame,
            text="Category Module",
            font=("Arial", 20, "bold"),
            text_color="white"
        ).pack(pady=(20, 10))

        self.name_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Enter category name"
        )
        self.name_entry.pack(fill="x", padx=20, pady=10)

        self.desc_entry = ctk.CTkTextbox(
            self.form_frame,
            height=120
        )
        self.desc_entry.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            self.form_frame,
            text="Add Category",
            command=self.add_category,
            fg_color="#1F4068"
        ).pack(fill="x", padx=20, pady=5)

        ctk.CTkButton(
            self.form_frame,
            text="Delete Selected",
            command=self.delete_category,
            fg_color="#ff4d6d",
            hover_color="#cc3a55"
        ).pack(fill="x", padx=20, pady=5)

        self.search_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Search category..."
        )
        self.search_entry.pack(fill="x", padx=20, pady=10)
        self.search_entry.bind("<KeyRelease>", self.search_category)

    # ======================
    # TABLE
    # ======================
    def build_table(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Treeview",
            background="#1A1A2E",
            foreground="white",
            rowheight=30,
            fieldbackground="#1A1A2E"
        )

        style.configure(
            "Treeview.Heading",
            background="#1F4068",
            foreground="white"
        )

        self.tree = ttk.Treeview(
            self.table_frame,
            columns=("Name", "Description"),
            show="headings"
        )

        self.tree.heading("Name", text="Category Name")
        self.tree.heading("Description", text="Description")

        self.tree.column("Name", width=200)
        self.tree.column("Description", width=300)

        self.tree.pack(fill="both", expand=True, padx=15, pady=15)

        self.refresh()

    # ======================
    # LOGIC
    # ======================
    def add_category(self):
        name = self.name_entry.get().strip()
        desc = self.desc_entry.get("0.0", "end").strip()

        if not name:
            messagebox.showerror("Error", "Category name required")
            return

        self.categories.append((name, desc))
        self.save_data()
        self.refresh()

        self.name_entry.delete(0, "end")
        self.desc_entry.delete("0.0", "end")

    def delete_category(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("Warning", "Select a category")
            return

        item = self.tree.item(selected[0])
        values = item["values"]

        self.categories = [c for c in self.categories if list(c) != values]

        self.save_data()
        self.refresh()

    def refresh(self, data=None):
        for i in self.tree.get_children():
            self.tree.delete(i)

        data = data if data else self.categories

        for c in data:
            self.tree.insert("", "end", values=c)

    def search_category(self, event=None):
        q = self.search_entry.get().lower()
        filtered = [c for c in self.categories if q in c[0].lower()]
        self.refresh(filtered)