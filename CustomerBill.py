import customtkinter as ctk
from tkinter import ttk, messagebox
from Database import get_all_sales, get_sale_items, delete_sale

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


class CustomerBillClass:
    def __init__(self, parent):
        self.parent = parent
        self.selected_sid = None
        self.build_ui()

    def build_ui(self):

        # ── Page title ──────────────────────────────────────────
        title_bar = ctk.CTkFrame(self.parent, fg_color=COLORS["header"], corner_radius=10)
        title_bar.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(title_bar, text="🧾 Customer Bill Viewer",
                     font=("Arial", 18, "bold"),
                     text_color=COLORS["card3"]).pack(side="left", padx=15, pady=8)

        self.count_label = ctk.CTkLabel(title_bar,
                                        text="Total Bills: 0",
                                        font=("Arial", 12),
                                        text_color=COLORS["text_dim"])
        self.count_label.pack(side="right", padx=20)

        # ── Action bar ──────────────────────────────────────────
        action_bar = ctk.CTkFrame(self.parent, fg_color=COLORS["sub_header"], corner_radius=10)
        action_bar.pack(fill="x", padx=10, pady=(0, 10))

        btn_cfg = {"height": 34, "corner_radius": 8,
                   "font": ("Arial", 12, "bold"), "width": 140}

        ctk.CTkButton(action_bar, text="🔄 Refresh",
                      fg_color=COLORS["btn_primary"],
                      hover_color=COLORS["sidebar_hover"],
                      text_color=COLORS["text"],
                      command=self.refresh,
                      **btn_cfg).pack(side="left", padx=10, pady=8)

        ctk.CTkButton(action_bar, text="🗑 Delete Bill",
                      fg_color=COLORS["btn_danger"],
                      hover_color="#e03058",
                      text_color=COLORS["text"],
                      command=self.delete_bill,
                      **btn_cfg).pack(side="left", padx=5, pady=8)

        # ── Main area — left table + right detail ────────────────
        main = ctk.CTkFrame(self.parent, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        main.grid_columnconfigure(0, weight=2)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        # Left — bills table
        table_card = ctk.CTkFrame(main, fg_color=COLORS["sidebar"], corner_radius=12)
        table_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        ctk.CTkLabel(table_card, text="All Bills",
                     font=("Arial", 13, "bold"),
                     text_color=COLORS["card2"]).pack(anchor="w", padx=15, pady=(10, 4))

        self.build_table(table_card)

        # Right — detail panel
        detail_card = ctk.CTkFrame(main, fg_color=COLORS["header"], corner_radius=12)
        detail_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        self.build_details(detail_card)

        self.refresh()

    # ── Bills table ─────────────────────────────────────────────
    def build_table(self, parent):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Bills.Treeview",
                        background=COLORS["header"],
                        foreground=COLORS["text"],
                        fieldbackground=COLORS["header"],
                        rowheight=30,
                        font=("Arial", 10))
        style.configure("Bills.Treeview.Heading",
                        background=COLORS["sub_header"],
                        foreground=COLORS["card3"],
                        font=("Arial", 10, "bold"),
                        relief="flat")
        style.map("Bills.Treeview",
                  background=[("selected", COLORS["sidebar_hover"])],
                  foreground=[("selected", COLORS["text"])])

        cols = ("ID", "Customer", "Contact", "Date", "Total", "Discount", "Net")
        col_widths = {"ID": 45, "Customer": 120, "Contact": 100,
                      "Date": 120, "Total": 80, "Discount": 75, "Net": 80}

        scroll_y = ctk.CTkScrollbar(parent)
        scroll_y.pack(side="right", fill="y", pady=8)

        self.tree = ttk.Treeview(parent, columns=cols, show="headings",
                                 style="Bills.Treeview",
                                 yscrollcommand=scroll_y.set)
        scroll_y.configure(command=self.tree.yview)

        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=col_widths[col], anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.tree.bind("<<TreeviewSelect>>", self.show_details)

    # ── Detail panel ────────────────────────────────────────────
    def build_details(self, parent):
        ctk.CTkLabel(parent, text="Invoice Details",
                     font=("Arial", 15, "bold"),
                     text_color=COLORS["card3"]).pack(pady=(15, 8))

        # Info card
        info_card = ctk.CTkFrame(parent, fg_color=COLORS["sidebar"], corner_radius=10)
        info_card.pack(fill="x", padx=12, pady=(0, 8))

        self.id_label       = ctk.CTkLabel(info_card, text="Bill ID:  ---",
                                           font=("Arial", 12), text_color=COLORS["text"])
        self.id_label.pack(anchor="w", padx=15, pady=4)

        self.customer_label = ctk.CTkLabel(info_card, text="Customer: ---",
                                           font=("Arial", 12), text_color=COLORS["text"])
        self.customer_label.pack(anchor="w", padx=15, pady=4)

        self.contact_label  = ctk.CTkLabel(info_card, text="Contact:  ---",
                                           font=("Arial", 12), text_color=COLORS["text"])
        self.contact_label.pack(anchor="w", padx=15, pady=4)

        self.date_label     = ctk.CTkLabel(info_card, text="Date:     ---",
                                           font=("Arial", 12), text_color=COLORS["text"])
        self.date_label.pack(anchor="w", padx=15, pady=(4, 10))

        # Totals card
        totals_card = ctk.CTkFrame(parent, fg_color=COLORS["sub_header"], corner_radius=10)
        totals_card.pack(fill="x", padx=12, pady=(0, 8))

        self.total_label = ctk.CTkLabel(totals_card, text="Bill:     Rs 0",
                                        font=("Arial", 12, "bold"),
                                        text_color=COLORS["text"])
        self.total_label.pack(anchor="w", padx=15, pady=4)

        self.disc_label  = ctk.CTkLabel(totals_card, text="Discount: Rs 0",
                                        font=("Arial", 12),
                                        text_color=COLORS["card2"])
        self.disc_label.pack(anchor="w", padx=15, pady=4)

        self.net_label   = ctk.CTkLabel(totals_card, text="Net:      Rs 0",
                                        font=("Arial", 14, "bold"),
                                        text_color=COLORS["card3"])
        self.net_label.pack(anchor="w", padx=15, pady=(4, 10))

        # Items sub-table
        ctk.CTkLabel(parent, text="Items in this Bill",
                     font=("Arial", 12, "bold"),
                     text_color=COLORS["card2"]).pack(pady=(4, 4))

        items_card = ctk.CTkFrame(parent, fg_color=COLORS["sidebar"], corner_radius=10)
        items_card.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        style = ttk.Style()
        style.configure("Items.Treeview",
                        background=COLORS["bg_main"],
                        foreground=COLORS["text"],
                        fieldbackground=COLORS["bg_main"],
                        rowheight=26,
                        font=("Consolas", 9))
        style.configure("Items.Treeview.Heading",
                        background=COLORS["sub_header"],
                        foreground=COLORS["card3"],
                        font=("Arial", 9, "bold"),
                        relief="flat")
        style.map("Items.Treeview",
                  background=[("selected", COLORS["sidebar_hover"])],
                  foreground=[("selected", COLORS["text"])])

        self.items_tree = ttk.Treeview(items_card, style="Items.Treeview",
                                       columns=("Product", "QTY", "Price", "Total"),
                                       show="headings")
        for col, w in [("Product", 110), ("QTY", 40), ("Price", 70), ("Total", 70)]:
            self.items_tree.heading(col, text=col)
            self.items_tree.column(col, width=w, anchor="center")

        self.items_tree.pack(fill="both", expand=True, padx=8, pady=8)

    # ── Data ────────────────────────────────────────────────────
    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        self.selected_sid = None
        self._reset_details()

        rows = get_all_sales()
        for r in rows:
            self.tree.insert("", "end", values=(
                r[0], r[1], r[2], r[3],
                f"Rs {r[4]:,.0f}",
                f"Rs {r[5]:,.0f}",
                f"Rs {r[6]:,.0f}"
            ))
        self.count_label.configure(text=f"Total Bills: {len(rows)}")

    def show_details(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0])["values"]
        sid, customer, contact, date, total, discount, net = values
        self.selected_sid = sid

        self.id_label.configure(text=f"Bill ID:  #{sid}")
        self.customer_label.configure(text=f"Customer: {customer}")
        self.contact_label.configure(text=f"Contact:  {contact}")
        self.date_label.configure(text=f"Date:     {date}")
        self.total_label.configure(text=f"Bill:     {total}")
        self.disc_label.configure(text=f"Discount: {discount}")
        self.net_label.configure(text=f"Net:      {net}")

        self.items_tree.delete(*self.items_tree.get_children())
        for item in get_sale_items(sid):
            self.items_tree.insert("", "end", values=(
                item[3], item[4],
                f"Rs {item[5]:,.0f}",
                f"Rs {item[6]:,.0f}"
            ))

    def delete_bill(self):
        if not self.selected_sid:
            messagebox.showerror("Error", "Select a bill to delete")
            return
        if messagebox.askyesno("Confirm Delete",
                               f"Delete Bill #{self.selected_sid}?\n\n"
                               f"Stock will be restored automatically."):
            delete_sale(self.selected_sid)
            self.refresh()
            messagebox.showinfo("Deleted", f"Bill #{self.selected_sid} deleted and stock restored.")

    def _reset_details(self):
        self.id_label.configure(text="Bill ID:  ---")
        self.customer_label.configure(text="Customer: ---")
        self.contact_label.configure(text="Contact:  ---")
        self.date_label.configure(text="Date:     ---")
        self.total_label.configure(text="Bill:     Rs 0")
        self.disc_label.configure(text="Discount: Rs 0")
        self.net_label.configure(text="Net:      Rs 0")
        self.items_tree.delete(*self.items_tree.get_children())