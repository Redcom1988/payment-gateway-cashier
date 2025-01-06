import tkinter as tk
from tkinter import Toplevel, ttk, messagebox, Label, Entry, Button, Scrollbar, PhotoImage, HORIZONTAL, VERTICAL, W, NO
from time import strftime
import sqlite3
from update_employee import Update_Employee
from add_employee import Add_Employee

class EmployeeManager:
    def __init__(self, top=None):
        self.window = top
        self.setup_window()
        self.create_ui_elements()
        self.setup_treeview()
        self.load_employee_data()

    def setup_window(self):
        self.window.geometry("1366x768")
        self.window.resizable(0, 0)
        self.window.title("Employee Management")

    def create_ui_elements(self):
        # Background Image
        self.background = Label(self.window)
        self.background.place(relx=0, rely=0, width=1366, height=768)
        self.bg_image = PhotoImage(file="./images/employee.png")
        self.background.configure(image=self.bg_image)

        # Header Elements
        self.create_header()
        
        # Search Elements
        self.create_search_section()
        
        # Action Buttons
        self.create_action_buttons()

    def create_header(self):
        # Admin Label
        self.admin_label = Label(self.window, text="ADMIN",
                               font="-family {Poppins} -size 10",
                               foreground="#000000", background="#ffffff",
                               anchor="w")
        self.admin_label.place(relx=0.046, rely=0.055, width=136, height=30)

        # Clock Label
        self.clock_label = Label(self.window,
                               font="-family {Poppins Light} -size 12",
                               foreground="#000000", background="#ffffff")
        self.clock_label.place(relx=0.9, rely=0.065, width=102, height=36)
        self.update_clock()

    def create_search_section(self):
        # Search Entry
        self.search_entry = Entry(self.window,
                                font="-family {Poppins} -size 12",
                                relief="flat")
        self.search_entry.place(relx=0.040, rely=0.286, width=240, height=28)

        # Search Button
        self.search_button = Button(self.window, text="Search",
                                  font="-family {Poppins SemiBold} -size 10",
                                  background="#CF1E14", foreground="#ffffff",
                                  command=self.search_employee,
                                  relief="flat", cursor="hand2")
        self.search_button.place(relx=0.229, rely=0.289, width=76, height=23)

    def create_action_buttons(self):
        button_configs = [
            ("ADD EMPLOYEE", 0.432, self.add_employee),
            ("UPDATE EMPLOYEE", 0.5, self.update_employee),
            ("DELETE EMPLOYEE", 0.57, self.delete_employee),
            ("EXIT", 0.885, self.exit_program)
        ]

        for text, rely, command in button_configs:
            btn = Button(self.window, text=text,
                        font="-family {Poppins SemiBold} -size 12",
                        background="#CF1E14", foreground="#ffffff",
                        command=command, relief="flat", cursor="hand2")
            
            if text == "EXIT":
                btn.place(relx=0.135, rely=rely, width=76, height=23)
            else:
                btn.place(relx=0.052, rely=rely, width=306, height=28)

    def setup_treeview(self):
        # Scrollbars
        self.scrollbar_x = Scrollbar(self.window, orient=HORIZONTAL)
        self.scrollbar_y = Scrollbar(self.window, orient=VERTICAL)

        # Treeview
        columns = ("Employee ID", "Username", "Contact No.", "Address", "Role")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings",
                                xscrollcommand=self.scrollbar_x.set,
                                yscrollcommand=self.scrollbar_y.set)

        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col, anchor=W)
            self.tree.column(col, stretch=NO, minwidth=0, width=176)  # Evenly distributed width

        self.tree.place(relx=0.307, rely=0.203, width=880, height=550)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Place scrollbars
        self.scrollbar_y.place(relx=0.954, rely=0.203, width=22, height=548)
        self.scrollbar_x.place(relx=0.307, rely=0.924, width=884, height=22)
        
        self.scrollbar_x.config(command=self.tree.xview)
        self.scrollbar_y.config(command=self.tree.yview)

    def load_employee_data(self):
        try:
            conn = sqlite3.connect('./Database/store.db')
            cursor = conn.cursor()
            cursor.execute("SELECT employee_id, username, contact_num, address, role FROM employees")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading employee data: {str(e)}")

    def search_employee(self):
        search_term = self.search_entry.get()
        for item in self.tree.get_children():
            if str(search_term) in str(self.tree.item(item)['values'][1]):  
                self.tree.selection_set(item)
                self.tree.focus(item)
                messagebox.showinfo("Success", f"Employee ID: {search_term} found.")
                return
        messagebox.showerror("Error", f"Employee ID: {search_term} not found.")

    def update_clock(self):
        time_string = strftime("%H:%M:%S %p")
        self.clock_label.config(text=time_string)
        self.clock_label.after(1000, self.update_clock)

    selected_items = []
    
    def on_tree_select(self, event):
        self.selected_items = self.tree.selection()

    def add_employee(self):
        try:
            # Create add window
            add_window = Toplevel(self.window)
            add_emp = Add_Employee(add_window)
            
            # Configure window closing behavior
            def on_closing():
                add_window.destroy()
                self.tree.delete(*self.tree.get_children())
                self.load_employee_data()
                
            add_window.protocol("WM_DELETE_WINDOW", on_closing)
            
            # Start clock
            add_emp.time()
            
            # Make the add window modal
            add_window.transient(self.window)
            add_window.grab_set()
            
            # Wait for window to close and refresh data
            add_window.wait_window()
            self.tree.delete(*self.tree.get_children())
            self.load_employee_data()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open add employee window: {str(e)}")

    def update_employee(self):
        if len(self.selected_items) != 1:
            messagebox.showerror("Error", "Please select exactly one employee to update.")
            return
            
        # Get the selected employee's data
        selected_item = self.selected_items[0]
        employee_data = self.tree.item(selected_item)['values']
        
        try:
            # Create update window
            update_window = Toplevel(self.window)
            # Pass employee_id as third parameter
            update_emp = Update_Employee(update_window, self, employee_data[0])
            
            # Populate fields with current data
            update_emp.entry1.insert(0, employee_data[1])  # Username
            update_emp.entry2.insert(0, employee_data[2])  # Contact
            update_emp.entry3.insert(0, employee_data[4])  # Role
            update_emp.entry4.insert(0, employee_data[3])  # Address
            
            # Configure window closing behavior
            update_window.protocol("WM_DELETE_WINDOW", update_emp.cancel)
            
            # Start clock
            update_emp.time()
            
            # Make the update window modal
            update_window.transient(self.window)
            update_window.grab_set()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open update window: {str(e)}")

    def delete_employee(self):
        if not self.selected_items:
            messagebox.showerror("Error", "Please select employee(s) to delete.")
            return
            
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete selected employee(s)?"):
            conn = None
            try:
                conn = sqlite3.connect('./Database/store.db')
                cursor = conn.cursor()
                for item in self.selected_items:
                    employee_id = self.tree.item(item)['values'][0]
                    cursor.execute("DELETE FROM employees WHERE employee_id = ?", (employee_id,))
                conn.commit()
                self.tree.delete(*self.tree.get_children())
                self.load_employee_data()  # Refresh the display
                messagebox.showinfo("Success", "Employee(s) deleted successfully.")
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Failed to delete employee(s): {str(e)}")
            finally:
                if conn:
                    conn.close()

    def exit_program(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.window.destroy()