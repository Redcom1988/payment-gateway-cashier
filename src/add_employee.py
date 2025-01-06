from time import strftime
from tkinter import *
from tkinter import messagebox
from utils.utils import valid_phone
import sqlite3


class Add_Employee:
    def __init__(self, top=None, employee_manager=None):
        self.employee_manager = employee_manager
        self.window = top
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Add Employee")

        self.label1 = Label(top)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/add_employee.png")
        self.label1.configure(image=self.img)

        self.clock = Label(top)
        self.clock.place(relx=0.84, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        self.r1 = top.register(self.testint)
        self.r2 = top.register(self.testchar)

        # Username field (previously name)
        self.entry1 = Entry(top)
        self.entry1.place(relx=0.132, rely=0.296, width=374, height=30)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")

        # Contact number field
        self.entry2 = Entry(top)
        self.entry2.place(relx=0.132, rely=0.413, width=374, height=30)
        self.entry2.configure(font="-family {Poppins} -size 12")
        self.entry2.configure(relief="flat")
        self.entry2.configure(validate="key", validatecommand=(self.r1, "%P"))

        # Role field (previously aadhar)
        self.entry3 = Entry(top)
        self.entry3.place(relx=0.132, rely=0.529, width=374, height=30)
        self.entry3.configure(font="-family {Poppins} -size 12")
        self.entry3.configure(relief="flat")

        # Address field
        self.entry4 = Entry(top)
        self.entry4.place(relx=0.527, rely=0.413, width=374, height=30)
        self.entry4.configure(font="-family {Poppins} -size 12")
        self.entry4.configure(relief="flat")

        # Password field
        self.entry5 = Entry(top)
        self.entry5.place(relx=0.527, rely=0.529, width=374, height=30)
        self.entry5.configure(font="-family {Poppins} -size 12")
        self.entry5.configure(relief="flat")
        self.entry5.configure(show="*")

        # Add button
        self.button1 = Button(top)
        self.button1.place(relx=0.408, rely=0.836, width=96, height=34)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#CF1E14")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#CF1E14")
        self.button1.configure(font="-family {Poppins SemiBold} -size 14")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""ADD""")
        self.button1.configure(command=self.add)

        # Cancel button (previously Clear)
        self.button2 = Button(top)
        self.button2.place(relx=0.526, rely=0.836, width=86, height=34)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#CF1E14")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#CF1E14")
        self.button2.configure(font="-family {Poppins SemiBold} -size 14")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""CANCEL""")
        self.button2.configure(command=self.cancel)

    def testint(self, val):
        if val.isdigit():
            return True
        elif val == "":
            return True
        return False

    def testchar(self, val):
        if val.isalpha():
            return True
        elif val == "":
            return True
        return False

    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)

    def add(self):
        username = self.entry1.get()
        contact = self.entry2.get()
        role = self.entry3.get()
        address = self.entry4.get()
        password = self.entry5.get()

        if username.strip():
            if valid_phone(contact):
                if role.lower() in ['admin', 'employee']:  # Validate role
                    if address:
                        if password:
                            try:
                                db = sqlite3.connect('./Database/store.db')
                                query = (
                                    "INSERT INTO employees(username, contact_num, address, password, role) "
                                    "VALUES(?,?,?,?,?)"
                                )
                                db.execute(query, [username, contact, address, password, role.lower()])
                                db.commit()
                                messagebox.showinfo("Success!", 
                                                "Employee successfully added to database.", 
                                                parent=self.window)
                                
                                # Refresh the employee manager's tree view if available
                                if self.employee_manager:
                                    self.employee_manager.tree.delete(*self.employee_manager.tree.get_children())
                                    self.employee_manager.load_employee_data()
                                    
                                self.cancel()  # Close window after successful add
                            except sqlite3.Error as e:
                                messagebox.showerror("Database Error", 
                                                f"Error adding employee: {str(e)}", 
                                                parent=self.window)
                        else:
                            messagebox.showerror("Error", 
                                               "Please enter a password.", 
                                               parent=self.window)
                    else:
                        messagebox.showerror("Error", 
                                           "Please enter an address.", 
                                           parent=self.window)
                else:
                    messagebox.showerror("Error", 
                                       "Role must be either 'admin' or 'employee'.", 
                                       parent=self.window)
            else:
                messagebox.showerror("Error", 
                                   "Invalid phone number.", 
                                   parent=self.window)
        else:
            messagebox.showerror("Error", 
                               "Please enter a username.", 
                               parent=self.window)

    def cancel(self):
        """Close the add employee window"""
        self.window.destroy()