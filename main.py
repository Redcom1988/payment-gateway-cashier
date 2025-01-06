__author__ = 'Kelompok 6 - D'
'1. Made Arief Budi Dharma (2308561034)'
'2. Adika Setyadharma Susilo (2308561088)'
'3. I Gusti Nyoman Pramajaya (230856109)'
'4. I Gede Rama Yasa Mahendra (2308561016)'
import os
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw

def round_corners(image, radius):
    mask = Image.new("L", image.size, 1)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0) + image.size, radius, fill=255)
    image.putalpha(mask)
    return image

main = Tk()
main.geometry("1366x768")
main.title("Aplikasi Belanja Online")
main.resizable(0, 0)

def Exit():
    sure = messagebox.askyesno("Exit","Are you sure you want to exit?", parent=main)
    if sure == True:
        main.destroy()
        
main.protocol("WM_DELETE_WINDOW", Exit)

def emp():
    main.withdraw()
    os.system("python employee.py")
    main.deiconify()

def adm():
    main.withdraw()
    os.system("python admin.py")
    main.deiconify()

label1 = Label(main)
label1.place(relx=0, rely=0, width=1366, height=768)
img = PhotoImage(file="./images/main.png")
label1.configure(image=img)

image1 = Image.open("./images/1.png")
image1 = round_corners(image1, 40) 
img2 = ImageTk.PhotoImage(image1)

button1 = Button(main)
button1.place(relx=0.316, rely=0.446, width=146, height=120)
button1.configure(relief="flat")
button1.configure(overrelief="flat")
button1.configure(activebackground="#ffffff")
button1.configure(cursor="hand2")
button1.configure(foreground="#ffffff")
button1.configure(background="#ffffff")
button1.configure(borderwidth="0")
button1.configure(image=img2)
button1.configure(command=emp)


image2 = Image.open("./images/2.png")
image2 = round_corners(image2, 40)  
img3 = ImageTk.PhotoImage(image2)

button2 = Button(main)
button2.place(relx=0.566, rely=0.448, width=146, height=120)
button2.configure(relief="flat")
button2.configure(overrelief="flat")
button2.configure(activebackground="#ffffff")
button2.configure(cursor="hand2")
button2.configure(foreground="#ffffff")
button2.configure(background="#ffffff")
button2.configure(borderwidth="0")
button2.configure(image=img3)
button2.configure(command=adm)

main.mainloop()
