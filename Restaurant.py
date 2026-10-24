import tkinter as tk
from tkinter import ttk, messagebox

# -------------------- Menu Data --------------------

MENU = {
    "Burgers": [
        {"name": "Classic Burger", "price": 120},
        {"name": "Cheese Burger", "price": 140},
        {"name": "Spicy Chicken", "price": 130},
        {"name": "Veggie Burger", "price": 110},
    ],
    "Pizza": [
        {"name": "Margherita", "price": 180},
        {"name": "Pepperoni", "price": 210},
        {"name": "BBQ Chicken", "price": 220},
        {"name": "Veggie Supreme", "price": 190},
    ],
    "Drinks": [
        {"name": "Cola (500ml)", "price": 40},
        {"name": "Fresh Lime", "price": 50},
        {"name": "Mango Shake", "price": 70},
        {"name": "Water", "price": 20},
    ],
    "Sides": [
        {"name": "French Fries", "price": 60},
        {"name": "Onion Rings", "price": 70},
        {"name": "Coleslaw", "price": 45},
        {"name": "Garlic Bread", "price": 55},
    ],
}

COLORS = {
    "bg": "#1a1a2e",
    "panel": "#16213e",
    "card": "#0f3460",
    "accent": "#e94560",
    "accent2": "#f5a623",
    "text": "#eaeaea",
    "subtext": "#a0a0b0",
    "success": "#4caf50",
    "white": "#ffffff",
}


# -------------------- Main Application --------------------

class FoodOrderApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Quick Bites — Food Order")
        self.geometry("950x660")
        self.resizable(False, False)
        self.configure(bg=COLORS["bg"])

        self.cart = {}
        self.customer_name = tk.StringVar()
        self.payment_method = tk.StringVar(value="Cash")

        self._build_header()
        self._build_body()
        self._build_footer()
        self._refresh_cart()

    # -------------------- Header --------------------

    def _build_header(self):
        header = tk.Frame(self, bg=COLORS["accent"], height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="  Quick Bites",
            font=("Georgia", 22, "bold"),
            bg=COLORS["accent"],
            fg=COLORS["white"],
        ).pack(side="left", padx=20)

        tk.Label(
            header,
            text="Fast • Fresh • Delicious",
            font=("Georgia", 11, "italic"),
            bg=COLORS["accent"],
            fg="#ffe0e0",
        ).pack(side="left")

    # -------------------- Main Body --------------------

    def _build_body(self):
        body = tk.Frame(self, bg=COLORS["bg"])
        body.pack(fill="both", expand=True, padx=16, pady=10)

        self._build_menu_panel(body)
        self._build_cart_panel(body)

    # -------------------- Menu Panel --------------------

    def _build_menu_panel(self, parent):
        left = tk.Frame(parent, bg=COLORS["bg"])
        left.pack(side="left", fill="both", expand=True)

        tk.Label(
            left,
            text="  Menu",
            font=("Georgia", 14, "bold"),
            bg=COLORS["bg"],
            fg=COLORS["accent2"],
        ).pack(anchor="w", pady=(0, 6))

        canvas = tk.Canvas(
            left,
            bg=COLORS["bg"],
            highlightthickness=0,
        )
        scrollbar = ttk.Scrollbar(
            left,
            orient="vertical",
            command=canvas.yview,
        )
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg=COLORS["bg"])
        window_id = canvas.create_window(
            (0, 0),
            window=inner,
            anchor="nw",
        )

        def update_scroll_region(_event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        inner.bind("<Configure>", update_scroll_region)
        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfigure(
                window_id, width=event.width
            ),
        )
        canvas.bind_all(
            "<MouseWheel>",
            lambda event: canvas.yview_scroll(
                -1 * (event.delta // 120), "units"
            ),
        )

        for category, items in MENU.items():
            category_frame = tk.Frame(
                inner,
                bg=COLORS["card"],
                pady=4,
            )
            category_frame.pack(fill="x", pady=(8, 2))

            tk.Label(
                category_frame,
                text=f"  {category}",
                font=("Georgia", 12, "bold"),
                bg=COLORS["card"],
                fg=COLORS["accent2"],
            ).pack(anchor="w", padx=8)

            for item in items:
                self._menu_row(inner, item)

    def _menu_row(self, parent, item):
        row = tk.Frame(
            parent,
            bg=COLORS["panel"],
            pady=6,
        )
        row.pack(fill="x", padx=2, pady=1)

        tk.Label(
            row,
            text=item["name"],
            font=("Helvetica", 11),
            bg=COLORS["panel"],
            fg=COLORS["text"],
            width=22,
            anchor="w",
        ).pack(side="left", padx=10)

        tk.Label(
            row,
            text=f"₹{item['price']}",
            font=("Helvetica", 11, "bold"),
            bg=COLORS["panel"],
            fg=COLORS["accent2"],
        ).pack(side="left", padx=6)

        tk.Button(
            row,
            text="+ Add",
            font=("Helvetica", 10, "bold"),
            bg=COLORS["accent"],
            fg=COLORS["white"],
            relief="flat",
            padx=10,
            cursor="hand2",
            command=lambda selected_item=item: self._add_to_cart(
                selected_item
            ),
        ).pack(side="right", padx=10, pady=2)

    # -------------------- Cart Panel --------------------

    def _build_cart_panel(self, parent):
        right = tk.Frame(
            parent,
            bg=COLORS["panel"],
            width=300,
        )
        right.pack(side="right", fill="y", padx=(12, 0))
        right.pack_propagate(False)

        tk.Label(
            right,
            text="  Your Cart",
            font=("Georgia", 14, "bold"),
            bg=COLORS["panel"],
            fg=COLORS["accent2"],
        ).pack(anchor="w", padx=12, pady=(10, 4))

        self.cart_frame = tk.Frame(
            right,
            bg=COLORS["panel"],
        )
        self.cart_frame.pack(
            fill="both",
            expand=True,
            padx=8,
        )

        tk.Frame(
            right,
            bg=COLORS["card"],
            height=2,
        ).pack(fill="x", padx=8, pady=4)

        self.total_label = tk.Label(
            right,
            text="Total: ₹0",
            font=("Georgia", 13, "bold"),
            bg=COLORS["panel"],
            fg=COLORS["accent"],
        )
        self.total_label.pack(anchor="e", padx=16, pady=2)

        tk.Label(
            right,
            text="Your Name:",
            font=("Helvetica", 10),
            bg=COLORS["panel"],
            fg=COLORS["subtext"],
        ).pack(anchor="w", padx=12)

        tk.Entry(
            right,
            textvariable=self.customer_name,
            font=("Helvetica", 11),
            bg=COLORS["card"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="flat",
            bd=4,
        ).pack(fill="x", padx=12, pady=(0, 6))

        tk.Label(
            right,
            text="Payment:",
            font=("Helvetica", 10),
            bg=COLORS["panel"],
            fg=COLORS["subtext"],
        ).pack(anchor="w", padx=12)

        payment_frame = tk.Frame(
            right,
            bg=COLORS["panel"],
        )
        payment_frame.pack(fill="x", padx=12, pady=(0, 8))

        for method in ("Cash", "Card", "UPI"):
            tk.Radiobutton(
                payment_frame,
                text=method,
                variable=self.payment_method,
                value=method,
                font=("Helvetica", 10),
                bg=COLORS["panel"],
                fg=COLORS["text"],
                selectcolor=COLORS["accent"],
                activebackground=COLORS["panel"],
                activeforeground=COLORS["white"],
            ).pack(side="left", padx=4)

        tk.Button(
            right,
            text="Place Order",
            font=("Georgia", 13, "bold"),
            bg=COLORS["success"],
            fg=COLORS["white"],
            relief="flat",
            pady=10,
            cursor="hand2",
            command=self._place_order,
        ).pack(fill="x", padx=12, pady=(0, 6))

        tk.Button(
            right,
            text="Clear Cart",
            font=("Helvetica", 10),
            bg=COLORS["card"],
            fg=COLORS["subtext"],
            relief="flat",
            pady=6,
            cursor="hand2",
            command=self._clear_cart,
        ).pack(fill="x", padx=12, pady=(0, 10))

    # -------------------- Footer --------------------

    def _build_footer(self):
        footer = tk.Frame(
            self,
            bg=COLORS["card"],
            height=28,
        )
        footer.pack(fill="x")

        tk.Label(
            footer,
            text="© 2024 Quick Bites | Simple Food Ordering",
            font=("Helvetica", 9),
            bg=COLORS["card"],
            fg=COLORS["subtext"],
        ).pack(pady=4)

    # -------------------- Cart Logic --------------------

    def _add_to_cart(self, item):
        name = item["name"]
        price = item["price"]

        if name in self.cart:
            self.cart[name]["qty"] += 1
        else:
            self.cart[name] = {
                "price": price,
                "qty": 1,
            }

        self._refresh_cart()

    def _remove_item(self, name):
        if name not in self.cart:
            return

        if self.cart[name]["qty"] > 1:
            self.cart[name]["qty"] -= 1
        else:
            del self.cart[name]

        self._refresh_cart()

    def _clear_cart(self):
        self.cart.clear()
        self._refresh_cart()

    def _refresh_cart(self):
        for widget in self.cart_frame.winfo_children():
            widget.destroy()

        if not self.cart:
            tk.Label(
                self.cart_frame,
                text="Cart is empty",
                font=("Helvetica", 10, "italic"),
                bg=COLORS["panel"],
                fg=COLORS["subtext"],
            ).pack(pady=20)

            self.total_label.config(text="Total: ₹0")
            return

        total = 0

        for name, info in self.cart.items():
            subtotal = info["price"] * info["qty"]
            total += subtotal

            row = tk.Frame(
                self.cart_frame,
                bg=COLORS["card"],
                pady=4,
            )
            row.pack(fill="x", pady=1)

            tk.Label(
                row,
                text=name,
                font=("Helvetica", 9),
                bg=COLORS["card"],
                fg=COLORS["text"],
                anchor="w",
                wraplength=110,
            ).grid(row=0, column=0, sticky="w", padx=4)

            tk.Label(
                row,
                text=f"₹{info['price']} × {info['qty']}",
                font=("Helvetica", 9),
                bg=COLORS["card"],
                fg=COLORS["subtext"],
            ).grid(row=0, column=1, padx=3)

            tk.Label(
                row,
                text=f"₹{subtotal}",
                font=("Helvetica", 9, "bold"),
                bg=COLORS["card"],
                fg=COLORS["accent2"],
            ).grid(row=0, column=2, padx=3)

            tk.Button(
                row,
                text="−",
                font=("Helvetica", 9, "bold"),
                bg=COLORS["accent"],
                fg=COLORS["white"],
                relief="flat",
                padx=4,
                cursor="hand2",
                command=lambda item_name=name: self._remove_item(
                    item_name
                ),
            ).grid(row=0, column=3, padx=4)

        self.total_label.config(text=f"Total: ₹{total}")

    # -------------------- Order Processing --------------------

    def _place_order(self):
        if not self.cart:
            messagebox.showwarning(
                "Empty Cart",
                "Please add items to your cart first!",
            )
            return

        name = self.customer_name.get().strip()

        if not name:
            messagebox.showwarning(
                "Name Required",
                "Please enter your name to place the order.",
            )
            return

        total = sum(
            item["price"] * item["qty"]
            for item in self.cart.values()
        )
        payment = self.payment_method.get()

        receipt_lines = [
            "  Quick Bites — Order Receipt",
            "=" * 38,
            f"Customer : {name}",
            f"Payment  : {payment}",
            "-" * 38,
        ]

        for item_name, info in self.cart.items():
            amount = info["price"] * info["qty"]
            receipt_lines.append(
                f"  {item_name:<22} x{info['qty']}  ₹{amount}"
            )

        receipt_lines.extend([
            "-" * 38,
            f"  {'TOTAL':<26} ₹{total}",
            "=" * 38,
            "Thank you! Your order is being prepared.",
        ])
        receipt = "\n".join(receipt_lines)

        popup = tk.Toplevel(self)
        popup.title("Order Confirmed!")
        popup.geometry("420x400")
        popup.configure(bg=COLORS["bg"])
        popup.transient(self)
        popup.grab_set()

        tk.Label(
            popup,
            text="Order Placed!",
            font=("Georgia", 16, "bold"),
            bg=COLORS["bg"],
            fg=COLORS["success"],
        ).pack(pady=10)

        receipt_text = tk.Text(
            popup,
            font=("Courier", 10),
            bg=COLORS["panel"],
            fg=COLORS["text"],
            relief="flat",
            padx=10,
            pady=8,
        )
        receipt_text.pack(
            fill="both",
            expand=True,
            padx=16,
            pady=4,
        )
        receipt_text.insert("1.0", receipt)
        receipt_text.config(state="disabled")

        tk.Button(
            popup,
            text="Close",
            font=("Helvetica", 11, "bold"),
            bg=COLORS["accent"],
            fg=COLORS["white"],
            relief="flat",
            padx=20,
            pady=6,
            cursor="hand2",
            command=popup.destroy,
        ).pack(pady=8)

        self._clear_cart()
        self.customer_name.set("")


# -------------------- Run Application --------------------

if __name__ == "__main__":
    app = FoodOrderApp()
    app.mainloop()
