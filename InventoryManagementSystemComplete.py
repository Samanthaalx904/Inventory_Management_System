import customtkinter as ctk
from datetime import datetime
from Login import LoginWindow
from Database import setup_db

# ===== THEME COLORS =====
COLORS = {
    "bg_main":      "#1A1A2E",
    "header":       "#162447",
    "sub_header":   "#1F4068",
    "sidebar":      "#1B1B3A",
    "sidebar_hover":"#3F2A56",
    "menu_title":   "#ff4d6d",
    "card1":        "#ff6b6b",
    "card2":        "#4ecdc4",
    "card3":        "#ffd93d",
}

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Setup DB tables on startup
setup_db()

# ================================================================
# MAIN APP — built after successful login
# ================================================================
def launch_app(role, username):
    from EmployeeData import EmployeeClass
    from SupplierDetails import SupplierClass
    from Category import CategoryClass
    from ProductDetails import ProductClass
    from CustomerBill import CustomerBillClass
    from SalesBilling import SalesBillingClass

    app = ctk.CTk()
    app.geometry("1100x650")
    app.title("Inventory Management System")
    app.configure(fg_color=COLORS["bg_main"])

    # ── Helpers ──────────────────────────────────────────────
    def clear_content():
        for widget in content.winfo_children():
            widget.destroy()

    def logout():
        app.destroy()
        # Relaunch login window
        LoginWindow(on_success=launch_app)

    # ── Header ───────────────────────────────────────────────
    header = ctk.CTkFrame(app, height=60, fg_color=COLORS["header"])
    header.pack(fill="x")

    ctk.CTkLabel(header, text="Inventory Management System",
                 font=("Arial", 20, "bold")).pack(side="left", padx=20)

    # Show logged-in user + role
    ctk.CTkLabel(header,
                 text=f"👤 {username}  |  Role: {role.capitalize()}",
                 font=("Arial", 11), text_color=COLORS["card3"]
                 ).pack(side="left", padx=20)

    ctk.CTkButton(header, text="Logout",
                  fg_color="#ff5733", hover_color="#ff2e00",
                  command=logout).pack(side="right", padx=20, pady=10)

    # ── Sub Header ───────────────────────────────────────────
    sub_header = ctk.CTkFrame(app, height=30, fg_color=COLORS["sub_header"])
    sub_header.pack(fill="x")

    def update_time():
        now = datetime.now().strftime("Date: %d-%m-%Y | Time: %H:%M:%S")
        time_label.configure(text=f"Welcome, {username} | {now}")
        app.after(1000, update_time)

    time_label = ctk.CTkLabel(sub_header, text="")
    time_label.pack()
    update_time()

    # ── Main frame ───────────────────────────────────────────
    main_frame = ctk.CTkFrame(app, fg_color=COLORS["bg_main"])
    main_frame.pack(fill="both", expand=True)

    # ── Sidebar ──────────────────────────────────────────────
    sidebar = ctk.CTkFrame(main_frame, width=200, fg_color=COLORS["sidebar"])
    sidebar.pack(side="left", fill="y")

    ctk.CTkLabel(sidebar, text="Menu",
                 fg_color=COLORS["menu_title"], corner_radius=6
                 ).pack(pady=20, padx=20, fill="x")

    btn_style = {"fg_color": "transparent",
                 "hover_color": COLORS["sidebar_hover"],
                 "anchor": "w"}

    # ── Content area ─────────────────────────────────────────
    content = ctk.CTkFrame(main_frame, fg_color=COLORS["bg_main"])
    content.pack(fill="both", expand=True, padx=20, pady=20)

    # ── Page functions ───────────────────────────────────────
    def show_dashboard():
        clear_content()
        import sqlite3
        conn = sqlite3.connect("ims.db")
        cur  = conn.cursor()
        try:
            emp_count  = cur.execute("SELECT COUNT(*) FROM employee").fetchone()[0]
        except:
            emp_count  = 0
        try:
            sup_count  = cur.execute("SELECT COUNT(*) FROM supplier").fetchone()[0]
        except:
            sup_count  = 0
        try:
            prod_count = cur.execute("SELECT COUNT(*) FROM product").fetchone()[0]
        except:
            prod_count = 0
        try:
            sale_count = cur.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
        except:
            sale_count = 0
        conn.close()

        ctk.CTkLabel(content, text="Dashboard",
                     font=("Arial", 22, "bold")).pack(pady=10)

        card_frame = ctk.CTkFrame(content, fg_color="transparent")
        card_frame.pack(pady=20)

        for i, (label, count, color) in enumerate([
            ("Total Employees", emp_count,  COLORS["card1"]),
            ("Total Suppliers", sup_count,  COLORS["card2"]),
            ("Total Products",  prod_count, COLORS["card3"]),
            ("Total Sales",     sale_count, "#a29bfe"),
        ]):
            ctk.CTkLabel(card_frame,
                         text=f"{label}\n[ {count} ]",
                         fg_color=color, width=180, height=90,
                         corner_radius=10,
                         font=("Arial", 13, "bold"),
                         text_color="#1A1A2E"
                         ).grid(row=0, column=i, padx=15)

    def open_employee():
        clear_content()
        EmployeeClass(content)

    def open_supplier():
        clear_content()
        SupplierClass(content)

    def open_category():
        clear_content()
        CategoryClass(content)

    def open_product():
        clear_content()
        ProductClass(content)

    def open_sales():
        clear_content()
        SalesBillingClass(content)

    def open_customer_bill():
        clear_content()
        CustomerBillClass(content)

    # ── Build sidebar based on ROLE ───────────────────────────
    if role == "admin":
        # Admin sees everything
        ctk.CTkButton(sidebar, text="📊 Dashboard",
                      command=show_dashboard, **btn_style).pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(sidebar, text="👷 Employee",
                      command=open_employee, **btn_style).pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(sidebar, text="🚚 Supplier",
                      command=open_supplier, **btn_style).pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(sidebar, text="🗂 Category",
                      command=open_category, **btn_style).pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(sidebar, text="📦 Product",
                      command=open_product, **btn_style).pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(sidebar, text="🛒 Sales",
                      command=open_sales, **btn_style).pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(sidebar, text="🧾 Customer Bill",
                      command=open_customer_bill, **btn_style).pack(fill="x", padx=10, pady=5)

        # Default page for admin
        show_dashboard()

    else:
        # Employee sees only Sales & Billing
        ctk.CTkButton(sidebar, text="🛒 Sales & Billing",
                      command=open_sales, **btn_style).pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(sidebar, text="🧾 Customer Bill",
                      command=open_customer_bill, **btn_style).pack(fill="x", padx=10, pady=5)

        # Default page for employee
        open_sales()

    ctk.CTkButton(sidebar, text="🚪 Exit",
                  command=app.destroy, **btn_style).pack(fill="x", padx=10, pady=5)

    # ── Footer ───────────────────────────────────────────────
    footer = ctk.CTkFrame(app, height=20, fg_color=COLORS["header"])
    footer.pack(fill="x")
    ctk.CTkLabel(footer, text="IMS - Inventory Management System").pack()

    app.mainloop()


# ================================================================
# START — show login first
# ================================================================
LoginWindow(on_success=launch_app)