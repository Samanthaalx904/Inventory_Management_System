from customtkinter import *
from tkinter import ttk, messagebox
from Database import (
    get_all_employees, add_employee, update_employee,
    delete_employee, search_employees
)

# ── Match dashboard theme ────────────────────────────────────────
COLORS = {
    "bg_main":       "#1A1A2E",
    "header":        "#162447",
    "sub_header":    "#1F4068",
    "sidebar":       "#1B1B3A",
    "sidebar_hover": "#3F2A56",
    "menu_title":    "#ff4d6d",
    "card1":         "#ff6b6b",
    "card2":         "#4ecdc4",
    "card3":         "#ffd93d",
    "text":          "#FFFFFF",
    "text_dim":      "#A0AEC0",
    "entry_bg":      "#162447",
    "btn_primary":   "#1F4068",
    "btn_danger":    "#ff4d6d",
    "btn_warning":   "#ffd93d",
    "btn_success":   "#4ecdc4",
}


class EmployeeClass:
    def __init__(self, root):
        self.root = root

        # ── Style ttk table to match dark theme ─────────────────
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background=COLORS["header"],
                        foreground=COLORS["text"],
                        fieldbackground=COLORS["header"],
                        rowheight=28,
                        font=("Arial", 10))
        style.configure("Treeview.Heading",
                        background=COLORS["sub_header"],
                        foreground=COLORS["card3"],
                        font=("Arial", 10, "bold"),
                        relief="flat")
        style.map("Treeview",
                  background=[("selected", COLORS["sidebar_hover"])],
                  foreground=[("selected", COLORS["text"])])

        # ---------------- VARIABLES ----------------
        self.var_search_by = StringVar()
        self.var_searchtxt = StringVar()
        self.var_em_id     = StringVar()
        self.var_gender    = StringVar()
        self.var_contact   = StringVar()
        self.var_name      = StringVar()
        self.var_dob       = StringVar()
        self.var_doj       = StringVar()
        self.var_email     = StringVar()
        self.var_pass      = StringVar()
        self.var_utype     = StringVar()
        self.var_salary    = StringVar()

        self.build_ui()
        self.show()

    # ================= UI =================
    def build_ui(self):

        # ── Page title ──────────────────────────────────────────
        title_bar = CTkFrame(self.root, fg_color=COLORS["header"], corner_radius=10)
        title_bar.pack(fill="x", pady=(0, 10))

        CTkLabel(title_bar, text="👷 Employee Management",
                 font=("Arial", 18, "bold"),
                 text_color=COLORS["card3"]).pack(side="left", padx=15, pady=8)

        # ── Search bar ──────────────────────────────────────────
        search_frame = CTkFrame(self.root, fg_color=COLORS["sub_header"], corner_radius=10)
        search_frame.pack(fill="x", padx=10, pady=(0, 10))

        CTkLabel(search_frame, text="Search By:",
                 font=("Arial", 12, "bold"),
                 text_color=COLORS["text"]).pack(side="left", padx=(15, 5), pady=10)

        CTkComboBox(search_frame,
                    values=("eid", "name", "email", "contact"),
                    variable=self.var_search_by,
                    width=150,
                    fg_color=COLORS["entry_bg"],
                    border_color=COLORS["sidebar_hover"],
                    button_color=COLORS["sidebar_hover"],
                    text_color=COLORS["text"],
                    dropdown_fg_color=COLORS["header"]
                    ).pack(side="left", padx=5, pady=10)

        CTkEntry(search_frame,
                 textvariable=self.var_searchtxt,
                 width=250,
                 fg_color=COLORS["entry_bg"],
                 border_color=COLORS["sidebar_hover"],
                 text_color=COLORS["text"],
                 placeholder_text="Enter search value..."
                 ).pack(side="left", padx=5, pady=10)

        CTkButton(search_frame, text="🔍 Search",
                  command=self.search,
                  fg_color=COLORS["btn_primary"],
                  hover_color=COLORS["sidebar_hover"],
                  text_color=COLORS["text"],
                  width=100).pack(side="left", padx=5)

        CTkButton(search_frame, text="↺ Show All",
                  command=self.show,
                  fg_color="transparent",
                  hover_color=COLORS["sidebar_hover"],
                  border_width=1,
                  border_color=COLORS["text_dim"],
                  text_color=COLORS["text"],
                  width=100).pack(side="left", padx=5)

        # ── Form card ───────────────────────────────────────────
        form_card = CTkFrame(self.root, fg_color=COLORS["header"], corner_radius=12)
        form_card.pack(fill="x", padx=10, pady=(0, 10))

        CTkLabel(form_card, text="Employee Details",
                 font=("Arial", 13, "bold"),
                 text_color=COLORS["card2"]).grid(
                 row=0, column=0, columnspan=6, sticky="w", padx=15, pady=(10, 5))

        # helper to make a label+entry pair
        def lbl(parent, text, row, col):
            CTkLabel(parent, text=text,
                     font=("Arial", 12, "bold"),
                     text_color=COLORS["text_dim"]
                     ).grid(row=row, column=col, sticky="w", padx=(15, 5), pady=6)

        def ent(parent, var, row, col, show=None):
            CTkEntry(parent, textvariable=var, width=180,
                     fg_color=COLORS["entry_bg"],
                     border_color=COLORS["sidebar_hover"],
                     text_color=COLORS["text"],
                     show=show or ""
                     ).grid(row=row, column=col+1, padx=(0, 15), pady=6)

        def cmb(parent, var, values, row, col):
            CTkComboBox(parent, variable=var, values=values, width=180,
                        fg_color=COLORS["entry_bg"],
                        border_color=COLORS["sidebar_hover"],
                        button_color=COLORS["sidebar_hover"],
                        text_color=COLORS["text"],
                        dropdown_fg_color=COLORS["header"]
                        ).grid(row=row, column=col+1, padx=(0, 15), pady=6)

        # Row 1
        lbl(form_card, "Emp ID",    1, 0); ent(form_card, self.var_em_id,   1, 0)
        lbl(form_card, "Gender",    1, 2); cmb(form_card, self.var_gender,   ["Male", "Female"], 1, 2)
        lbl(form_card, "Contact",   1, 4); ent(form_card, self.var_contact,  1, 4)

        # Row 2
        lbl(form_card, "Name",      2, 0); ent(form_card, self.var_name,     2, 0)
        lbl(form_card, "D.O.B",     2, 2); ent(form_card, self.var_dob,      2, 2)
        lbl(form_card, "D.O.J",     2, 4); ent(form_card, self.var_doj,      2, 4)

        # Row 3
        lbl(form_card, "Email",     3, 0); ent(form_card, self.var_email,    3, 0)
        lbl(form_card, "Password",  3, 2); ent(form_card, self.var_pass,     3, 2, show="*")
        lbl(form_card, "User Type", 3, 4); cmb(form_card, self.var_utype,    ["Admin", "Employee"], 3, 4)

        # Row 4 — Address spans wide, Salary at end
        lbl(form_card, "Address", 4, 0)
        self.txt_address = CTkTextbox(form_card, width=400, height=40,
                                      fg_color=COLORS["entry_bg"],
                                      border_color=COLORS["sidebar_hover"],
                                      text_color=COLORS["text"],
                                      border_width=2)
        self.txt_address.grid(row=4, column=1, columnspan=3, sticky="w",
                              padx=(0, 15), pady=6)

        lbl(form_card, "Salary", 4, 4); ent(form_card, self.var_salary, 4, 4)

        # ── Action buttons ──────────────────────────────────────
        btn_frame = CTkFrame(self.root, fg_color="transparent")
        btn_frame.pack(pady=8)

        btn_cfg = {"width": 130, "height": 36, "corner_radius": 8,
                   "font": ("Arial", 12, "bold")}

        CTkButton(btn_frame, text="💾 Save",
                  fg_color=COLORS["btn_success"],
                  hover_color="#38b2ac",
                  text_color=COLORS["bg_main"],
                  command=self.add, **btn_cfg).pack(side="left", padx=8)

        CTkButton(btn_frame, text="✏️ Update",
                  fg_color=COLORS["btn_primary"],
                  hover_color=COLORS["sidebar_hover"],
                  text_color=COLORS["text"],
                  command=self.update, **btn_cfg).pack(side="left", padx=8)

        CTkButton(btn_frame, text="🗑 Delete",
                  fg_color=COLORS["btn_danger"],
                  hover_color="#e03058",
                  text_color=COLORS["text"],
                  command=self.delete, **btn_cfg).pack(side="left", padx=8)

        CTkButton(btn_frame, text="🔄 Clear",
                  fg_color="transparent",
                  hover_color=COLORS["sidebar_hover"],
                  border_width=1,
                  border_color=COLORS["text_dim"],
                  text_color=COLORS["text"],
                  command=self.clear, **btn_cfg).pack(side="left", padx=8)

        # ── Table ───────────────────────────────────────────────
        table_card = CTkFrame(self.root, fg_color=COLORS["header"], corner_radius=12)
        table_card.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        CTkLabel(table_card, text="Employee Records",
                 font=("Arial", 13, "bold"),
                 text_color=COLORS["card2"]).pack(anchor="w", padx=15, pady=(8, 4))

        cols = ("eid", "name", "email", "gender", "contact",
                "dob", "doj", "password", "utype", "salary", "address")

        scroll_y = CTkScrollbar(table_card)
        scroll_y.pack(side="right", fill="y", pady=5)

        self.emp_table = ttk.Treeview(table_card, columns=cols,
                                      show="headings",
                                      yscrollcommand=scroll_y.set)
        scroll_y.configure(command=self.emp_table.yview)

        col_widths = {
            "eid": 70, "name": 120, "email": 160, "gender": 70,
            "contact": 100, "dob": 90, "doj": 90, "password": 90,
            "utype": 80, "salary": 80, "address": 160
        }
        for col in cols:
            self.emp_table.heading(col, text=col.upper())
            self.emp_table.column(col, width=col_widths.get(col, 90), anchor="center")

        self.emp_table.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.emp_table.bind("<ButtonRelease-1>", self.get_data)

    # ================= ACTIONS =================
    def add(self):
        if not self.var_em_id.get():
            messagebox.showerror("Error", "Employee ID is required")
            return
        success = add_employee({
            "eid":      self.var_em_id.get(),
            "name":     self.var_name.get(),
            "email":    self.var_email.get(),
            "gender":   self.var_gender.get(),
            "contact":  self.var_contact.get(),
            "dob":      self.var_dob.get(),
            "doj":      self.var_doj.get(),
            "password": self.var_pass.get(),
            "utype":    self.var_utype.get(),
            "salary":   self.var_salary.get(),
            "address":  self.txt_address.get("1.0", END).strip()
        })
        if success:
            self.show()
            self.clear()
            messagebox.showinfo("Success", "Employee added successfully")
        else:
            messagebox.showerror("Error", "Employee ID already exists")

    def update(self):
        if not self.var_em_id.get():
            messagebox.showerror("Error", "Select an employee to update")
            return
        update_employee({
            "eid":      self.var_em_id.get(),
            "name":     self.var_name.get(),
            "email":    self.var_email.get(),
            "gender":   self.var_gender.get(),
            "contact":  self.var_contact.get(),
            "dob":      self.var_dob.get(),
            "doj":      self.var_doj.get(),
            "password": self.var_pass.get(),
            "utype":    self.var_utype.get(),
            "salary":   self.var_salary.get(),
            "address":  self.txt_address.get("1.0", END).strip()
        })
        self.show()
        self.clear()
        messagebox.showinfo("Success", "Employee updated successfully")

    def delete(self):
        if not self.var_em_id.get():
            messagebox.showerror("Error", "Select an employee to delete")
            return
        if messagebox.askyesno("Confirm", "Delete this employee?"):
            delete_employee(self.var_em_id.get())
            self.show()
            self.clear()
            messagebox.showinfo("Success", "Employee deleted successfully")

    def show(self):
        self.emp_table.delete(*self.emp_table.get_children())
        for row in get_all_employees():
            self.emp_table.insert("", END, values=row)

    def get_data(self, ev):
        row = self.emp_table.item(self.emp_table.focus())["values"]
        if row:
            self.var_em_id.set(row[0])
            self.var_name.set(row[1])
            self.var_email.set(row[2])
            self.var_gender.set(row[3])
            self.var_contact.set(row[4])
            self.var_dob.set(row[5])
            self.var_doj.set(row[6])
            self.var_pass.set(row[7])
            self.var_utype.set(row[8])
            self.var_salary.set(row[9])
            self.txt_address.delete("1.0", END)
            self.txt_address.insert(END, row[10])

    def clear(self):
        for v in (self.var_em_id, self.var_name, self.var_email, self.var_gender,
                  self.var_contact, self.var_dob, self.var_doj, self.var_pass,
                  self.var_utype, self.var_salary):
            v.set("")
        self.txt_address.delete("1.0", END)

    def search(self):
        field = self.var_search_by.get()
        if not field:
            messagebox.showerror("Error", "Select a search field")
            return
        self.emp_table.delete(*self.emp_table.get_children())
        for row in search_employees(field, self.var_searchtxt.get()):
            self.emp_table.insert("", END, values=row)