#==================imports===================
import sqlite3
import string
import threading
import time
from datetime import datetime
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext as tkst
from tkinter import simpledialog
import requests
import hashlib
import json

from utils.dokuAPI import DokuOVOPayment
#============================================

class Item:
    def __init__(self, product_id, name, price, qty):
        self.product_id = product_id
        self.product_name = name
        self.price = price
        self.qty = qty

class Cart:
    def __init__(self):
        self.items = []
        self.dictionary = {}

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self):
        if self.items:
            self.items.pop()

    def remove_items(self):
        self.items.clear()
        self.dictionary.clear()

    def total(self):
        total = 0.0
        for i in self.items:
            total += i.price * i.qty
        return total

    def isEmpty(self):
        return len(self.items) == 0

    def allCart(self):
        self.dictionary.clear()
        for i in self.items:
            if i.product_id in self.dictionary:
                self.dictionary[i.product_id] += i.qty
            else:
                self.dictionary[i.product_id] = i.qty
        return self.dictionary

class bill_window:
    def __init__(self, top=None, employee_id=None):
        if employee_id is None:
            messagebox.showerror("Error", "No employee ID provided")
            top.destroy()
            return
            
        self.root = top
        self.employee_id = employee_id
        self.cart = Cart()
        self.state = 1  # For bill generation state tracking
        
        self.root.geometry("1366x768")
        self.root.resizable(0, 0)
        self.root.title("Retail Manager")

        self.label = Label(self.root)
        self.label.place(relx=0, rely=0, width=1366, height=768)
        try:
            self.img = PhotoImage(file="./images/bill_window.png")
            self.label.configure(image=self.img)
        except:
            self.label.configure(bg="white")

        # Employee info display
        self.message = Label(self.root)
        self.message.place(relx=0.038, rely=0.055, width=136, height=30)
        self.message.configure(font="-family {Poppins} -size 10")
        self.message.configure(foreground="#000000")
        self.message.configure(background="#ffffff")
        
        # Get and display employee username
        with sqlite3.connect("./Database/store.db") as db:
            cur = db.cursor()
            cur.execute("SELECT username FROM employees WHERE employee_id = ?", [self.employee_id])
            result = cur.fetchone()
            if result:
                self.message.configure(text=result[0])
        self.message.configure(anchor="w")

        # Clock
        self.clock = Label(self.root)
        self.clock.place(relx=0.9, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        # Transaction Display
        self.transaction_id = None  # Will be set when bill is generated
        
        # Date Display
        self.date_label = Label(self.root)
        self.date_label.place(relx=0.791, rely=0.23, width=240, height=24)
        self.date_label.configure(font="-family {Poppins} -size 12")
        self.date_label.configure(text=datetime.now().strftime('%Y-%m-%d'))
        self.date_label.configure(background="#ffffff")

        # Product Selection Area
        self.setup_product_selection()
        
        # Bill Text Area
        self.setup_bill_area()
        
        # Buttons
        self.setup_buttons()

        # Start clock
        self.update_clock()

    def setup_product_selection(self):
        text_font = ("Poppins", "8")
        
        # Category Combobox
        self.combo1 = ttk.Combobox(self.root)
        self.combo1.place(relx=0.035, rely=0.408, width=477, height=26)
        
        with sqlite3.connect("./Database/store.db") as db:
            cur = db.cursor()
            cur.execute("""
                SELECT DISTINCT p.product_cat 
                FROM products p 
                JOIN inventory i ON p.product_id = i.product_id 
                WHERE i.stock > 0
            """)
            categories = [row[0] for row in cur.fetchall()]
            
        self.combo1.configure(values=categories)
        self.combo1.configure(state="readonly")
        self.combo1.configure(font=text_font)
        self.combo1.bind("<<ComboboxSelected>>", self.get_category)

        # Subcategory Combobox
        self.combo2 = ttk.Combobox(self.root)
        self.combo2.place(relx=0.035, rely=0.479, width=477, height=26)
        self.combo2.configure(state="disabled")
        self.combo2.configure(font=text_font)

        # Product Combobox
        self.combo3 = ttk.Combobox(self.root)
        self.combo3.place(relx=0.035, rely=0.551, width=477, height=26)
        self.combo3.configure(state="disabled")
        self.combo3.configure(font=text_font)

        # Quantity Entry
        self.entry4 = Entry(self.root)
        self.entry4.place(relx=0.035, rely=0.629, width=477, height=26)
        self.entry4.configure(font=text_font)
        self.entry4.configure(state="disabled")

    def setup_bill_area(self):
        self.Scrolledtext1 = tkst.ScrolledText(self.root)
        self.Scrolledtext1.place(relx=0.439, rely=0.586, width=695, height=275)
        self.Scrolledtext1.configure(borderwidth=0)
        self.Scrolledtext1.configure(font="-family {Podkova} -size 8")
        self.Scrolledtext1.configure(state="disabled")

    def setup_buttons(self):
        button_style = {
            'font': "-family {Poppins SemiBold} -size 10",
            'bg': "#CF1E14",
            'fg': "#ffffff",
            'relief': "flat",
            'cursor': "hand2"
        }

        # Add to Cart button
        self.button7 = Button(self.root, text="Add To Cart", command=self.add_to_cart, **button_style)
        self.button7.place(relx=0.098, rely=0.734, width=86, height=26)

        # Remove button
        self.button9 = Button(self.root, text="Remove", command=self.remove_product, **button_style)
        self.button9.place(relx=0.194, rely=0.734, width=68, height=26)

        # Clear Selection button
        self.button8 = Button(self.root, text="Clear", command=self.clear_selection, **button_style)
        self.button8.place(relx=0.274, rely=0.734, width=84, height=26)

        # Total button
        self.button3 = Button(self.root, text="Total", command=self.total_bill, **button_style)
        self.button3.place(relx=0.048, rely=0.885, width=86, height=25)

        # Generate button
        self.button4 = Button(self.root, text="Generate", command=self.gen_bill, **button_style)
        self.button4.place(relx=0.141, rely=0.885, width=84, height=25)

        # Clear Bill button
        self.button5 = Button(self.root, text="Clear", command=self.clear_bill, **button_style)
        self.button5.place(relx=0.230, rely=0.885, width=86, height=25)

        # Exit button
        self.button6 = Button(self.root, text="Exit", command=self.exit_app, **button_style)
        self.button6.place(relx=0.322, rely=0.885, width=86, height=25)

        # Logout button
        self.logout_button = Button(self.root, text="Logout", command=self.logout, **button_style)
        self.logout_button.place(relx=0.030, rely=0.1025, width=76, height=23)

    def update_clock(self):
        string = time.strftime('%H:%M:%S %p') 
        self.clock.config(text=string)
        self.clock.after(1000, self.update_clock)

    def get_category(self, event=None):
        self.combo2.configure(state="readonly")
        self.combo2.set('')
        self.combo3.set('')
        
        try:
            with sqlite3.connect("./Database/store.db") as db:
                cur = db.cursor()
                cur.execute("""
                    SELECT DISTINCT p.product_subcat 
                    FROM products p 
                    JOIN inventory i ON p.product_id = i.product_id 
                    WHERE p.product_cat = ? AND i.stock > 0
                """, [self.combo1.get()])
                subcats = [row[0] for row in cur.fetchall()]
                print(f"Available subcategories: {subcats}")  # Debug print
                
            self.combo2.configure(values=subcats)
            self.combo2.bind("<<ComboboxSelected>>", self.get_subcat)
            self.combo3.configure(state="disabled")
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            messagebox.showerror("Database Error", f"Error fetching subcategories: {e}", parent=self.root)

    def get_subcat(self, event=None):
        self.combo3.configure(state="readonly")
        self.combo3.set('')
        
        try:
            with sqlite3.connect("./Database/store.db") as db:
                cur = db.cursor()
                cur.execute("""
                    SELECT p.product_name 
                    FROM products p 
                    JOIN inventory i ON p.product_id = i.product_id 
                    WHERE p.product_cat = ? 
                    AND p.product_subcat = ? 
                    AND i.stock > 0
                """, [self.combo1.get(), self.combo2.get()])
                
                products = [row[0] for row in cur.fetchall()]
                print(f"Available products: {products}")  # Debug print
                
            self.combo3.configure(values=products)
            self.combo3.bind("<<ComboboxSelected>>", self.show_qty)
            self.entry4.configure(state="disabled")
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            messagebox.showerror("Database Error", f"Error fetching products: {e}", parent=self.root)
            
    def show_products(self, event=None):
        self.combo3.configure(state="readonly")
        self.combo3.set('')
        
        try:
            with sqlite3.connect("./Database/store.db") as db:
                cur = db.cursor()
                cur.execute("""
                    SELECT p.product_name 
                    FROM products p 
                    JOIN inventory i ON p.product_id = i.product_id 
                    WHERE p.product_cat = ? 
                    AND p.product_subcat = ? 
                    AND i.stock > 0
                """, [self.combo1.get(), self.combo2.get()])
                
                products = [row[0] for row in cur.fetchall()]
                print(f"Available products: {products}")  # Debug print
                
            self.combo3.configure(values=products)
            self.combo3.bind("<<ComboboxSelected>>", self.show_qty)
            self.entry4.configure(state="disabled")
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            messagebox.showerror("Database Error", f"Error fetching products: {e}", parent=self.root)

    def show_qty(self, event=None):
        self.entry4.configure(state="normal")
        self.qty_label = Label(self.root)
        self.qty_label.place(relx=0.033, rely=0.664, width=82, height=26)
        self.qty_label.configure(font="-family {Poppins} -size 8")
        self.qty_label.configure(anchor="w")

        with sqlite3.connect("./Database/store.db") as db:
            cur = db.cursor()
            cur.execute("""
                SELECT i.stock, i.sell_price, p.product_id 
                FROM inventory i 
                JOIN products p ON i.product_id = p.product_id 
                WHERE p.product_name = ?
            """, [self.combo3.get()])
            result = cur.fetchone()
            
            if result:
                self.current_stock = result[0]
                self.current_price = result[1]
                self.current_product_id = result[2]
                self.qty_label.configure(text=f"In Stock: {self.current_stock}")
                self.qty_label.configure(background="#ffffff")
                self.qty_label.configure(foreground="#333333")

    def add_to_cart(self):
        if not self.combo3.get():
            messagebox.showerror("Error", "Please select a product", parent=self.root)
            return

        qty = self.entry4.get()
        if not qty.isdigit():
            messagebox.showerror("Error", "Please enter a valid quantity", parent=self.root)
            return

        qty = int(qty)
        if qty > self.current_stock:
            messagebox.showerror("Error", "Insufficient stock", parent=self.root)
            return

        if qty <= 0:
            messagebox.showerror("Error", "Invalid quantity", parent=self.root)
            return

        item = Item(self.current_product_id, self.combo3.get(), self.current_price, qty)
        self.cart.add_item(item)

        self.Scrolledtext1.configure(state="normal")
        bill_text = f"{item.product_name}\t\t{qty}\t\t{item.price * qty:.2f}\n"
        self.Scrolledtext1.insert(END, bill_text)
        self.Scrolledtext1.configure(state="disabled")
        self.clear_selection()

    def remove_product(self):
        if self.cart.isEmpty():
            messagebox.showerror("Error", "Cart is empty", parent=self.root)
            return

        self.Scrolledtext1.configure(state="normal")
        all_lines = self.Scrolledtext1.get("1.0", END).split("\n")
        if len(all_lines) > 2:  # Check if there's content to remove
            all_lines = all_lines[:-2]  # Remove last item and empty line
            self.Scrolledtext1.delete("1.0", END)
            self.Scrolledtext1.insert(END, "\n".join(all_lines) + "\n")
        self.Scrolledtext1.configure(state="disabled")
        self.cart.remove_item()

    def clear_selection(self):
        self.entry4.delete(0, END)
        self.combo1.set('')
        self.combo2.set('')
        self.combo3.set('')
        self.combo2.configure(state="disabled")
        self.combo3.configure(state="disabled")
        self.entry4.configure(state="disabled")
        try:
            self.qty_label.configure(foreground="#ffffff")
        except AttributeError:
            pass

    def total_bill(self):
        if self.cart.isEmpty():
            messagebox.showerror("Error", "Cart is empty", parent=self.root)
            return

        self.Scrolledtext1.configure(state="normal")
        bill_content = self.Scrolledtext1.get("1.0", END)
        if "Total" not in bill_content:
            divider = "\n" + "="*50 + "\n"
            total = f"Total\t\t\t\tRp. {self.cart.total():.2f}"
            self.Scrolledtext1.insert(END, f"{divider}{total}{divider}")
        self.Scrolledtext1.configure(state="disabled")

    def gen_bill(self):
        if self.state != 1:
            return

        if self.cart.isEmpty():
            messagebox.showerror("Error", "Cart is empty", parent=self.root)
            return

        # Generate total if not already done
        if "Total" not in self.Scrolledtext1.get("1.0", END):
            self.total_bill()

        # Get OVO phone number from user
        ovo_phone = simpledialog.askstring("OVO Payment", 
                                        "Enter OVO phone number:",
                                        parent=self.root)
        
        if not ovo_phone:
            messagebox.showerror("Error", "OVO phone number is required", parent=self.root)
            return

        try:
            with sqlite3.connect("./Database/store.db") as db:
                cur = db.cursor()
                
                # Create transaction with pending status
                cur.execute("""
                    INSERT INTO transactions (transaction_details, total, employee_id, transaction_status)
                    VALUES (?, ?, ?, 'pending')
                """, [self.Scrolledtext1.get("1.0", END), self.cart.total(), self.employee_id])
                
                self.transaction_id = cur.lastrowid

                # Initialize Doku OVO payment
                doku_payment = DokuOVOPayment()
                
                # Create progress dialog
                progress_window = Toplevel(self.root)
                progress_window.title("Payment Processing")
                progress_window.geometry("300x150")
                progress_window.transient(self.root)
                
                Label(progress_window, 
                    text=f"Waiting for payment confirmation...\nInvoice: {doku_payment.INVOICE_NUMBER}\nPlease complete payment in OVO app", 
                    pady=10).pack()
                
                progress = ttk.Progressbar(progress_window, length=200, mode='determinate')
                progress.pack(pady=20)
                
                time_label = Label(progress_window, text="Time remaining: 70s")
                time_label.pack()

                payment_status = {'completed': False, 'error': None, 'response': None}

                def process_payment():
                    try:
                        # Convert total to integer (OVO requires amount without decimals)
                        amount = int(self.cart.total())
                        print(f"Processing payment for amount: {amount}")
                        
                        # Initial payment request
                        response = doku_payment.create_payment(
                            amount=amount,
                            ovo_phone=ovo_phone
                        )
                        print(f"Initial payment response: {response}")
                        
                        if 'error' in response:
                            raise Exception(response['error']['message'])
                            
                        start_timestamp = time.time()
                        print(f"Starting payment wait at: {start_timestamp}")
                        
                        while time.time() - start_timestamp < 70:
                            current_timestamp = time.time()
                            elapsed = int(current_timestamp - start_timestamp)
                            remaining = 70 - elapsed
                            
                            print(f"Checking payment status - Elapsed: {elapsed}s, Remaining: {remaining}s")
                            
                            if response.get('ovo_payment', {}).get('status') == 'SUCCESS':
                                payment_status['completed'] = True
                                payment_status['response'] = response
                                print("Payment completed successfully")
                                break
                                
                            # Update progress bar
                            progress['value'] = (elapsed / 70) * 100
                            time_label.config(text=f"Time remaining: {remaining}s")
                            progress_window.update()
                            time.sleep(1)
                            
                    except Exception as e:
                        print(f"Payment error occurred: {str(e)}")
                        payment_status['error'] = str(e)
                    finally:
                        print("Payment processing completed")
                        progress_window.destroy()

                # Start payment processing in a separate thread
                payment_thread = threading.Thread(target=process_payment)
                payment_thread.start()
                
                # Wait for the thread to complete
                self.root.wait_window(progress_window)

                # Process the payment result
                if payment_status['error']:
                    raise Exception(payment_status['error'])
                
                if payment_status['completed']:
                    # Update transaction status to completed
                    cur.execute("""
                        UPDATE transactions 
                        SET transaction_status = 'completed' 
                        WHERE transaction_id = ?
                    """, [self.transaction_id])
                    
                    # Update inventory
                    cart_items = self.cart.allCart()
                    for product_id, qty in cart_items.items():
                        cur.execute("""
                            UPDATE inventory 
                            SET stock = stock - ? 
                            WHERE product_id = ?
                        """, [qty, product_id])

                    db.commit()
                    
                    messagebox.showinfo(
                        "Payment Success", 
                        f"Transaction ID: {self.transaction_id}\nInvoice: {doku_payment.INVOICE_NUMBER}\nPayment completed successfully!",
                        parent=self.root
                    )
                    self.state = 0
                else:
                    raise Exception("Payment timeout or not completed")

        except Exception as e:
            messagebox.showerror("Payment Error", f"Failed to process payment: {str(e)}", parent=self.root)
            if db:
                db.rollback()

    def clear_bill(self):
        self.Scrolledtext1.configure(state="normal")
        self.Scrolledtext1.delete(1.0, END)
        self.Scrolledtext1.configure(state="disabled")
        self.cart.remove_items()
        self.state = 1
        self.transaction_id = None
        self.clear_selection()

    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=self.root):
            self.root.destroy()

    def logout(self):
        if messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?",
            parent=self.root
        ):
            self.root.destroy()
            # Find the root window and show it
            root = self.root.master
            while root.master:
                root = root.master
            root.deiconify()