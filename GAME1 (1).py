from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from tkinter.messagebox import showinfo

# Ini adalah Push Pertama 
# Ini adalah Push Kedua 

class Start:
    def __init__(self, root):
        self.root = root
        self.root.title("GAME Quiz")
        self.root.geometry('300x320')

        Label(self.root, text="Click Here!").grid(row=0, column=3)
        Label(self.root, text="↓").grid(row=1, column=3)

        self.button1 = Button(
            self.root,
            text="Let's Start!",
            width=13,
            height=5,
            bg="yellow",
            fg='green',
            font=("Tahoma", 30),
            command=self.tutup   # Fix di sini (tanpa ())
        )
        self.button1.grid(row=2, column=3)

    def tutup(self):
        self.root.destroy()
        Quiz()  # buka quiz


class Quiz:
    def __init__(self):
        self.root = tk.Tk()   # buat window baru
        self.root.title("GAME Quiz")
        self.root.geometry('1000x900')

        Label(self.root, text="Masukkan Foto Pahlawan",background='light blue').grid(row=1, column=3)

        self.button1 = Button(
            self.root,
            text="Close Game",
            width=13,
            height=5,
            bg="yellow",
            fg='green',
            font=("Tahoma", 30),
            command=self.root.destroy,
        )
        self.button1.grid(row=20, column=3)

        self.root.mainloop()   # penting!


if __name__ == "__main__":
    root = tk.Tk()
    Start(root)
    root.mainloop()
