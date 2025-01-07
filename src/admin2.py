import os
from tkinter import *
from tkinter import messagebox, font, PhotoImage, Toplevel

class AdminPage:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768")
        self.root.title("Admin Dashboard")
        self.root.resizable(0, 0)
        self.create_fonts()
        self.setup_gui()

    def create_fonts(self):
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
        # Background
        try:
            self.bg_image = PhotoImage(file="./images/admin.png")
            self.bg_label = Label(self.root, image=self.bg_image)
            self.bg_label.place(x=0, y=0, width=1366, height=768)
        except:
            print("Could not load background image")
            self.bg_label = Label(self.root, bg="white")
            self.bg_label.place(x=0, y=0, width=1366, height=768)

        # Create header with admin label
        self.header = Label(
            self.root,
            text="ADMIN",
            font=self.poppins_regular,
            fg="#ffffff",
            bg="#FE6B61",
            anchor="w"
        )
        self.header.place(x=63, y=43, width=62, height=30)

        # Navigation buttons
        self.setup_navigation()
        
        # Logout button
        self.setup_logout_button()

    def setup_navigation(self):
        """Create the main navigation buttons"""
        nav_buttons = [
            ("Inventory", 0.14, self.open_inventory),
            ("Employees", 0.338, self.open_employees),
            ("Invoices", 0.536, self.open_invoices),
            ("About Us", 0.732, self.open_about)
        ]
        
        for text, x_pos, command in nav_buttons:
            btn = Button(
                self.root,
                text=text,
                font=self.poppins_semibold,
                fg="#333333",
                bg="#ffffff",
                relief="flat",
                overrelief="flat",
                activebackground="#ffffff",
                cursor="hand2",
                borderwidth=0,
                command=command
            )
            btn.place(
                relx=x_pos,
                rely=0.508,
                width=146,
                height=63
            )

    def setup_logout_button(self):
        self.logout_btn = Button(
            self.root,
            text="Logout",
            font=self.poppins_regular,
            fg="#ffffff",
            bg="#CF1E14",
            relief="flat",
            overrelief="flat",
            activebackground="#CF1E14",
            cursor="hand2",
            borderwidth=0,
            command=self.logout
        )
        self.logout_btn.place(x=48, y=81, width=76, height=23)

    def open_inventory(self):
        try:
            from inventory_manager import InventoryManager
            inv_window = Toplevel(self.root)
            InventoryManager(inv_window)
        except ImportError:
            messagebox.showerror("Error", "Could not load inventory manager")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def open_employees(self):
        try:
            from employee_manager import EmployeeManager
            emp_window = Toplevel(self.root)
            EmployeeManager(emp_window)
        except ImportError:
            messagebox.showerror("Error", "Could not load employee manager module")
            self.root.deiconify()  
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.root.deiconify() 

    def open_invoices(self):
        try:
            # Create a new window for invoices
            invoice_window = Toplevel(self.root)
            
            # Import and initialize InvoiceManager
            from invoice_manager import InvoiceManager 
            InvoiceManager(invoice_window)
            
        except ImportError:
            messagebox.showerror("Error", "Could not load invoice manager module")
            self.root.deiconify()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.root.deiconify()

    def open_about(self):
        messagebox.showinfo("About", "Payment Gateway Cashier System\nVersion 1.0")

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