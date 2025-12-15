import tkinter as tk
import random
import json
from PIL import Image, ImageTk
from tkinter import messagebox


# edit belum fiks 
# ==========================
# DATA KUIS (0= a, 1=b, 2=c 3=d)
# ===========================

def load_questions_from_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def save_questions_to_file(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

questions = load_questions_from_file("questions.txt")

# ===========================
# GUI QUIZ
# ===========================
class HeroQuizApp:
    def __init__(self, root):
        self.root = root
        root.title("Quiz Pahlawan")
        root.geometry("960x540")
        root.configure(bg="#ff623b")

        self.score = 0
        self.q_index = 0

        self.create_home()
        self.root.bind("<Configure>", self.resize_background)

    def place_background(self):
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.bg_canvas = self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

    # ===========================
    # HALAMAN HOME
    # ===========================
    def create_home(self):
        self.clear()

        self.bg_image = Image.open("background_kuis_pahlawan.jpg")
        self.place_background()

        # Tombol Mulai
        self.start_btn = tk.Button(
            self.root, text="Mulai",
            font=("Arial", 20, "bold"),
            bg="#ff623b", fg="white",
            width=10, command=self.start_quiz
        )

        self.btn_window = self.canvas.create_window(
            self.canvas.winfo_width() // 2,
            int(self.canvas.winfo_height() * 0.7),
            window=self.start_btn
        )

        # Tombol Kelola Soal
        self.manage_btn = tk.Button(
            self.root, text="Kelola Soal",
            font=("Arial", 14, "bold"),
            bg="red", fg="#f2b80b",
            width=12, command=self.manage_questions
        )

        self.manage_window = self.canvas.create_window(
            self.canvas.winfo_width() // 2,
            int(self.canvas.winfo_height() * 0.85),
            window=self.manage_btn
        )

    def resize_background(self, event):
        if not hasattr(self, "canvas"):
            return

        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w < 10 or h < 10:
            return

        resized = self.bg_image.resize((w, h), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(resized)
        self.canvas.itemconfig(self.bg_canvas, image=self.bg_photo)

        if hasattr(self, "btn_window"):
            self.canvas.coords(self.btn_window, w // 2, int(h * 0.7))

        if hasattr(self, "manage_window"):
            self.canvas.coords(self.manage_window, w // 2, int(h * 0.85))

    # ===========================
    # KELOLA SOAL (TAMBAH & HAPUS)
    # ===========================
    def manage_questions(self):
        win = tk.Toplevel(self.root)
        win.title("Kelola Soal")
        win.geometry("750x550")

        data = load_questions_from_file("questions.txt")

        listbox = tk.Listbox(win, width=100)
        listbox.pack(pady=10)

        def refresh():
            listbox.delete(0, tk.END)
            for i, q in enumerate(data):
                listbox.insert(tk.END, f"{i+1}. {q['question']}")

        refresh()

        frame = tk.Frame(win)
        frame.pack(pady=10)

        q_entry = tk.Entry(frame, width=100)
        q_entry.pack(pady=3)
        q_entry.insert(0, "Tulis pertanyaan")

        opt_entries = []
        for i in range(4):
            e = tk.Entry(frame, width=100)
            e.pack(pady=2)
            e.insert(0, f"Opsi {i}")
            opt_entries.append(e)

        ans_var = tk.IntVar(value=0)
        tk.Label(frame, text="Jawaban Benar (0-3)").pack()
        tk.Entry(frame, textvariable=ans_var).pack()

        def add_question():
            data.append({
                "question": q_entry.get(),
                "options": [e.get() for e in opt_entries],
                "answer": ans_var.get()
            })
            save_questions_to_file("questions.txt", data)
            refresh()
            messagebox.showinfo("Sukses", "Soal berhasil ditambahkan")

        def delete_question():
            idx = listbox.curselection()
            if not idx:
                messagebox.showwarning("Pilih Soal", "Pilih soal dulu")
                return
            del data[idx[0]]
            save_questions_to_file("questions.txt", data)
            refresh()
            messagebox.showinfo("Sukses", "Soal berhasil dihapus")

        tk.Button(win, text="Tambah Soal", bg="#4CAF50",
                  fg="white", width=25, command=add_question).pack(pady=5)

        tk.Button(win, text="Hapus Soal", bg="#f44336",
                  fg="white", width=25, command=delete_question).pack(pady=5)

    # ===========================
    # MULAI KUIS
    # ===========================
    def start_quiz(self):
        global questions
        questions = load_questions_from_file("questions.txt")
        self.score = 0
        self.q_index = 0
        self.quiz_questions = random.sample(questions, 10)
        self.show_question()

    # ===========================
    # TAMPILAN SOAL
    # ===========================
    def show_question(self):
        self.clear()
        self.bg_image = Image.open("bg_kuis.jpg")
        self.place_background()

        q = self.quiz_questions[self.q_index]

        frame = tk.Frame(self.root, bg="#ff623b")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=600, height=500)

        tk.Label(
            frame,
            text=f"Pertanyaan {self.q_index + 1}\n\n{q['question']}",
            bg="white", font=("Arial", 18, "bold"),
            wraplength=550
        ).pack(pady=20)

        for i, opt in enumerate(q["options"]):
            tk.Button(
                frame, text=opt,
                font=("Arial", 14), width=40,
                command=lambda i=i: self.check_answer(i)
            ).pack(pady=6)

    def check_answer(self, selected):
        if selected == self.quiz_questions[self.q_index]["answer"]:
            self.score += 1
            messagebox.showinfo("Benar", "Jawaban benar!")
        else:
            messagebox.showerror("Salah", "Jawaban salah!")

        self.q_index += 1
        if self.q_index < len(self.quiz_questions):
            self.show_question()
        else:
            self.show_result()

    def show_result(self):
        self.clear()
        self.bg_image = Image.open("bg_kuis.jpg")
        self.place_background()

        frame = tk.Frame(self.root, bg="#ff623b")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=300)

        tk.Label(frame, text="Quiz Selesai",
                 font=("Arial", 26, "bold")).pack(pady=20)

        tk.Label(frame, text=f"Skor: {self.score}",
                 font=("Arial", 20)).pack(pady=10)

        tk.Button(frame, text="Home",
                  command=self.create_home).pack(pady=10)

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# ===========================
# JALANKAN APLIKASI
# ===========================
root = tk.Tk()
app = HeroQuizApp(root)
root.mainloop()
