__author__ = 'Kelompok 6 - D'
'1. Made Arief Budi Dharma (2308561034)'
'2. Adika Setyadharma Susilo (2308561088)'
'3. I Gusti Nyoman Pramajaya (230856109)'
'4. I Gede Rama Yasa Mahendra (2308561016)'

import os
import sys
from tkinter import *
from tkinter import messagebox
from tkinter import font

class MainPage:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768")
        self.root.title("Aplikasi Belanja Online")
        self.root.resizable(0, 0)
        
        self.create_fonts()
        self.setup_gui()
        
        # Set up exit protocol
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

    def create_fonts(self):
        font_folder = "./fonts"

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
        self.bg_image = PhotoImage(file="images/main.png")
        self.bg_label = Label(self.root, image=self.bg_image)
        self.bg_label.place(relx=0, rely=0, width=1366, height=768)

        # Start Button
        self.start_btn = Button(
            self.root,
            text="START",
            command=self.open_login,
            font=self.poppins_semibold,
            bg="#D2463E",
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2"
        )
        self.start_btn.place(relx=0.366, rely=0.685, width=356, height=83)

    def exit_app(self):
        sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=self.root)
        if sure:
            self.root.destroy()

    def open_login(self):
        self.root.withdraw()
        try:
            from login import LoginPage
            login_window = Toplevel(self.root)
            login_app = LoginPage(login_window)
            login_window.protocol("WM_DELETE_WINDOW", lambda: self.on_login_close(login_window))
            login_window.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open login page: {str(e)}")
            self.root.deiconify() 

    def on_login_close(self, login_window):
        login_window.destroy()
        self.root.deiconify() 

if __name__ == "__main__":
    root = Tk()
    app = MainPage(root)
    root.mainloop()