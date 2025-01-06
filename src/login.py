import os
from tkinter import *
from tkinter import messagebox
from tkinter import font
import sqlite3

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768")
        self.root.title(f"LOGIN SCREEN")
        self.root.resizable(0, 0)
        self.create_fonts()

        self.username = StringVar()
        self.password = StringVar()

        self.setup_gui()

    def create_fonts(self):
        font_folder = "./fonts"
        
        self.poppins_regular = font.Font(
            family="Poppins",
            size=10,
            weight="normal"
        )
        
        self.poppins_semibold = font.Font(
            family="Poppins",
            size=20,
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
            self.bg_image = PhotoImage(file="images/login.png")
            self.bg_label = Label(self.root, image=self.bg_image)
            self.bg_label.place(relx=0, rely=0, width=1366, height=768)
        except:
            print("Could not load background image")
            self.bg_label = Label(self.root, bg="white")
            self.bg_label.place(relx=0, rely=0, width=1366, height=768)

        # Username entry
        self.username_entry = Entry(self.root, textvariable=self.username)
        self.username_entry.place(relx=0.373, rely=0.273, width=374, height=24)
        self.username_entry.configure(
            font=self.poppins_regular,
            relief="flat"
        )

        # Password entry
        self.password_entry = Entry(self.root, textvariable=self.password, show="*")
        self.password_entry.place(relx=0.373, rely=0.384, width=374, height=24)
        self.password_entry.configure(
            font=self.poppins_regular,
            relief="flat"
        )

        # Login button
        self.login_btn = Button(
            self.root,
            text="LOGIN",
            command=self.login,
            font=self.poppins_semibold,
            bg="#D2463E",
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2"
        )
        self.login_btn.place(relx=0.366, rely=0.685, width=356, height=43)

        # Bind Enter key to login
        self.root.bind('<Return>', self.login)

    def login(self, event=None):
        username = self.username.get()
        password = self.password.get()

        try:
            conn = sqlite3.connect('Database/store.db')
            cursor = conn.cursor()
            
            query = "SELECT * FROM employees WHERE username = ? AND password = ?"
            cursor.execute(query, [username, password])
            results = cursor.fetchone()

            if results:
                self.employee_id = results[0]
                if results[5] == "admin":
                    messagebox.showinfo("Success", "Login successful")
                    self.clear_entries()
                    self.root.withdraw()
                    self.open_admin_panel()
                elif results[5] == "employee":
                    messagebox.showinfo("Success", "Login successful")
                    self.clear_entries()
                    self.root.withdraw()
                    self.open_employee_panel()
            else:
                messagebox.showerror("Error", "Invalid credentials")
                self.password_entry.delete(0, END)
                
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def clear_entries(self):
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)

    def open_admin_panel(self):
        from admin2 import AdminPage
        admin_window = Toplevel(self.root)
        AdminPage(admin_window)  

    def open_employee_panel(self):
        from employee import bill_window
        employee_window = Toplevel()
        bill_window(employee_window, self.employee_id)