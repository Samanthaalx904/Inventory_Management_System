import sqlite3
import datetime

DB = "ims.db"

def get_conn():
    return sqlite3.connect(DB)

def setup_db():
    conn = get_conn()
    cur  = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        uid      INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role     TEXT NOT NULL DEFAULT 'employee'
    )
    """)
    cur.execute("""
        INSERT OR IGNORE INTO users (username, password, role)
        VALUES ('admin', 'admin123', 'admin')
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS employee (
        eid      TEXT PRIMARY KEY,
        name     TEXT,
        email    TEXT,
        gender   TEXT,
        contact  TEXT,
        dob      TEXT,
        doj      TEXT,
        password TEXT,
        utype    TEXT,
        salary   TEXT,
        address  TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS supplier (
        sid     INTEGER PRIMARY KEY AUTOINCREMENT,
        name    TEXT NOT NULL,
        contact TEXT,
        email   TEXT,
        address TEXT,
        company TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS category (
        cid         INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT NOT NULL UNIQUE,
        description TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS product (
        pid      INTEGER PRIMARY KEY AUTOINCREMENT,
        name     TEXT NOT NULL,
        category TEXT,
        supplier TEXT,
        price    REAL DEFAULT 0,
        qty      INTEGER DEFAULT 0,
        status   TEXT DEFAULT 'Active'
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        sid      INTEGER PRIMARY KEY AUTOINCREMENT,
        customer TEXT,
        contact  TEXT,
        total    REAL DEFAULT 0,
        discount REAL DEFAULT 0,
        net      REAL DEFAULT 0,
        date     TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sale_items (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        sale_id      INTEGER NOT NULL,
        product_id   INTEGER,
        product_name TEXT,
        qty          INTEGER DEFAULT 1,
        price        REAL DEFAULT 0,
        total        REAL DEFAULT 0,
        FOREIGN KEY (sale_id) REFERENCES sales(sid)
    )
    """)

    conn.commit()
    conn.close()


# ══════════════════════════════════════════════════════════════════
# USERS / AUTH
# ══════════════════════════════════════════════════════════════════
def validate_login(username, password):
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("SELECT role FROM users WHERE username=? AND password=?",
                (username, password))
    row = cur.fetchone()
    conn.close()
    return (row[0], username) if row else None

def add_user(username, password, role="employee"):
    conn = get_conn()
    cur  = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password, role) VALUES (?,?,?)",
                    (username, password, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_users():
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("SELECT uid, username, role FROM users")
    rows = cur.fetchall()
    conn.close()
    return rows


# ══════════════════════════════════════════════════════════════════
# EMPLOYEES
# ══════════════════════════════════════════════════════════════════
def get_all_employees():
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM employee")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_employee(data: dict):
    conn = get_conn()
    cur  = conn.cursor()
    try:
        cur.execute("INSERT INTO employee VALUES (?,?,?,?,?,?,?,?,?,?,?)", (
            data["eid"], data["name"], data["email"], data["gender"],
            data["contact"], data["dob"], data["doj"], data["password"],
            data["utype"], data["salary"], data["address"]
        ))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def update_employee(data: dict):
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("""
        UPDATE employee SET
            name=?, email=?, gender=?, contact=?, dob=?, doj=?,
            password=?, utype=?, salary=?, address=?
        WHERE eid=?
    """, (
        data["name"], data["email"], data["gender"], data["contact"],
        data["dob"], data["doj"], data["password"], data["utype"],
        data["salary"], data["address"], data["eid"]
    ))
    conn.commit()
    conn.close()

def delete_employee(eid):
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("DELETE FROM employee WHERE eid=?", (eid,))
    conn.commit()
    conn.close()

def search_employees(field, value):
    allowed = {"eid", "name", "email", "contact"}
    if field not in allowed:
        return []
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute(f"SELECT * FROM employee WHERE {field} LIKE ?", (f"%{value}%",))
    rows = cur.fetchall()
    conn.close()
    return rows


# ══════════════════════════════════════════════════════════════════
# SUPPLIERS
# ══════════════════════════════════════════════════════════════════
def get_all_suppliers():
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM supplier")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_supplier(name, contact, email, address, company):
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("INSERT INTO supplier (name,contact,email,address,company) VALUES (?,?,?,?,?)",
                (name, contact, email, address, company))
    conn.commit()
    conn.close()

def update_supplier(sid, name, contact, email, address, company):
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("""
        UPDATE supplier SET name=?, contact=?, email=?, address=?, company=?
        WHERE sid=?
    """, (name, contact, email, address, company, sid))
    conn.commit()
    conn.close()

def delete_supplier(sid):
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("DELETE FROM supplier WHERE sid=?", (sid,))
    conn.commit()
    conn.close()

def search_suppliers(field, value):
    allowed = {"name", "contact", "email", "company"}
    if field not in allowed:
        return []
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute(f"SELECT * FROM supplier WHERE {field} LIKE ?", (f"%{value}%",))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_supplier_names():
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("SELECT name FROM supplier")
    rows = [r[0] for r in cur.fetchall()]
    conn.close()
    return rows


# ══════════════════════════════════════════════════════════════════
# CATEGORIES
# ══════════════════════════════════════════════════════════════════
def get_all_categories():
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM category")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_category(name, description=""):
    conn = get_conn()
    cur  = conn.cursor()
    try:
        cur.execute("INSERT INTO category (name, description) VALUES (?,?)",
                    (name, description))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def update_category(cid, name, description=""):
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("UPDATE category SET name=?, description=? WHERE cid=?",
                (name, description, cid))
    conn.commit()
    conn.close()

def delete_category(cid):
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("DELETE FROM category WHERE cid=?", (cid,))
    conn.commit()
    conn.close()

def get_category_names():
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("SELECT name FROM category")
    rows = [r[0] for r in cur.fetchall()]
    conn.close()
    return rows


# ══════════════════════════════════════════════════════════════════
# PRODUCTS
# ══════════════════════════════════════════════════════════════════
def get_all_products():
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM product")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_active_products():
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("""
        SELECT pid, name, price, qty, status
        FROM product
        WHERE status = 'Active' AND qty > 0
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def add_product(name, category, supplier, price, qty, status="Active"):
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("""
        INSERT INTO product (name, category, supplier, price, qty, status)
        VALUES (?,?,?,?,?,?)
    """, (name, category, supplier, price, qty, status))
    conn.commit()
    conn.close()

def update_product(pid, name, category, supplier, price, qty, status):
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("""
        UPDATE product SET name=?, category=?, supplier=?, price=?, qty=?, status=?
        WHERE pid=?
    """, (name, category, supplier, price, qty, status, pid))
    conn.commit()
    conn.close()

def delete_product(pid):
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("DELETE FROM product WHERE pid=?", (pid,))
    conn.commit()
    conn.close()

def search_products(field, value):
    allowed = {"name", "category", "supplier", "status"}
    if field not in allowed:
        return []
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute(f"SELECT * FROM product WHERE {field} LIKE ?", (f"%{value}%",))
    rows = cur.fetchall()
    conn.close()
    return rows


# ══════════════════════════════════════════════════════════════════
# SALES
# ══════════════════════════════════════════════════════════════════
def save_sale(customer, contact, cart, discount_pct=5):
    bill     = sum(c["total"] for c in cart)
    discount = round(bill * discount_pct / 100, 2)
    net      = round(bill - discount, 2)
    date     = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

    conn = get_conn()
    cur  = conn.cursor()

    cur.execute("""
        INSERT INTO sales (customer, contact, total, discount, net, date)
        VALUES (?,?,?,?,?,?)
    """, (customer, contact, bill, discount, net, date))

    sale_id = cur.lastrowid

    for item in cart:
        cur.execute("""
            INSERT INTO sale_items
                (sale_id, product_id, product_name, qty, price, total)
            VALUES (?,?,?,?,?,?)
        """, (sale_id, item["pid"], item["name"],
              item["qty"], item["price"], item["total"]))

        cur.execute("UPDATE product SET qty = qty - ? WHERE pid = ?",
                    (item["qty"], item["pid"]))

    conn.commit()
    conn.close()
    return sale_id

def get_all_sales():
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM sales ORDER BY sid DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_sale_items(sale_id):
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM sale_items WHERE sale_id=?", (sale_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_sale_by_id(sale_id):
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM sales WHERE sid=?", (sale_id,))
    row = cur.fetchone()
    conn.close()
    return row

def delete_sale(sid):
    """Delete a bill, its line items, and restore stock."""
    conn = get_conn()
    cur  = conn.cursor()

    # Restore stock for each item in this bill
    items = cur.execute(
        "SELECT product_id, qty FROM sale_items WHERE sale_id=?", (sid,)
    ).fetchall()
    for product_id, qty in items:
        cur.execute("UPDATE product SET qty = qty + ? WHERE pid = ?",
                    (qty, product_id))

    cur.execute("DELETE FROM sale_items WHERE sale_id=?", (sid,))
    cur.execute("DELETE FROM sales WHERE sid=?", (sid,))

    conn.commit()
    conn.close()


# ══════════════════════════════════════════════════════════════════
# DASHBOARD COUNTS
# ══════════════════════════════════════════════════════════════════
def get_counts():
    conn = get_conn()
    cur  = conn.cursor()
    counts = {
        "employees":  cur.execute("SELECT COUNT(*) FROM employee").fetchone()[0],
        "suppliers":  cur.execute("SELECT COUNT(*) FROM supplier").fetchone()[0],
        "categories": cur.execute("SELECT COUNT(*) FROM category").fetchone()[0],
        "products":   cur.execute("SELECT COUNT(*) FROM product").fetchone()[0],
        "sales":      cur.execute("SELECT COUNT(*) FROM sales").fetchone()[0],
    }
    conn.close()
    return counts