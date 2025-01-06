import sqlite3
from time import strftime
from tkinter import END, LEFT, Button, Entry, Label, PhotoImage, messagebox


class Update_Product:
    def __init__(self, top=None, selected_product=None):
        self.window = top
        self.window.geometry("1366x768")
        self.window.resizable(0, 0)
        self.window.title("Update Product")
        self.selected_product = selected_product

        # Background
        self.label1 = Label(self.window)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/update_product.png")
        self.label1.configure(image=self.img)

        # Create read-only fields
        self.create_readonly_fields()

        # Create editable fields
        self.create_editable_fields()

        # Create buttons
        self.create_buttons()

    def create_readonly_fields(self):
        """Create read-only information fields"""
        # Position name value under "Product Name" label - shifted down and left
        name_label = Label(
            self.window,
            text=str(self.selected_product[1]),
            font="-family {Poppins} -size 12",
            background="#ffffff",
            anchor="w"
        )
        name_label.place(relx=0.13, rely=0.3, height=25)  # Adjusted from 0.2, 0.25

        # Position category value under "Category" label
        category_label = Label(
            self.window,
            text=str(self.selected_product[2]),
            font="-family {Poppins} -size 12",
            background="#ffffff",
            anchor="w"
        )
        category_label.place(relx=0.13, rely=0.42, height=25)  # Adjusted from 0.2, 0.37

        # Position sub-category value under "Sub Category" label
        subcategory_label = Label(
            self.window,
            text=str(self.selected_product[3]),
            font="-family {Poppins} -size 12",
            background="#ffffff",
            anchor="w"
        )
        subcategory_label.place(relx=0.53, rely=0.42, height=25)  # Adjusted from 0.6, 0.37

        # Position cost price value under "Cost Price" label
        cost_label = Label(
            self.window,
            text=str(self.selected_product[6]),
            font="-family {Poppins} -size 12",
            background="#ffffff",
            anchor="w"
        )
        cost_label.place(relx=0.53, rely=0.53, height=25)  # Adjusted from 0.6, 0.49

        # Position vendor value under "Vendor" label
        vendor_label = Label(
            self.window,
            text=str(self.selected_product[7]),
            font="-family {Poppins} -size 12",
            background="#ffffff",
            anchor="w"
        )
        vendor_label.place(relx=0.53, rely=0.65, height=25)  # Adjusted from 0.6, 0.61

    def create_editable_fields(self):
        """Create editable fields for stock and price"""
        self.r2 = self.window.register(self.testint)
        
        # Stock Entry under "Quantity" label
        self.stock_entry = Entry(self.window)
        self.stock_entry.place(relx=0.13, rely=0.53, width=100, height=30)  # Adjusted from 0.2, 0.49
        self.stock_entry.configure(
            font="-family {Poppins} -size 12",
            relief="flat",
            validate="key",
            validatecommand=(self.r2, "%P")
        )

        # Selling Price Entry under "Selling Price" label
        self.price_entry = Entry(self.window)
        self.price_entry.place(relx=0.13, rely=0.65, width=100, height=30)  # Adjusted from 0.2, 0.61
        self.price_entry.configure(
            font="-family {Poppins} -size 12",
            relief="flat"
        )

        # Fill editable fields with current values if product is selected
        if self.selected_product:
            self.stock_entry.insert(0, str(self.selected_product[4]))
            self.price_entry.insert(0, str(self.selected_product[5]))

    def create_buttons(self):
        # Update Button
        self.button1 = Button(
            self.window,
            text="UPDATE",
            command=self.update,
            relief="flat",
            overrelief="flat",
            activebackground="#CF1E14",
            cursor="hand2",
            foreground="#ffffff",
            background="#CF1E14",
            font="-family {Poppins SemiBold} -size 14",
            borderwidth="0"
        )
        self.button1.place(relx=0.408, rely=0.836, width=96, height=34)

        # Cancel Button
        self.button2 = Button(
            self.window,
            text="CANCEL",
            command=self.window.destroy,
            relief="flat",
            overrelief="flat",
            activebackground="#CF1E14",
            cursor="hand2",
            foreground="#ffffff",
            background="#CF1E14",
            font="-family {Poppins SemiBold} -size 14",
            borderwidth="0"
        )
        self.button2.place(relx=0.526, rely=0.836, width=86, height=34)

    def update(self):
        """Update product in database"""
        try:
            # Get values from entries
            stock = self.stock_entry.get().strip()
            selling_price = self.price_entry.get().strip()

            # Validation
            if not all([stock, selling_price]):
                messagebox.showerror("Error", "Both stock and selling price are required.", 
                                   parent=self.window)
                return

            try:
                stock = int(stock)
                selling_price = float(selling_price)

                if stock < 0:
                    messagebox.showerror("Error", "Stock cannot be negative.", 
                                       parent=self.window)
                    return
                if selling_price <= 0:
                    messagebox.showerror("Error", "Selling price must be greater than 0.", 
                                       parent=self.window)
                    return

            except ValueError:
                messagebox.showerror("Error", "Invalid numeric values.", 
                                   parent=self.window)
                return

            # Update database
            with sqlite3.connect("./Database/store.db") as db:
                cur = db.cursor()
                
                # Update inventory table only
                cur.execute("""
                    UPDATE inventory 
                    SET stock=?, sell_price=?
                    WHERE product_id=?
                """, (stock, selling_price, self.selected_product[0]))

                db.commit()

            messagebox.showinfo("Success", "Product updated successfully!", 
                              parent=self.window)
            self.window.destroy()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", 
                               f"Error updating product: {str(e)}", 
                               parent=self.window)

    def testint(self, val):
        """Validate integer input"""
        if val.isdigit():
            return True
        elif val == "":
            return True
        return False