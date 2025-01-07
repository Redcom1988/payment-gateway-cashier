import os
from time import strftime
from tkinter import *
from tkinter import ttk, messagebox, font, PhotoImage
from datetime import datetime 
import sqlite3

class InvoiceManager:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_fonts()
        self.setup_gui()
        self.load_transaction_data()

    def setup_window(self):
        """Initialize main window properties"""
        self.root.geometry("1366x768")
        self.root.resizable(0, 0)
        self.root.title(f"Invoice View")
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
            size=14,
            weight="bold"
        )

        self.poppins_small = font.Font(
            family="Poppins",
            size=10,
            weight="normal"
        )

        if os.path.exists(font_folder):
            for font_file in os.listdir(font_folder):
                if font_file.endswith('.ttf'):
                    font_path = os.path.join(font_folder, font_file)
                    try:
                        font.Font(file=font_path)
                    except:
                        print(f"Could not load font: {font_file}")

    def setup_header(self):
        """Setup header section with admin label and time info"""
        # Admin Label
        self.header_label = Label(
            self.root,
            text="ADMIN",
            font=self.poppins_small,
            fg="#ffffff",
            bg="#FE6B61",
            anchor="w"
        )
        self.header_label.place(x=63, y=43, width=62, height=30)

        # Date Time Label
        self.time_label = Label(
            self.root,
            text="Current Date and Time (UTC): 2025-01-07 00:57:15",
            font=self.poppins_small,
            fg="#333333",
            bg="#F0F0F0"
        )
        self.time_label.place(x=63, y=81, width=300, height=23)

        # User Label
        self.user_label = Label(
            self.root,
            text="Current User's Login: Redcom1988",
            font=self.poppins_small,
            fg="#333333",
            bg="#F0F0F0"
        )
        self.user_label.place(x=363, y=81, width=250, height=23)

    def setup_gui(self):
        """Setup all GUI elements"""
        self.setup_header()
        self.setup_background()
        self.setup_treeview()

    def setup_background(self):
        """Setup background image"""
        try:
            self.bg_image = PhotoImage(file="./images/invoices.png")
            self.bg_label = Label(self.root, image=self.bg_image)
            self.bg_label.place(x=0, y=0, width=1366, height=768)
        except:
            print("Could not load background image")
            self.bg_label = Label(self.root, bg="white")
            self.bg_label.place(x=0, y=0, width=1366, height=768)

    def setup_treeview(self):
        # Scrollbars
        self.scrollbar_x = Scrollbar(self.root, orient=HORIZONTAL)
        self.scrollbar_y = Scrollbar(self.root, orient=VERTICAL)

        # Treeview
        columns = ('transaction_id', 'date', 'details', 'total', 
                'status', 'employee_id', 'employee_name')
        self.tree = ttk.Treeview(
            self.root, 
            columns=columns, 
            show="headings",
            xscrollcommand=self.scrollbar_x.set,
            yscrollcommand=self.scrollbar_y.set
        )

        # Configure columns
        column_widths = {
            'transaction_id': 100,
            'date': 200,
            'details': 400,
            'total': 150,
            'status': 150,
            'employee_id': 100,
            'employee_name': 150
        }

        column_headings = {
            'transaction_id': 'Trans. ID',
            'date': 'Date',
            'details': 'Transaction Details',
            'total': 'Total Amount',
            'status': 'Status',
            'employee_id': 'Emp. ID',
            'employee_name': 'Employee'
        }

        # Format columns
        for col in columns:
            self.tree.heading(col, text=column_headings[col], anchor=CENTER)
            self.tree.column(col, width=column_widths[col], anchor=CENTER)

        # Apply style
        style = ttk.Style()
        style.configure(
            "Treeview",
            font=self.poppins_small,
            rowheight=50  # Increased row height
        )
        style.configure(
            "Treeview.Heading",
            font=self.poppins_regular
        )

        # Place treeview and scrollbars - adjusted positioning
        self.tree.place(relx=0.05, rely=0.18, width=1250, height=550)  # Wider and slightly higher
        self.scrollbar_y.place(relx=0.954, rely=0.18, width=22, height=548)  # Adjusted Y position
        self.scrollbar_x.place(relx=0.05, rely=0.924, width=1254, height=22)  # Adjusted width
        
        # Configure scrollbars
        self.scrollbar_x.config(command=self.tree.xview)
        self.scrollbar_y.config(command=self.tree.yview)

    def load_transaction_data(self):
        """Load and display transaction data"""
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)

            conn = sqlite3.connect('./Database/store.db')
            cursor = conn.cursor()
            
            # Get all transactions
            cursor.execute("""
                SELECT 
                    t.transaction_id,
                    t.date,
                    t.transaction_details,
                    t.total,
                    t.transaction_status,
                    t.employee_id,
                    e.username
                FROM transactions t
                LEFT JOIN employees e ON t.employee_id = e.employee_id
                ORDER BY t.transaction_id DESC
            """)
            
            transactions = cursor.fetchall()
            
            for transaction in transactions:
                self.tree.insert(
                    '',
                    'end',
                    values=(
                        transaction[0],  # Transaction ID
                        transaction[1],  # Date
                        transaction[2],  # Details
                        f"${transaction[3]:.2f}",  # Total
                        transaction[4].upper(),  # Status
                        transaction[5],  # Employee ID
                        transaction[6]   # Employee Name
                    )
                )
            
            conn.close()
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading transaction data: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def refresh_data(self):
        """Refresh transaction data"""
        self.load_transaction_data()

if __name__ == "__main__":
    root = Tk()
    app = InvoiceManager(root)
    root.mainloop()