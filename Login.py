import customtkinter as ctk
import sqlite3
import hashlib

COLORS = {
    "bg_main":     "#1A1A2E",
    "header":      "#162447",
    "sub_header":  "#1F4068",
    "card3":       "#ffd93d",
    "btn_green":   "#2ecc71",
    "btn_red":     "#e74c3c",
    "text_dim":    "#A0AEC0",
    "border":      "#0F3460",
}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def setup_users_table():
    """Create users table and insert default admin if not exists."""
    conn = sqlite3.connect("ims.db")
    cur  = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role     TEXT DEFAULT 'employee'
        )
    """)
    # Default admin: username=admin, password=admin123
    cur.execute("""
        INSERT OR IGNORE INTO users (username, password, role)
        VALUES (?, ?, 'admin')
    """, ("admin", hash_password("admin123")))

    # Default employee: username=employee, password=emp123
    cur.execute("""
        INSERT OR IGNORE INTO users (username, password, role)
        VALUES (?, ?, 'employee')
    """, ("employee", hash_password("emp123")))

    conn.commit()
    conn.close()

def check_login(username, password):
    """Returns role if valid, None if invalid."""
    conn = sqlite3.connect("ims.db")
    cur  = conn.cursor()
    cur.execute("""
        SELECT role FROM users
        WHERE username=? AND password=?
    """, (username, hash_password(password)))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


class LoginWindow:
    def __init__(self, on_success):
        """
        on_success: callback function called with (role, username)
                    when login is successful
        """
        self.on_success = on_success

        setup_users_table()

        # ── Window ──────────────────────────────────────────
        self.root = ctk.CTk()
        self.root.geometry("420x520")
        self.root.title("IMS — Login")
        self.root.configure(fg_color=COLORS["bg_main"])
        self.root.resizable(False, False)

        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - 420) // 2
        y = (self.root.winfo_screenheight() - 520) // 2
        self.root.geometry(f"420x520+{x}+{y}")

        self._build_ui()
        self.root.mainloop()

    def _build_ui(self):
        # Logo / Title area
        top = ctk.CTkFrame(self.root, fg_color=COLORS["header"], corner_radius=0)
        top.pack(fill="x")

        ctk.CTkLabel(top, text="🏪", font=("Arial", 48)).pack(pady=(30, 5))
        ctk.CTkLabel(top, text="Inventory Management System",
                     font=("Arial", 16, "bold"),
                     text_color=COLORS["card3"]).pack()
        ctk.CTkLabel(top, text="Please login to continue",
                     font=("Arial", 11),
                     text_color=COLORS["text_dim"]).pack(pady=(4, 20))

        # Form area
        form = ctk.CTkFrame(self.root, fg_color=COLORS["sub_header"], corner_radius=15)
        form.pack(fill="x", padx=30, pady=25)

        ctk.CTkLabel(form, text="Username", font=("Arial", 12),
                     text_color=COLORS["text_dim"]).pack(anchor="w", padx=20, pady=(20, 4))
        self.username_entry = ctk.CTkEntry(
            form, placeholder_text="Enter username",
            fg_color=COLORS["bg_main"], border_color=COLORS["border"],
            height=38, font=("Arial", 13)
        )
        self.username_entry.pack(fill="x", padx=20)

        ctk.CTkLabel(form, text="Password", font=("Arial", 12),
                     text_color=COLORS["text_dim"]).pack(anchor="w", padx=20, pady=(15, 4))
        self.password_entry = ctk.CTkEntry(
            form, placeholder_text="Enter password",
            fg_color=COLORS["bg_main"], border_color=COLORS["border"],
            height=38, font=("Arial", 13), show="*"
        )
        self.password_entry.pack(fill="x", padx=20)

        # Error label
        self.error_lbl = ctk.CTkLabel(form, text="", font=("Arial", 11),
                                      text_color="#ff4d6d")
        self.error_lbl.pack(pady=(8, 0))

        # Login button
        ctk.CTkButton(
            form, text="Login", height=42,
            fg_color=COLORS["btn_green"], hover_color="#27ae60",
            font=("Arial", 14, "bold"),
            command=self._attempt_login
        ).pack(fill="x", padx=20, pady=(10, 20))

        # Default credentials hint
        hint = ctk.CTkFrame(self.root, fg_color="transparent")
        hint.pack()
        ctk.CTkLabel(hint, text="Default — Admin: admin / admin123   |   Employee: employee / emp123",
                     font=("Arial", 9), text_color=COLORS["text_dim"]).pack()

        # Bind Enter key
        self.root.bind("<Return>", lambda e: self._attempt_login())
        self.username_entry.focus()

    def _attempt_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.error_lbl.configure(text="⚠ Please enter username and password")
            return

        role = check_login(username, password)

        if role:
            self.root.destroy()
            self.on_success(role, username)
        else:
            self.error_lbl.configure(text="❌ Invalid username or password")
            self.password_entry.delete(0, "end")