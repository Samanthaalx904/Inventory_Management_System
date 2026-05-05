import customtkinter as ctk
import sqlite3
from tkinter import ttk, messagebox
from Database import setup_db   # ← shared DB setup

# ===== THEME =====
COLORS = {
    "bg_main": "#1A1A2E",
    "header":  "#162447",
    "text":    "white"
}

class ProductClass:
    def __init__(self, parent):
        self.parent = parent

        # ===== VARIABLES =====
        self.var_id    = ctk.StringVar()
        self.var_name  = ctk.StringVar()
        self.var_cat   = ctk.StringVar()
        self.var_sup   = ctk.StringVar()
        self.var_price = ctk.StringVar()
        self.var_qty   = ctk.StringVar()

        setup_db()          # make sure table exists (safe to call multiple times)
        self.build_ui()
        self.load()

    # ================= UI =================
    def build_ui(self):

        ctk.CTkLabel(
            self.parent,
            text="PRODUCT MANAGEMENT",
            font=("Arial", 22, "bold")
        ).pack(pady=10)

        # ===== FORM =====
        form = ctk.CTkFrame(self.parent, fg_color=COLORS["header"])
        form.pack(fill="x", padx=20, pady=10)
        form.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkLabel(form, text="Name",     text_color="white").grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkEntry(form, textvariable=self.var_name,  height=32).grid(row=0, column=1, padx=10)

        ctk.CTkLabel(form, text="Category", text_color="white").grid(row=0, column=2)
        ctk.CTkEntry(form, textvariable=self.var_cat,   height=32).grid(row=0, column=3, padx=10)

        ctk.CTkLabel(form, text="Supplier", text_color="white").grid(row=1, column=0)
        ctk.CTkEntry(form, textvariable=self.var_sup,   height=32).grid(row=1, column=1, padx=10)

        ctk.CTkLabel(form, text="Price",    text_color="white").grid(row=1, column=2)
        ctk.CTkEntry(form, textvariable=self.var_price, height=32).grid(row=1, column=3, padx=10)

        ctk.CTkLabel(form, text="Qty",      text_color="white").grid(row=2, column=0)
        ctk.CTkEntry(form, textvariable=self.var_qty,   height=32).grid(row=2, column=1, padx=10)

        # ===== BUTTONS =====
        btn_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Add",    fg_color="#4ecdc4", command=self.add   ).grid(row=0, column=0, padx=10)
        ctk.CTkButton(btn_frame, text="Update", fg_color="#1f6aa5", command=self.update).grid(row=0, column=1, padx=10)
        ctk.CTkButton(btn_frame, text="Delete", fg_color="#ff4d6d", command=self.delete).grid(row=0, column=2, padx=10)
        ctk.CTkButton(btn_frame, text="Clear",  fg_color="#3F2A56", command=self.clear ).grid(row=0, column=3, padx=10)

        # ===== TABLE =====
        table_frame = ctk.CTkFrame(self.parent, fg_color=COLORS["bg_main"])
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#162447", foreground="white",
                        rowheight=28, fieldbackground="#162447")
        style.map("Treeview", background=[("selected", "#1F4068")])

        self.table = ttk.Treeview(
            table_frame,
            columns=("id", "name", "cat", "sup", "price", "qty", "status"),
            show="headings"
        )
        for col, label in [
            ("id", "ID"), ("name", "Name"), ("cat", "Category"),
            ("sup", "Supplier"), ("price", "Price"),
            ("qty", "QTY"), ("status", "Status")
        ]:
            self.table.heading(col, text=label)
            self.table.column(col, width=90, anchor="center")

        self.table.pack(fill="both", expand=True)
        self.table.bind("<ButtonRelease-1>", self.select)

    # ================= DATABASE FUNCTIONS =================
    def add(self):
        if not self.var_name.get():
            messagebox.showerror("Error", "Name is required")
            return
        if not self.var_price.get() or not self.var_qty.get():
            messagebox.showerror("Error", "Price and Qty are required")
            return

        try:
            price = float(self.var_price.get())
            qty   = int(self.var_qty.get())
        except ValueError:
            messagebox.showerror("Error", "Price must be a number, Qty must be a whole number")
            return

        conn = sqlite3.connect("ims.db")
        cur  = conn.cursor()
        cur.execute("""
            INSERT INTO product (name, category, supplier, price, qty, status)
            VALUES (?,?,?,?,?,'Active')
        """, (self.var_name.get(), self.var_cat.get(),
              self.var_sup.get(), price, qty))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Product '{self.var_name.get()}' added!")
        self.load()
        self.clear()

    def load(self):
        conn = sqlite3.connect("ims.db")
        cur  = conn.cursor()
        cur.execute("SELECT pid, name, category, supplier, price, qty, status FROM product")
        rows = cur.fetchall()
        conn.close()

        self.table.delete(*self.table.get_children())
        for r in rows:
            self.table.insert("", "end", values=r)

    def select(self, event):
        row  = self.table.focus()
        data = self.table.item(row).get("values")
        if not data:
            return
        self.var_id.set(data[0])
        self.var_name.set(data[1])
        self.var_cat.set(data[2])
        self.var_sup.set(data[3])
        self.var_price.set(data[4])
        self.var_qty.set(data[5])

    def update(self):
        if not self.var_id.get():
            messagebox.showerror("Error", "Select a product first")
            return
        try:
            price = float(self.var_price.get())
            qty   = int(self.var_qty.get())
        except ValueError:
            messagebox.showerror("Error", "Price must be a number, Qty must be a whole number")
            return

        conn = sqlite3.connect("ims.db")
        cur  = conn.cursor()
        cur.execute("""
            UPDATE product
            SET name=?, category=?, supplier=?, price=?, qty=?
            WHERE pid=?
        """, (self.var_name.get(), self.var_cat.get(),
              self.var_sup.get(), price, qty,
              self.var_id.get()))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Product updated!")
        self.load()
        self.clear()

    def delete(self):
        if not self.var_id.get():
            messagebox.showerror("Error", "Select a product first")
            return
        if not messagebox.askyesno("Confirm", "Delete this product?"):
            return

        conn = sqlite3.connect("ims.db")
        cur  = conn.cursor()
        cur.execute("DELETE FROM product WHERE pid=?", (self.var_id.get(),))
        conn.commit()
        conn.close()

        messagebox.showinfo("Deleted", "Product deleted!")
        self.load()
        self.clear()

    def clear(self):
        self.var_id.set("")
        self.var_name.set("")
        self.var_cat.set("")
        self.var_sup.set("")
        self.var_price.set("")
        self.var_qty.set("")