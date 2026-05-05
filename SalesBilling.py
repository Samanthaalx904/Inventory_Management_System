import customtkinter as ctk
from tkinter import ttk, messagebox
import datetime
from Database import get_active_products, save_sale   # ← capital D

# ===== COLORS =====
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
    "panel":         "#16213E",
    "border":        "#0F3460",
    "accent":        "#E94560",
    "btn_green":     "#2ecc71",
    "btn_red":       "#e74c3c",
    "btn_orange":    "#f39c12",
    "btn_blue":      "#2980b9",
    "btn_teal":      "#1abc9c",
    "text_white":    "#FFFFFF",
    "text_dim":      "#A0AEC0",
    "calc_btn":      "#0F3460",
    "calc_hover":    "#1F4068",
    "calc_op":       "#E94560",
    "calc_op_hover": "#c0392b",
}


class SalesBillingClass:
    def __init__(self, parent):
        self.parent = parent
        self.cart = []
        self.calc_value = ""
        self.selected_product = None
        self._load_products_from_db()
        self.build_ui()

    def _load_products_from_db(self):
        rows = get_active_products()
        self.products = [
            {"pid": r[0], "name": r[1], "price": float(r[2]),
             "qty": int(r[3]), "status": r[4]}
            for r in rows
        ]
        self.filtered_products = list(self.products)

    def _refresh_products(self):
        self._load_products_from_db()
        self.filtered_products = list(self.products)
        self._populate_products()

    def build_ui(self):
        title_bar = ctk.CTkFrame(self.parent, fg_color=COLORS["header"], corner_radius=10)
        title_bar.pack(fill="x", padx=5, pady=(0, 8))

        ctk.CTkLabel(title_bar, text="🛒  Sales & Billing",
                     font=("Trebuchet MS", 20, "bold"),
                     text_color=COLORS["card3"]).pack(side="left", padx=15, pady=8)

        now = datetime.datetime.now().strftime("Date: %d-%m-%Y   |   Time: %H:%M")
        ctk.CTkLabel(title_bar, text=now, font=("Consolas", 12),
                     text_color=COLORS["text_dim"]).pack(side="right", padx=15)

        ctk.CTkButton(title_bar, text="🔄 Refresh Products", width=150, height=28,
                      fg_color=COLORS["btn_teal"], hover_color=COLORS["sub_header"],
                      font=("Arial", 10, "bold"),
                      command=self._refresh_products).pack(side="right", padx=10)

        body = ctk.CTkFrame(self.parent, fg_color="transparent")
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=4)
        body.columnconfigure(2, weight=3)
        body.rowconfigure(0, weight=1)

        self._build_products_panel(body)
        self._build_middle_panel(body)
        self._build_billing_panel(body)

    def _build_products_panel(self, body):
        panel = ctk.CTkFrame(body, fg_color=COLORS["panel"], corner_radius=12)
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=0)
        panel.rowconfigure(2, weight=1)
        panel.columnconfigure(0, weight=1)

        hdr = ctk.CTkFrame(panel, fg_color=COLORS["sub_header"], corner_radius=8)
        hdr.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 4))
        ctk.CTkLabel(hdr, text="All Products", font=("Trebuchet MS", 14, "bold"),
                     text_color=COLORS["card3"]).pack(side="left", padx=10, pady=6)

        search_frame = ctk.CTkFrame(panel, fg_color="transparent")
        search_frame.grid(row=1, column=0, sticky="ew", padx=8, pady=4)
        search_frame.columnconfigure(1, weight=1)

        ctk.CTkLabel(search_frame, text="Search:", font=("Arial", 11),
                     text_color=COLORS["text_dim"]).grid(row=0, column=0, padx=(0, 4))

        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self._filter_products)
        ctk.CTkEntry(search_frame, textvariable=self.search_var,
                     placeholder_text="Product name...",
                     fg_color=COLORS["bg_main"], border_color=COLORS["border"],
                     height=30).grid(row=0, column=1, sticky="ew")

        ctk.CTkButton(search_frame, text="Show All", width=70, height=30,
                      fg_color=COLORS["btn_blue"], hover_color=COLORS["sub_header"],
                      command=self._show_all_products).grid(row=0, column=2, padx=(4, 0))

        tree_frame = ctk.CTkFrame(panel, fg_color="transparent")
        tree_frame.grid(row=2, column=0, sticky="nsew", padx=8, pady=(4, 8))
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Products.Treeview",
                        background=COLORS["bg_main"], foreground="white",
                        rowheight=28, fieldbackground=COLORS["bg_main"],
                        font=("Consolas", 10))
        style.configure("Products.Treeview.Heading",
                        background=COLORS["border"], foreground=COLORS["card3"],
                        font=("Arial", 10, "bold"))
        style.map("Products.Treeview", background=[("selected", COLORS["accent"])])

        self.product_tree = ttk.Treeview(
            tree_frame, style="Products.Treeview",
            columns=("PID", "Name", "Price", "QTY", "Status"),
            show="headings", selectmode="browse"
        )
        for col, w in [("PID", 35), ("Name", 110), ("Price", 65), ("QTY", 45), ("Status", 55)]:
            self.product_tree.heading(col, text=col)
            self.product_tree.column(col, width=w, anchor="center")

        sb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.product_tree.yview)
        self.product_tree.configure(yscrollcommand=sb.set)
        self.product_tree.grid(row=0, column=0, sticky="nsew")
        sb.grid(row=0, column=1, sticky="ns")

        self.product_tree.bind("<<TreeviewSelect>>", self._on_product_select)
        self._populate_products()

        ctk.CTkLabel(panel, text="Note: Enter 0 QTY to remove from cart",
                     font=("Arial", 9), text_color=COLORS["text_dim"]).grid(
            row=3, column=0, padx=8, pady=(0, 6))

    def _build_middle_panel(self, body):
        panel = ctk.CTkFrame(body, fg_color=COLORS["panel"], corner_radius=12)
        panel.grid(row=0, column=1, sticky="nsew", padx=5, pady=0)
        panel.columnconfigure(0, weight=1)

        cust_hdr = ctk.CTkFrame(panel, fg_color=COLORS["sub_header"], corner_radius=8)
        cust_hdr.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 4))
        ctk.CTkLabel(cust_hdr, text="Customer Details",
                     font=("Trebuchet MS", 14, "bold"),
                     text_color=COLORS["card3"]).pack(padx=10, pady=6)

        cust_form = ctk.CTkFrame(panel, fg_color="transparent")
        cust_form.grid(row=1, column=0, sticky="ew", padx=12, pady=6)
        cust_form.columnconfigure(1, weight=1)
        cust_form.columnconfigure(3, weight=1)

        ctk.CTkLabel(cust_form, text="Name", font=("Arial", 11),
                     text_color=COLORS["text_dim"]).grid(row=0, column=0, padx=(0, 6), sticky="w")
        self.cust_name = ctk.CTkEntry(cust_form, placeholder_text="Customer name",
                                      fg_color=COLORS["bg_main"],
                                      border_color=COLORS["border"], height=30)
        self.cust_name.grid(row=0, column=1, sticky="ew", padx=(0, 12))

        ctk.CTkLabel(cust_form, text="Contact", font=("Arial", 11),
                     text_color=COLORS["text_dim"]).grid(row=0, column=2, padx=(0, 6), sticky="w")
        self.cust_contact = ctk.CTkEntry(cust_form, placeholder_text="03xx-xxxxxxx",
                                         fg_color=COLORS["bg_main"],
                                         border_color=COLORS["border"], height=30)
        self.cust_contact.grid(row=0, column=3, sticky="ew")

        calc_disp_frame = ctk.CTkFrame(panel, fg_color=COLORS["bg_main"],
                                       corner_radius=8, border_width=1,
                                       border_color=COLORS["border"])
        calc_disp_frame.grid(row=2, column=0, sticky="ew", padx=12, pady=6)

        self.calc_display = ctk.CTkLabel(calc_disp_frame, text="0",
                                         font=("Consolas", 22, "bold"),
                                         text_color=COLORS["card3"], anchor="e")
        self.calc_display.pack(fill="x", padx=12, pady=8)

        calc_frame = ctk.CTkFrame(panel, fg_color="transparent")
        calc_frame.grid(row=3, column=0, padx=12, pady=4)

        for r, row in enumerate([
            ["7", "8", "9", "+"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "*"],
            ["0", "C", "=", "/"],
        ]):
            for c, lbl in enumerate(row):
                is_op    = lbl in ("+", "-", "*", "/", "=")
                is_clear = lbl == "C"
                fg = COLORS["calc_op"] if is_op else (COLORS["btn_orange"] if is_clear else COLORS["calc_btn"])
                hv = COLORS["calc_op_hover"] if is_op else (COLORS["btn_red"] if is_clear else COLORS["calc_hover"])
                ctk.CTkButton(calc_frame, text=lbl, width=62, height=50,
                              font=("Consolas", 16, "bold"),
                              fg_color=fg, hover_color=hv, corner_radius=8,
                              command=lambda x=lbl: self._calc_press(x)
                              ).grid(row=r, column=c, padx=4, pady=4)

        info_hdr = ctk.CTkFrame(panel, fg_color=COLORS["sub_header"], corner_radius=6)
        info_hdr.grid(row=4, column=0, sticky="ew", padx=8, pady=(8, 2))
        ctk.CTkLabel(info_hdr, text="Selected Product Info",
                     font=("Arial", 11, "bold"),
                     text_color=COLORS["card3"]).pack(padx=10, pady=4)

        info_form = ctk.CTkFrame(panel, fg_color="transparent")
        info_form.grid(row=5, column=0, sticky="ew", padx=12, pady=4)
        info_form.columnconfigure(1, weight=1)
        info_form.columnconfigure(3, weight=1)
        info_form.columnconfigure(5, weight=1)

        for i, (lbl, attr) in enumerate([
            ("Product",   "prod_name_lbl"),
            ("Price/Qty", "prod_price_lbl"),
            ("Quantity",  "prod_qty_entry"),
        ]):
            ctk.CTkLabel(info_form, text=lbl, font=("Arial", 10),
                         text_color=COLORS["text_dim"]).grid(row=0, column=i*2, padx=(0, 4))
            if attr == "prod_qty_entry":
                self.prod_qty_entry = ctk.CTkEntry(
                    info_form, width=70, fg_color=COLORS["bg_main"],
                    border_color=COLORS["card3"], height=28,
                    textvariable=ctk.StringVar(value="1"))
                self.prod_qty_entry.grid(row=0, column=i*2+1, padx=(0, 8), sticky="ew")
            else:
                w = ctk.CTkLabel(info_form, text="---",
                                 font=("Consolas", 10, "bold"),
                                 fg_color=COLORS["bg_main"],
                                 corner_radius=6, width=100)
                w.grid(row=0, column=i*2+1, padx=(0, 8), sticky="ew")
                setattr(self, attr, w)

        self.in_stock_lbl = ctk.CTkLabel(panel, text="In Stock: ---",
                                         font=("Arial", 10), text_color=COLORS["card2"])
        self.in_stock_lbl.grid(row=6, column=0, sticky="w", padx=14)

        action_frame = ctk.CTkFrame(panel, fg_color="transparent")
        action_frame.grid(row=7, column=0, sticky="ew", padx=12, pady=8)
        action_frame.columnconfigure(0, weight=1)
        action_frame.columnconfigure(1, weight=1)
        action_frame.columnconfigure(2, weight=1)

        ctk.CTkButton(action_frame, text="Clear Selection",
                      fg_color=COLORS["btn_red"], hover_color="#c0392b",
                      font=("Arial", 11, "bold"), height=36,
                      command=self._clear_selection).grid(row=0, column=0, padx=3, sticky="ew")

        ctk.CTkButton(action_frame, text="⟵ Use Calc",
                      fg_color=COLORS["btn_orange"], hover_color="#d68910",
                      font=("Arial", 11, "bold"), height=36,
                      command=self._use_calc_qty).grid(row=0, column=1, padx=3, sticky="ew")

        ctk.CTkButton(action_frame, text="Add / Update Cart ✔",
                      fg_color=COLORS["btn_green"], hover_color="#27ae60",
                      font=("Arial", 11, "bold"), height=36,
                      command=self._add_to_cart).grid(row=0, column=2, padx=3, sticky="ew")

    def _build_billing_panel(self, body):
        panel = ctk.CTkFrame(body, fg_color=COLORS["panel"], corner_radius=12)
        panel.grid(row=0, column=2, sticky="nsew", padx=(5, 0), pady=0)
        panel.rowconfigure(2, weight=1)
        panel.columnconfigure(0, weight=1)

        hdr = ctk.CTkFrame(panel, fg_color=COLORS["accent"], corner_radius=8)
        hdr.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 4))
        ctk.CTkLabel(hdr, text="🧾  Customer Billing Area",
                     font=("Trebuchet MS", 14, "bold"),
                     text_color="white").pack(side="left", padx=10, pady=6)

        self.cart_count_lbl = ctk.CTkLabel(hdr, text="Total Products: [0]",
                                           font=("Arial", 11), text_color=COLORS["card3"])
        self.cart_count_lbl.pack(side="right", padx=10)

        cart_cols = ctk.CTkFrame(panel, fg_color=COLORS["sub_header"], corner_radius=6)
        cart_cols.grid(row=1, column=0, sticky="ew", padx=8, pady=2)
        for i, (lbl, w) in enumerate([("PID", 40), ("Product", 140), ("QTY", 50), ("Price", 70), ("Total", 80)]):
            ctk.CTkLabel(cart_cols, text=lbl, font=("Arial", 10, "bold"),
                         text_color=COLORS["card3"], width=w,
                         anchor="center").grid(row=0, column=i, padx=2, pady=4)

        cart_frame = ctk.CTkFrame(panel, fg_color="transparent")
        cart_frame.grid(row=2, column=0, sticky="nsew", padx=8, pady=2)
        cart_frame.rowconfigure(0, weight=1)
        cart_frame.columnconfigure(0, weight=1)

        style = ttk.Style()
        style.configure("Cart.Treeview",
                        background=COLORS["bg_main"], foreground="white",
                        rowheight=30, fieldbackground=COLORS["bg_main"],
                        font=("Consolas", 10))
        style.configure("Cart.Treeview.Heading",
                        background=COLORS["border"], foreground=COLORS["card3"],
                        font=("Arial", 10, "bold"))
        style.map("Cart.Treeview", background=[("selected", COLORS["accent"])])

        self.cart_tree = ttk.Treeview(
            cart_frame, style="Cart.Treeview",
            columns=("PID", "Product", "QTY", "Price", "Total"),
            show="headings", selectmode="browse"
        )
        for col, w in [("PID", 40), ("Product", 130), ("QTY", 45), ("Price", 65), ("Total", 75)]:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=w, anchor="center")

        csb = ttk.Scrollbar(cart_frame, orient="vertical", command=self.cart_tree.yview)
        self.cart_tree.configure(yscrollcommand=csb.set)
        self.cart_tree.grid(row=0, column=0, sticky="nsew")
        csb.grid(row=0, column=1, sticky="ns")

        totals = ctk.CTkFrame(panel, fg_color=COLORS["header"], corner_radius=10)
        totals.grid(row=3, column=0, sticky="ew", padx=8, pady=(4, 4))
        totals.columnconfigure((0, 1, 2), weight=1)

        for col, (label, attr, color) in enumerate([
            ("Bill Amount", "bill_amount_lbl", COLORS["card1"]),
            ("Discount 5%", "discount_lbl",    COLORS["card2"]),
            ("Net Pay",     "net_pay_lbl",      COLORS["card3"]),
        ]):
            box = ctk.CTkFrame(totals, fg_color=COLORS["sub_header"], corner_radius=8)
            box.grid(row=0, column=col, padx=6, pady=6, sticky="ew")
            ctk.CTkLabel(box, text=label, font=("Arial", 10, "bold"),
                         text_color=color).pack(pady=(6, 0))
            val_lbl = ctk.CTkLabel(box, text="0", font=("Consolas", 14, "bold"),
                                   text_color="white")
            val_lbl.pack(pady=(0, 6))
            setattr(self, attr, val_lbl)

        bill_btns = ctk.CTkFrame(panel, fg_color="transparent")
        bill_btns.grid(row=4, column=0, sticky="ew", padx=8, pady=(2, 8))
        bill_btns.columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(bill_btns, text="🖨 Print",
                      fg_color=COLORS["btn_blue"], hover_color=COLORS["sub_header"],
                      font=("Arial", 11, "bold"), height=38,
                      command=self._print_bill).grid(row=0, column=0, padx=3, sticky="ew")

        ctk.CTkButton(bill_btns, text="🗑 Clear All",
                      fg_color=COLORS["btn_red"], hover_color="#c0392b",
                      font=("Arial", 11, "bold"), height=38,
                      command=self._clear_cart).grid(row=0, column=1, padx=3, sticky="ew")

        ctk.CTkButton(bill_btns, text="💾 Save Bill",
                      fg_color=COLORS["btn_green"], hover_color="#27ae60",
                      font=("Arial", 11, "bold"), height=38,
                      command=self._save_bill).grid(row=0, column=2, padx=3, sticky="ew")

    def _populate_products(self):
        for i in self.product_tree.get_children():
            self.product_tree.delete(i)
        for p in self.filtered_products:
            self.product_tree.insert("", "end",
                                     values=(p["pid"], p["name"],
                                             f"Rs {p['price']:,.0f}",
                                             p["qty"], p["status"]))

    def _filter_products(self, *_):
        q = self.search_var.get().lower()
        self.filtered_products = [p for p in self.products if q in p["name"].lower()]
        self._populate_products()

    def _show_all_products(self):
        self.search_var.set("")
        self.filtered_products = list(self.products)
        self._populate_products()

    def _on_product_select(self, event):
        sel = self.product_tree.selection()
        if not sel:
            return
        item = self.product_tree.item(sel[0])
        pid  = item["values"][0]
        self.selected_product = next((p for p in self.products if p["pid"] == pid), None)
        if self.selected_product:
            self.prod_name_lbl.configure(text=self.selected_product["name"])
            self.prod_price_lbl.configure(text=f"Rs {self.selected_product['price']:,.0f}")
            self.in_stock_lbl.configure(
                text=f"In Stock: {self.selected_product['qty']} units",
                text_color=COLORS["card2"]
            )
            existing = next((c for c in self.cart if c["pid"] == pid), None)
            self.prod_qty_entry.delete(0, "end")
            self.prod_qty_entry.insert(0, str(existing["qty"]) if existing else "1")

    def _calc_press(self, key):
        if key == "C":
            self.calc_value = ""
            self.calc_display.configure(text="0")
        elif key == "=":
            try:
                result = eval(self.calc_value)
                self.calc_value = str(result)
                self.calc_display.configure(text=self.calc_value)
            except Exception:
                self.calc_display.configure(text="Error")
                self.calc_value = ""
        else:
            self.calc_value += str(key)
            self.calc_display.configure(text=self.calc_value)

    def _use_calc_qty(self):
        val = self.calc_display.cget("text")
        try:
            qty = int(float(val))
            self.prod_qty_entry.delete(0, "end")
            self.prod_qty_entry.insert(0, str(qty))
        except ValueError:
            messagebox.showwarning("Invalid", "Calculator has no valid number.")

    def _add_to_cart(self):
        if not self.selected_product:
            messagebox.showwarning("No Product", "Please select a product first.")
            return
        try:
            qty = int(self.prod_qty_entry.get())
        except ValueError:
            messagebox.showerror("Invalid QTY", "Enter a valid quantity.")
            return

        pid = self.selected_product["pid"]

        if qty == 0:
            self.cart = [c for c in self.cart if c["pid"] != pid]
        elif qty < 0:
            messagebox.showerror("Invalid QTY", "Quantity cannot be negative.")
            return
        elif qty > self.selected_product["qty"]:
            messagebox.showwarning("Stock Issue",
                                   f"Only {self.selected_product['qty']} units available.")
            return
        else:
            total    = qty * self.selected_product["price"]
            existing = next((c for c in self.cart if c["pid"] == pid), None)
            if existing:
                existing["qty"]   = qty
                existing["total"] = total
            else:
                self.cart.append({
                    "pid":   pid,
                    "name":  self.selected_product["name"],
                    "price": self.selected_product["price"],
                    "qty":   qty,
                    "total": total,
                })
        self._refresh_cart()

    def _refresh_cart(self):
        for i in self.cart_tree.get_children():
            self.cart_tree.delete(i)
        for item in self.cart:
            self.cart_tree.insert("", "end", values=(
                item["pid"], item["name"], item["qty"],
                f"Rs {item['price']:,.0f}", f"Rs {item['total']:,.0f}"
            ))
        self.cart_count_lbl.configure(text=f"Total Products: [{len(self.cart)}]")
        bill     = sum(c["total"] for c in self.cart)
        discount = round(bill * 0.05)
        net      = bill - discount
        self.bill_amount_lbl.configure(text=f"Rs {bill:,.0f}")
        self.discount_lbl.configure(text=f"Rs {discount:,.0f}")
        self.net_pay_lbl.configure(text=f"Rs {net:,.0f}")

    def _clear_selection(self):
        self.selected_product = None
        self.prod_name_lbl.configure(text="---")
        self.prod_price_lbl.configure(text="---")
        self.in_stock_lbl.configure(text="In Stock: ---")
        self.prod_qty_entry.delete(0, "end")
        self.prod_qty_entry.insert(0, "1")
        self.calc_value = ""
        self.calc_display.configure(text="0")
        for sel in self.product_tree.selection():
            self.product_tree.selection_remove(sel)

    def _clear_cart(self):
        if messagebox.askyesno("Clear Cart", "Remove all items from the cart?"):
            self.cart.clear()
            self._refresh_cart()

    def _print_bill(self):
        if not self.cart:
            messagebox.showinfo("Empty Cart", "No items in the cart to print.")
            return
        name     = self.cust_name.get() or "Walk-in Customer"
        contact  = self.cust_contact.get() or "---"
        bill     = sum(c["total"] for c in self.cart)
        discount = round(bill * 0.05)
        net      = bill - discount
        lines = [
            "=" * 40,
            "      INVENTORY MANAGEMENT SYSTEM",
            "=" * 40,
            f"Customer : {name}",
            f"Contact  : {contact}",
            f"Date     : {datetime.datetime.now().strftime('%d-%m-%Y  %H:%M')}",
            "-" * 40,
            f"{'Product':<18} {'QTY':>4} {'Price':>8} {'Total':>8}",
            "-" * 40,
        ]
        for c in self.cart:
            lines.append(
                f"{c['name'][:18]:<18} {c['qty']:>4} {c['price']:>8,.0f} {c['total']:>8,.0f}"
            )
        lines += [
            "-" * 40,
            f"{'Bill Amount':<28} Rs {bill:>8,.0f}",
            f"{'Discount (5%)':<28} Rs {discount:>8,.0f}",
            f"{'Net Pay':<28} Rs {net:>8,.0f}",
            "=" * 40,
            "        Thank you for shopping!",
            "=" * 40,
        ]
        messagebox.showinfo("Print Preview", "\n".join(lines))

    def _save_bill(self):
        if not self.cart:
            messagebox.showinfo("Empty Cart", "No items to save.")
            return

        name    = self.cust_name.get() or "Walk-in Customer"
        contact = self.cust_contact.get() or "---"

        sale_id = save_sale(name, contact, self.cart)

        bill     = sum(c["total"] for c in self.cart)
        discount = round(bill * 0.05)
        net      = bill - discount

        messagebox.showinfo(
            "Bill Saved ✔",
            f"Bill #{sale_id} for '{name}' saved!\n"
            f"Net Payable: Rs {net:,.0f}\n"
            f"Stock has been updated automatically."
        )

        self.cart.clear()
        self._refresh_cart()
        self._refresh_products()
        self.cust_name.delete(0, "end")
        self.cust_contact.delete(0, "end")


if __name__ == "__main__":
    from Database import setup_db
    setup_db()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.geometry("1280x700")
    root.title("IMS — Sales & Billing Preview")
    root.configure(fg_color=COLORS["bg_main"])

    content = ctk.CTkFrame(root, fg_color=COLORS["bg_main"])
    content.pack(fill="both", expand=True, padx=15, pady=15)

    SalesBillingClass(content)
    root.mainloop()