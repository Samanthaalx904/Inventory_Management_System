# 📦 Inventory Management System (IMS)

A full-featured desktop **Inventory Management System** built with Python and CustomTkinter. It features a modern dark-themed UI, role-based access control, and a local SQLite database — all packaged as a standalone desktop application.

---



> Dark-themed UI with sidebar navigation, dashboard cards, and a real-time clock display.

---

## ✨ Features

- 🔐 **Login System** — Secure authentication with role-based access (Admin / Employee)
- 📊 **Dashboard** — Live summary cards showing total Employees, Suppliers, Products, and Sales
- 👷 **Employee Management** — Add, view, and manage employee records
- 🚚 **Supplier Management** — Track supplier details and contacts
- 🗂️ **Category Management** — Organize products by category
- 📦 **Product Management** — Full product inventory with details
- 🛒 **Sales & Billing** — Create and process sales transactions
- 🧾 **Customer Bill** — Generate and view customer bills
- 🕒 **Real-Time Clock** — Live date and time shown in the sub-header
- 🚪 **Logout / Exit** — Session management with easy logout and re-login

---

## 🛡️ Role-Based Access Control

| Feature            | Admin | Employee |
|--------------------|:-----:|:--------:|
| Dashboard          | ✅    | ❌       |
| Employee Module    | ✅    | ❌       |
| Supplier Module    | ✅    | ❌       |
| Category Module    | ✅    | ❌       |
| Product Module     | ✅    | ❌       |
| Sales & Billing    | ✅    | ✅       |
| Customer Bill      | ✅    | ✅       |

---

## 🗂️ Project Structure

```
inventory-management-system/
│
├── main.py                # App entry point — launches login, then main window
├── Login.py               # Login window UI and authentication logic
├── Database.py            # Database setup (setup_db) — creates all tables
├── EmployeeData.py        # Employee CRUD module
├── SupplierDetails.py     # Supplier CRUD module
├── Category.py            # Category CRUD module
├── ProductDetails.py      # Product CRUD module
├── SalesBilling.py        # Sales & billing module
├── CustomerBill.py        # Customer bill viewer/generator
├── ims.db                 # SQLite database (auto-created on first run)
└── README.md
```

---

## 🛠️ Tech Stack

| Layer        | Technology                          |
|--------------|-------------------------------------|
| Language     | Python 3.x                          |
| GUI          | [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) |
| Database     | SQLite3 (built-in)                  |
| Datetime     | Python `datetime` module            |

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/inventory-management-system.git
cd inventory-management-system
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install customtkinter
```

> **Note:** All other dependencies (`sqlite3`, `datetime`) are part of Python's standard library.

### 4. Run the Application

```bash
python main.py
```

The database (`ims.db`) will be created automatically on first launch via `setup_db()`.

---

## 🔑 Default Login Credentials

> ⚠️ Change these credentials after your first login for security.

| Role     | Username | Password  |
|----------|----------|-----------|
| Admin    | `admin`  | `admin123`|
| Employee | `emp1`   | `emp123`  |

*(Credentials are configured in `Database.py` or `Login.py` — update as needed.)*

---

## 🗃️ Database Schema

The SQLite database (`ims.db`) is initialized automatically. Key tables include:

| Table      | Description                          |
|------------|--------------------------------------|
| `users`    | Stores login credentials and roles   |
| `employee` | Employee records                     |
| `supplier` | Supplier contact details             |
| `category` | Product categories                   |
| `product`  | Product inventory data               |
| `sales`    | Sales transaction records            |

---

## 🎨 Theme & Colors

The UI uses a consistent dark color palette defined in `main.py`:

| Token           | Color     | Usage                    |
|-----------------|-----------|--------------------------|
| `bg_main`       | `#1A1A2E` | Main background          |
| `header`        | `#162447` | Top header bar           |
| `sub_header`    | `#1F4068` | Sub-header / time bar    |
| `sidebar`       | `#1B1B3A` | Sidebar background       |
| `sidebar_hover` | `#3F2A56` | Sidebar button hover     |
| `menu_title`    | `#ff4d6d` | "Menu" label             |
| `card1`         | `#ff6b6b` | Employees card           |
| `card2`         | `#4ecdc4` | Suppliers card           |
| `card3`         | `#ffd93d` | Products card / username |

---

## 🔄 Application Flow

```
main.py
  └── LoginWindow()
        └── on_success(role, username)
              └── launch_app(role, username)
                    ├── Header (title, user info, logout)
                    ├── Sub-Header (live clock)
                    ├── Sidebar (role-filtered menu)
                    └── Content Area (dynamic module loading)
```

---

## 📋 Requirements

- Python **3.8+**
- `customtkinter >= 5.0`
- OS: Windows, macOS, or Linux

---

## 🚀 Future Improvements

- [ ] PDF export for invoices and reports
- [ ] Search and filter across all modules
- [ ] Low-stock alerts and notifications
- [ ] Data export to Excel/CSV
- [ ] Charts and graphs on the dashboard
- [ ] User management panel for admins
- [ ] Password hashing for secure credential storage

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👤 Author

**Your Name**
- GitHub: [@your-username](https://github.com/your-username)
- Email: your.email@example.com

---

> Built with ❤️ using Python & CustomTkinter
