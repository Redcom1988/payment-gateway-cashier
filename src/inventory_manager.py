import os
from time import strftime
from tkinter import *
from tkinter import ttk, messagebox, font, PhotoImage
from datetime import datetime 
import sqlite3

class InventoryManager:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_fonts()
        self.setup_gui()
        self.sel = []  # Selected items list

    def setup_window(self):
        """Initialize main window properties"""
        self.root.geometry("1366x768")
        self.root.resizable(0, 0)
        self.root.title(f"Inventory Management")
        # Add keyboard shortcut for refresh (F5)
        self.root.bind('<F5>', lambda event: self.refresh_data())

    def create_fonts(self):
        """Initialize fonts"""
        font_folder = "./fonts"

        self.poppins_regular = font.Font(
            family="Poppins",
            size=12,
            weight="normal"
        )
        
        self.poppins_semibold = font.Font(
            family="Poppins",
            size=12,
            weight="bold"
        )

        self.poppins_small = font.Font(
            family="Poppins",
            size=10,
            weight="normal"
        )
        
        # Only try to load fonts if the folder exists
        if os.path.exists(font_folder):
            for font_file in os.listdir(font_folder):
                if font_file.endswith('.ttf'):
                    font_path = os.path.join(font_folder, font_file)
                    try:
                        font.Font(file=font_path)
                    except:
                        print(f"Could not load font: {font_file}")

    def setup_gui(self):
        """Setup all GUI elements"""
        self.setup_background()
        self.setup_header()
        self.setup_search()
        self.create_buttons()
        self.create_treeview()
        self.DisplayData()

    def setup_background(self):
        """Setup background image"""
        try:
            self.bg_image = PhotoImage(file="./images/inventory.png")
            self.bg_label = Label(self.root, image=self.bg_image)
            self.bg_label.place(x=0, y=0, width=1366, height=768)
        except:
            print("Could not load background image")
            self.bg_label = Label(self.root, bg="white")
            self.bg_label.place(x=0, y=0, width=1366, height=768)

    def setup_header(self):
        """Setup header section with admin label, user info, and clock"""
        # Admin Label
        self.header_label = Label(
            self.root,
            text=f"ADMIN",
            font=self.poppins_small,
            fg="#000000",
            bg="#ffffff",
            anchor="w"
        )
        self.header_label.place(x=63, y=43, width=200, height=30)

        # Clock
        self.clock = Label(
            self.root,
            font=("-family {Poppins Light} -size 12"),
            foreground="#000000",
            background="#ffffff"
        )
        self.clock.place(relx=0.75, rely=0.065, width=102, height=36)
        self.update_clock()

    def setup_search(self):
        """Setup search section"""
        self.search_var = StringVar()
        self.search_entry = Entry(
            self.root,
            textvariable=self.search_var,
            font=self.poppins_regular,
            relief="flat"
        )
        self.search_entry.place(relx=0.040, rely=0.286, width=240, height=28)
        
        # Bind Enter key to search
        self.search_entry.bind('<Return>', lambda event: self.search_product())

    def create_buttons(self):
        """Create all buttons"""
        # Add refresh button
        self.refresh_btn = Button(
            self.root,
            text="⟳ Refresh",
            font=self.poppins_regular,
            fg="#ffffff",
            bg="#CF1E14",
            relief="flat",
            overrelief="flat",
            activebackground="#CF1E14",
            cursor="hand2",
            borderwidth=0,
            command=self.refresh_data
        )
        self.refresh_btn.place(relx=0.85, rely=0.065, width=90, height=36)

        # Other buttons
        buttons = [
            ("Search", 0.229, 0.289, 76, 23, self.search_product),
            ("ADD PRODUCT", 0.052, 0.432, 306, 28, self.add_product),
            ("UPDATE PRODUCT", 0.052, 0.5, 306, 28, self.update_product),
            ("DELETE PRODUCT", 0.052, 0.57, 306, 28, self.delete_product),
            ("EXIT", 0.135, 0.885, 76, 23, self.Exit)
        ]

        for text, relx, rely, width, height, command in buttons:
            btn = Button(
                self.root,
                text=text,
                font=self.poppins_semibold,
                fg="#ffffff",
                bg="#CF1E14",
                relief="flat",
                overrelief="flat",
                activebackground="#CF1E14",
                cursor="hand2",
                borderwidth=0,
                command=command
            )
            btn.place(relx=relx, rely=rely, width=width, height=height)

    def create_treeview(self):
        """Create and configure treeview"""
        # Scrollbars
        self.scrollbarx = Scrollbar(self.root, orient=HORIZONTAL)
        self.scrollbary = Scrollbar(self.root, orient=VERTICAL)
        
        # Treeview
        self.tree = ttk.Treeview(self.root)
        self.tree.place(relx=0.307, rely=0.203, width=880, height=550)
        
        self.tree.configure(
            yscrollcommand=self.scrollbary.set,
            xscrollcommand=self.scrollbarx.set,
            selectmode="extended"
        )

        # Configure scrollbars
        self.scrollbary.configure(command=self.tree.yview)
        self.scrollbarx.configure(command=self.tree.xview)
        
        self.scrollbary.place(relx=0.954, rely=0.203, width=22, height=548)
        self.scrollbarx.place(relx=0.307, rely=0.924, width=884, height=22)

        # Configure columns
        columns = (
            "Product ID",
            "Name",
            "Category",
            "Sub-Category",
            "Stock",
            "Selling Price",
            "Cost Price",
            "Vendor"
        )
        
        self.tree.configure(columns=columns)

        # Column headings
        for col in columns:
            self.tree.heading(col, text=col, anchor=W)

        # Column widths
        self.tree.column("#0", stretch=NO, minwidth=0, width=0)
        column_widths = [80, 260, 100, 120, 80, 80, 80, 100]
        for i, width in enumerate(column_widths, 1):
            self.tree.column(f"#{i}", stretch=NO, minwidth=0, width=width)

        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def DisplayData(self):
        """Fetch and display data in treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        query = """
        SELECT 
            p.product_id,
            p.product_name,
            p.product_cat,
            p.product_subcat,
            i.stock,
            i.sell_price,
            p.cost_price,
            p.vendor
        FROM products p
        INNER JOIN inventory i ON p.product_id = i.product_id
        ORDER BY p.product_id
        """
            
        try:
            with sqlite3.connect("./Database/store.db") as db:
                cur = db.cursor()
                cur.execute(query)
                rows = cur.fetchall()
                
            for row in rows:
                self.tree.insert("", "end", values=row)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error fetching data: {str(e)}", 
                            parent=self.root)

    def refresh_data(self):
        """Refresh the inventory display"""
        try:
            self.refresh_btn.configure(text="⟳ Loading...", state="disabled")
            self.root.update()
            self.DisplayData()
            self.refresh_btn.configure(text="⟳ Refresh", state="normal")
            messagebox.showinfo("Success", "Data refreshed successfully!", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh data: {str(e)}", parent=self.root)
            self.refresh_btn.configure(text="⟳ Refresh", state="normal")

    def search_product(self):
            """Search for products"""
            search_term = self.search_var.get().strip()
            
            # If search term is empty, just refresh the table
            if not search_term:
                self.DisplayData()
                return

            query = """
            SELECT 
                p.product_id,
                p.product_name,
                p.product_cat,
                p.product_subcat,
                i.stock,
                i.sell_price,
                p.cost_price,
                p.vendor
            FROM products p
            INNER JOIN inventory i ON p.product_id = i.product_id
            WHERE p.product_id = ? OR p.product_name LIKE ? OR p.product_cat LIKE ?
            """

            try:
                with sqlite3.connect("./Database/store.db") as db:
                    cur = db.cursor()
                    search_pattern = f"%{search_term}%"
                    cur.execute(query, [
                        search_term if search_term.isdigit() else -1,
                        search_pattern,
                        search_pattern
                    ])
                    rows = cur.fetchall()

                    if rows:
                        # Clear treeview
                        for item in self.tree.get_children():
                            self.tree.delete(item)
                        # Display search results
                        for row in rows:
                            self.tree.insert("", "end", values=row)
                        messagebox.showinfo("Success", "Search results found.", parent=self.root)
                    else:
                        messagebox.showerror("Error", "No matching products found.", parent=self.root)
                        
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error searching products: {str(e)}", 
                                parent=self.root)

    def add_product(self):
        """Open add product window"""
        try:
            add_window = Toplevel(self.root)
            from add_products import add_product
            add_window_instance = add_product(add_window)
            add_window.protocol("WM_DELETE_WINDOW", 
                            lambda: self.handle_window_close(add_window))
        except Exception as e:
            messagebox.showerror("Error", f"Could not open add product window: {str(e)}", 
                            parent=self.root)

    def handle_add_window_close(self, window):
        """Handle add product window closing"""
        window.destroy()
        self.DisplayData()  # Refresh the inventory display

    def update_product(self):
        """Open update product window"""
        if len(self.sel) != 1:
            messagebox.showerror("Error", "Please select exactly one product to update.", 
                            parent=self.root)
            return

        try:
            update_window = Toplevel(self.root)
            selected_values = self.tree.item(self.sel[0])["values"]
            
            # Import and create Update_Product instance
            from update_products import Update_Product
            update_instance = Update_Product(update_window, selected_values)
            
            # Set protocol for window close
            update_window.protocol("WM_DELETE_WINDOW", 
                                lambda: self.handle_update_window_close(update_window))
                                
        except Exception as e:
            messagebox.showerror("Error", f"Could not open update window: {str(e)}", 
                            parent=self.root)

    def delete_product(self):
        """Delete selected product(s)"""
        if not self.sel:
            messagebox.showerror("Error", "Please select a product.", parent=self.root)
            return

        if messagebox.askyesno("Confirm", "Delete selected product(s)?", parent=self.root):
            try:
                with sqlite3.connect("./Database/store.db") as db:
                    cur = db.cursor()
                    for item in self.sel:
                        product_id = self.tree.item(item)["values"][0]
                        # Delete from inventory first due to foreign key constraint
                        cur.execute("DELETE FROM inventory WHERE product_id = ?", [product_id])
                        # Then delete from products
                        cur.execute("DELETE FROM products WHERE product_id = ?", [product_id])
                    db.commit()
                    
                messagebox.showinfo("Success", "Product(s) deleted successfully.", 
                                  parent=self.root)
                self.sel.clear()
                self.DisplayData()
                
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error deleting product(s): {str(e)}", 
                                   parent=self.root)

    def handle_window_close(self, window):
        """Handle child window closing"""
        window.destroy()
        self.DisplayData()

    def on_tree_select(self, event):
        """Handle treeview selection"""
        self.sel = self.tree.selection()

    def update_clock(self):
        """Update clock display"""
        time_string = strftime("%H:%M:%S %p")
        self.clock.config(text=time_string)
        self.clock.after(1000, self.update_clock)

    def Exit(self):
        """Handle exit button click"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=self.root):
            self.root.destroy()