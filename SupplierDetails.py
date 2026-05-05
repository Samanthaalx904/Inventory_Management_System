import customtkinter as ctk
from tkinter import ttk, messagebox
from Database import (
    get_all_suppliers, add_supplier, update_supplier,
    delete_supplier, search_suppliers, get_supplier_names
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
    "btn_success":   "#4ecdc4",
}


class SupplierClass:
    def __init__(self, root):
        self.root = root

        # ── Style ttk table ──────────────────────────────────────
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
        self.var_search_by = ctk.StringVar()
        self.var_searchtxt = ctk.StringVar()
        self.var_sid       = ctk.StringVar()
        self.var_name      = ctk.StringVar()
        self.var_contact   = ctk.StringVar()
        self.var_email     = ctk.StringVar()
        self.var_company   = ctk.StringVar()

        self.build_ui()
        self.show()

    # ================= UI =================
    def build_ui(self):

        # ── Page title ──────────────────────────────────────────
        title_bar = ctk.CTkFrame(self.root, fg_color=COLORS["header"], corner_radius=10)
        title_bar.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(title_bar, text="🚚 Supplier Management",
                     font=("Arial", 18, "bold"),
                     text_color=COLORS["card3"]).pack(side="left", padx=15, pady=8)

        # ── Search bar ──────────────────────────────────────────
        search_frame = ctk.CTkFrame(self.root, fg_color=COLORS["sub_header"], corner_radius=10)
        search_frame.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(search_frame, text="Search By:",
                     font=("Arial", 12, "bold"),
                     text_color=COLORS["text"]).pack(side="left", padx=(15, 5), pady=10)

        ctk.CTkComboBox(search_frame,
                        values=("name", "contact", "email", "company"),
                        variable=self.var_search_by,
                        width=150,
                        fg_color=COLORS["entry_bg"],
                        border_color=COLORS["sidebar_hover"],
                        button_color=COLORS["sidebar_hover"],
                        text_color=COLORS["text"],
                        dropdown_fg_color=COLORS["header"]
                        ).pack(side="left", padx=5, pady=10)

        ctk.CTkEntry(search_frame,
                     textvariable=self.var_searchtxt,
                     width=250,
                     fg_color=COLORS["entry_bg"],
                     border_color=COLORS["sidebar_hover"],
                     text_color=COLORS["text"],
                     placeholder_text="Enter search value..."
                     ).pack(side="left", padx=5, pady=10)

        ctk.CTkButton(search_frame, text="🔍 Search",
                      command=self.search,
                      fg_color=COLORS["btn_primary"],
                      hover_color=COLORS["sidebar_hover"],
                      text_color=COLORS["text"],
                      width=100).pack(side="left", padx=5)

        ctk.CTkButton(search_frame, text="↺ Show All",
                      command=self.show,
                      fg_color="transparent",
                      hover_color=COLORS["sidebar_hover"],
                      border_width=1,
                      border_color=COLORS["text_dim"],
                      text_color=COLORS["text"],
                      width=100).pack(side="left", padx=5)

        # ── Form card ───────────────────────────────────────────
        form_card = ctk.CTkFrame(self.root, fg_color=COLORS["header"], corner_radius=12)
        form_card.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(form_card, text="Supplier Details",
                     font=("Arial", 13, "bold"),
                     text_color=COLORS["card2"]).grid(
                     row=0, column=0, columnspan=6, sticky="w", padx=15, pady=(10, 5))

        def lbl(text, row, col):
            ctk.CTkLabel(form_card, text=text,
                         font=("Arial", 12, "bold"),
                         text_color=COLORS["text_dim"]
                         ).grid(row=row, column=col, sticky="w", padx=(15, 5), pady=6)

        def ent(var, row, col):
            ctk.CTkEntry(form_card, textvariable=var, width=200,
                         fg_color=COLORS["entry_bg"],
                         border_color=COLORS["sidebar_hover"],
                         text_color=COLORS["text"]
                         ).grid(row=row, column=col + 1, padx=(0, 15), pady=6)

        # Row 1
        lbl("Supplier ID", 1, 0); ent(self.var_sid,     1, 0)
        lbl("Name",        1, 2); ent(self.var_name,    1, 2)
        lbl("Company",     1, 4); ent(self.var_company, 1, 4)

        # Row 2
        lbl("Contact",     2, 0); ent(self.var_contact, 2, 0)
        lbl("Email",       2, 2); ent(self.var_email,   2, 2)

        # Row 3 — Address
        lbl("Address", 3, 0)
        self.txt_address = ctk.CTkTextbox(form_card, width=500, height=45,
                                          fg_color=COLORS["entry_bg"],
                                          border_color=COLORS["sidebar_hover"],
                                          text_color=COLORS["text"],
                                          border_width=2)
        self.txt_address.grid(row=3, column=1, columnspan=5, sticky="w",
                              padx=(0, 15), pady=6)

        # ── Action buttons ──────────────────────────────────────
        btn_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        btn_frame.pack(pady=8)

        btn_cfg = {"width": 130, "height": 36, "corner_radius": 8,
                   "font": ("Arial", 12, "bold")}

        ctk.CTkButton(btn_frame, text="💾 Save",
                      fg_color=COLORS["btn_success"],
                      hover_color="#38b2ac",
                      text_color=COLORS["bg_main"],
                      command=self.add, **btn_cfg).pack(side="left", padx=8)

        ctk.CTkButton(btn_frame, text="✏️ Update",
                      fg_color=COLORS["btn_primary"],
                      hover_color=COLORS["sidebar_hover"],
                      text_color=COLORS["text"],
                      command=self.update, **btn_cfg).pack(side="left", padx=8)

        ctk.CTkButton(btn_frame, text="🗑 Delete",
                      fg_color=COLORS["btn_danger"],
                      hover_color="#e03058",
                      text_color=COLORS["text"],
                      command=self.delete, **btn_cfg).pack(side="left", padx=8)

        ctk.CTkButton(btn_frame, text="🔄 Clear",
                      fg_color="transparent",
                      hover_color=COLORS["sidebar_hover"],
                      border_width=1,
                      border_color=COLORS["text_dim"],
                      text_color=COLORS["text"],
                      command=self.clear, **btn_cfg).pack(side="left", padx=8)

        # ── Table ───────────────────────────────────────────────
        table_card = ctk.CTkFrame(self.root, fg_color=COLORS["header"], corner_radius=12)
        table_card.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        ctk.CTkLabel(table_card, text="Supplier Records",
                     font=("Arial", 13, "bold"),
                     text_color=COLORS["card2"]).pack(anchor="w", padx=15, pady=(8, 4))

        cols = ("sid", "name", "contact", "email", "address", "company")

        scroll_y = ctk.CTkScrollbar(table_card)
        scroll_y.pack(side="right", fill="y", pady=5)

        self.supplier_table = ttk.Treeview(table_card, columns=cols,
                                           show="headings",
                                           yscrollcommand=scroll_y.set)
        scroll_y.configure(command=self.supplier_table.yview)

        col_widths = {
            "sid": 60, "name": 140, "contact": 110,
            "email": 180, "address": 200, "company": 130
        }
        for col in cols:
            self.supplier_table.heading(col, text=col.upper())
            self.supplier_table.column(col, width=col_widths.get(col, 120), anchor="center")

        self.supplier_table.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.supplier_table.bind("<ButtonRelease-1>", self.get_data)

    # ================= ACTIONS =================
    def add(self):
        if not self.var_name.get():
            messagebox.showerror("Error", "Supplier name is required")
            return
        add_supplier(
            self.var_name.get(),
            self.var_contact.get(),
            self.var_email.get(),
            self.txt_address.get("1.0", "end").strip(),
            self.var_company.get()
        )
        self.show()
        self.clear()
        messagebox.showinfo("Success", "Supplier added successfully")

    def update(self):
        if not self.var_sid.get():
            messagebox.showerror("Error", "Select a supplier to update")
            return
        update_supplier(
            self.var_sid.get(),
            self.var_name.get(),
            self.var_contact.get(),
            self.var_email.get(),
            self.txt_address.get("1.0", "end").strip(),
            self.var_company.get()
        )
        self.show()
        self.clear()
        messagebox.showinfo("Success", "Supplier updated successfully")

    def delete(self):
        if not self.var_sid.get():
            messagebox.showerror("Error", "Select a supplier to delete")
            return
        if messagebox.askyesno("Confirm", "Delete this supplier?"):
            delete_supplier(self.var_sid.get())
            self.show()
            self.clear()
            messagebox.showinfo("Success", "Supplier deleted successfully")

    def show(self):
        self.supplier_table.delete(*self.supplier_table.get_children())
        for row in get_all_suppliers():
            self.supplier_table.insert("", "end", values=row)

    def get_data(self, ev):
        row = self.supplier_table.item(self.supplier_table.focus())["values"]
        if row:
            self.var_sid.set(row[0])
            self.var_name.set(row[1])
            self.var_contact.set(row[2])
            self.var_email.set(row[3])
            self.txt_address.delete("1.0", "end")
            self.txt_address.insert("end", row[4])
            self.var_company.set(row[5])

    def clear(self):
        for v in (self.var_sid, self.var_name, self.var_contact,
                  self.var_email, self.var_company):
            v.set("")
        self.txt_address.delete("1.0", "end")

    def search(self):
        field = self.var_search_by.get()
        if not field:
            messagebox.showerror("Error", "Select a search field")
            return
        self.supplier_table.delete(*self.supplier_table.get_children())
        for row in search_suppliers(field, self.var_searchtxt.get()):
            self.supplier_table.insert("", "end", values=row)