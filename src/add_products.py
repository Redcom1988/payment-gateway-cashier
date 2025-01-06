from tkinter import *
from tkinter import ttk, messagebox, font, PhotoImage
from time import strftime
import sqlite3

class add_product:
    def __init__(self, top=None):
        self.window = top
        self.window.geometry("1366x768")
        self.window.resizable(0, 0)
        self.window.title("Add to Inventory")

        # Background
        self.label1 = Label(self.window)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/add_products.png")
        self.label1.configure(image=self.img)

        # Clock
        self.clock = Label(self.window)
        self.clock.place(relx=0.84, rely=0.065, width=102, height=36)
        self.clock.configure(
            font="-family {Poppins Light} -size 12",
            foreground="#000000",
            background="#ffffff"
        )
        self.time()

        # Create Treeview for Products
        self.create_products_treeview()

        # Stock Entry
        self.stock_label = Label(
            self.window,
            text="Stock Quantity:",
            font="-family {Poppins} -size 12",
            background="#ffffff"
        )
        self.stock_label.place(relx=0.132, rely=0.65)

        self.r2 = self.window.register(self.testint)
        self.stock_entry = Entry(self.window)
        self.stock_entry.place(relx=0.132, rely=0.7, width=374, height=30)
        self.stock_entry.configure(
            font="-family {Poppins} -size 12",
            relief="flat",
            validate="key",
            validatecommand=(self.r2, "%P")
        )

        # Selling Price Entry
        self.price_label = Label(
            self.window,
            text="Selling Price:",
            font="-family {Poppins} -size 12",
            background="#ffffff"
        )
        self.price_label.place(relx=0.527, rely=0.65)

        self.price_entry = Entry(self.window)
        self.price_entry.place(relx=0.527, rely=0.7, width=374, height=30)
        self.price_entry.configure(
            font="-family {Poppins} -size 12",
            relief="flat"
        )

        # Add to Inventory Button
        self.add_btn = Button(
            self.window,
            text="Add",
            command=self.add,
            relief="flat",
            overrelief="flat",
            activebackground="#CF1E14",
            cursor="hand2",
            foreground="#ffffff",
            background="#CF1E14",
            font="-family {Poppins SemiBold} -size 14",
            borderwidth="0"
        )
        self.add_btn.place(relx=0.475, rely=0.84, width=40, height=30)

        # Selected product
        self.selected_product = None

        # Load products
        self.load_products()

    def create_products_treeview(self):
        """Create and configure treeview for products"""
        # Frame for Treeview
        self.tree_frame = Frame(self.window)
        self.tree_frame.place(relx=0.132, rely=0.2, relwidth=0.7, relheight=0.4)

        # Scrollbars
        self.scrollbarx = Scrollbar(self.tree_frame, orient=HORIZONTAL)
        self.scrollbary = Scrollbar(self.tree_frame, orient=VERTICAL)

        # Treeview
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Configure scrollbars
        self.scrollbary.config(command=self.tree.yview)
        self.scrollbarx.config(command=self.tree.xview)
        self.scrollbary.pack(side=RIGHT, fill=Y)
        self.scrollbarx.pack(side=BOTTOM, fill=X)

        self.tree.configure(
            yscrollcommand=self.scrollbary.set,
            xscrollcommand=self.scrollbarx.set,
            selectmode="browse"
        )

        # Configure columns
        self.tree["columns"] = (
            "Product ID",
            "Name",
            "Category",
            "Sub-Category",
            "Cost Price",
            "Vendor Stock",
            "Vendor"
        )

        # Column headings
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, anchor=W)

        # Column widths
        self.tree.column("#0", width=0, stretch=NO)
        widths = [80, 200, 120, 120, 100, 100, 120]  # Adjusted widths
        for i, width in enumerate(widths):
            self.tree.column(self.tree["columns"][i], width=width, stretch=NO)

        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def load_products(self):
        """Load products from database"""
        try:
            with sqlite3.connect("./Database/store.db") as db:
                cur = db.cursor()
                query = """
                SELECT 
                    product_id,
                    product_name,
                    product_cat,
                    product_subcat,
                    cost_price,
                    vendor_stock,
                    vendor
                FROM products 
                ORDER BY product_id
                """
                cur.execute(query)
                rows = cur.fetchall()

                for row in rows:
                    self.tree.insert("", END, values=row)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading products: {str(e)}", 
                               parent=self.window)

    def on_select(self, event):
        """Handle product selection"""
        selected_items = self.tree.selection()
        if selected_items:
            self.selected_product = self.tree.item(selected_items[0])["values"]

    def add(self):
        """Add selected product to inventory"""
        if not self.selected_product:
            messagebox.showerror("Error", "Please select a product.", parent=self.window)
            return

        stock = self.stock_entry.get()
        sell_price = self.price_entry.get()

        if not stock:
            messagebox.showerror("Error", "Please enter stock quantity.", parent=self.window)
            return

        if not sell_price:
            messagebox.showerror("Error", "Please enter selling price.", parent=self.window)
            return

        try:
            stock = int(stock)
            sell_price = float(sell_price)

            if stock <= 0:
                messagebox.showerror("Error", "Stock must be greater than 0.", parent=self.window)
                return

            if sell_price <= 0:
                messagebox.showerror("Error", "Selling price must be greater than 0.", 
                                   parent=self.window)
                return

            with sqlite3.connect("./Database/store.db") as db:
                cur = db.cursor()
                cur.execute("""
                    INSERT INTO inventory (product_id, stock, sell_price) 
                    VALUES (?, ?, ?)
                """, (self.selected_product[0], stock, sell_price))
                db.commit()

            messagebox.showinfo("Success", "Product added to inventory successfully!", 
                              parent=self.window)
            self.window.destroy()

        except ValueError:
            messagebox.showerror("Error", "Invalid input for stock or selling price.", 
                               parent=self.window)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error adding to inventory: {str(e)}", 
                               parent=self.window)

    def testint(self, val):
        """Validate integer input"""
        if val.isdigit():
            return True
        elif val == "":
            return True
        return False

    def time(self):
        """Update clock"""
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)