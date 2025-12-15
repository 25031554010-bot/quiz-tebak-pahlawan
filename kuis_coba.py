import tkinter as tk
import random
import json
from PIL import Image, ImageTk
from tkinter import messagebox
# ===========================
# DATA KUIS (0= a, 1=b, 2=c 3=d)
# ===========================

def load_questions_from_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

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
        """Menambahkan canvas + background image ke halaman apapun"""
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.bg_canvas = self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")


    # ===========================
    # HALAMAN HOME
    # ===========================
    def create_home(self):
        self.clear()

        # ===========================
        # LOAD BACKGROUND GAMBAR
        # ===========================
        self.bg_image = Image.open("background_kuis_pahlawan.jpg")   # <-- GANTI NAMA FILE DI SINI
        self.original_bg = self.bg_image.copy()
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.place_background()
        
        # ===========================
        # TOMBOL MULAI DI TENGAH BANNER
        # ===========================
        self.start_btn = tk.Button(self.root, text="Mulai",
                                font=("Arial", 20, "bold"),
                                bg="#ff623b", fg="white",
                                width=10, command=self.start_quiz)

        # letakkan tombol di tengah window (nanti direposisi otomatis pas resize)
        self.btn_window = self.canvas.create_window(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2,
            window=self.start_btn
        )

    def resize_background(self, event):
        # Jika canvas tidak ada (halaman sudah berpindah), hentikan
        if not hasattr(self, "canvas") or not self.canvas.winfo_exists():
            return

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width < 10 or canvas_height < 10:
            return

        # Resize dengan ukuran canvas agar background selalu full screen
        resized = self.bg_image.resize((canvas_width, canvas_height), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(resized)
        self.canvas.itemconfig(self.bg_canvas, image=self.bg_photo)
    
        # Reposisi tombol mengikuti ukuran canvas
        if hasattr(self, "btn_window"):
            self.canvas.coords(
                self.btn_window,
                canvas_width // 2,           # posisi X tengah
                int(canvas_height * 0.71)    # posisi Y → sesuaikan supaya pas dengan banner
            )

    def show_zoom_image(self, img_path):
        # Buat overlay transparan
        overlay = tk.Toplevel(self.root)
        overlay.attributes("-topmost", True)
        overlay.geometry(f"{self.root.winfo_width()}x{self.root.winfo_height()}+{self.root.winfo_rootx()}+{self.root.winfo_rooty()}")
        overlay.configure(bg="black")  # hitam solid (aman di Tkinter)
        overlay.overrideredirect(True)  # hilangkan frame window

        # Load gambar besar
        big_img = Image.open(img_path)
        # Resize proporsional agar pas layar
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        ratio = min(screen_w / big_img.width, screen_h / big_img.height)
        new_w = int(big_img.width * ratio * 0.8)
        new_h = int(big_img.height * ratio * 0.8)
        
        big_img = big_img.resize((new_w, new_h), Image.LANCZOS)
        self.big_photo = ImageTk.PhotoImage(big_img)

        # Gambar besar di tengah
        img_label = tk.Label(overlay, image=self.big_photo, bg="#000")
        img_label.place(relx=0.5, rely=0.5, anchor="center")

        # Tutup overlay jika klik di luar gambar
        def close_overlay(event):
            overlay.destroy()

        overlay.bind("<Button-1>", close_overlay)
        img_label.bind("<Button-1>", lambda e: None)  # blok klik pada gambar agar tidak menutup
        
    # ===========================
    # MULAI KUIS
    # ===========================
    def start_quiz(self):
        self.score = 0
        self.q_index = 0
        random.shuffle(questions)
        self.show_question()

    # ===========================
    # TAMPILAN SOAL
    # ===========================
    def show_question(self):
        self.clear()
        self.bg_image = Image.open("bg_kuis.jpg")
        self.place_background()

        q = questions[self.q_index]

        frame = tk.Frame(self.root, bg="#ff623b")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=600, height=500)
        
        # ---------------------------
        # TAMPILKAN GAMBAR JIKA ADA
        # ---------------------------
        if "image" in q:
            img = Image.open(q["image"])
            img = img.resize((150, 100))
            self.q_photo = ImageTk.PhotoImage(img)

            img_label = tk.Label(frame, image=self.q_photo, bg="white", cursor="hand2")
            img_label.pack(pady=10)

            # Klik gambar untuk zoom
            img_label.bind("<Button-1>", lambda e, path=q["image"]: self.show_zoom_image(path))

        q_label = tk.Label(frame, text=f"Pertanyaan {self.q_index + 1}/{len(questions)}\n\n{q['question']}",
                           bg="white", fg="black",
                           font=("Arial", 18, "bold"), wraplength=600)
        q_label.pack(pady=20)

        for i, opt in enumerate(q["options"]):
            btn = tk.Button(frame, text=opt, bg="white", fg="black",
                            font=("Arial", 14), width=40,
                            command=lambda i=i: self.check_answer(i))
            btn.pack(pady=8)

    # ===========================
    # CEK JAWABAN
    # ===========================
    def check_answer(self, selected):
        correct = questions[self.q_index]["answer"]

        if selected == correct:
            self.score += 1
            messagebox.showinfo("Correct!", "Jawaban kamu benar! 🔥")
        else:
            messagebox.showerror("Wrong!", "Jawaban kamu salah!")

        self.q_index += 1

        if self.q_index < len(questions):
            self.show_question()
        else:
            self.show_result()

    # ===========================
    # HASIL
    # ===========================
    def show_result(self):
        self.clear()
        self.bg_image = Image.open("bg_kuis.jpg")
        self.place_background()

        frame = tk.Frame(self.root, bg="#ff623b")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=650, height=400)

        tk.Label(frame, text="Quiz Complete!",
                 bg="white", fg="black",
                 font=("Arial", 26, "bold")).pack(pady=15)

        tk.Label(frame, text=f"Score: {self.score}/{len(questions)}",
                 bg="white", fg="black",
                 font=("Arial", 22, "bold")).pack(pady=10)

        tk.Label(frame,
                 text="Selamat kamu telah menyelesaikan kuis ini!",
                 bg="white", fg="black",
                 font=("Arial", 14)).pack(pady=10)

        # Tombol Play Again
        tk.Button(frame, text="Play Again",
                  font=("Arial", 14, "bold"),
                  bg="white", fg="#ff623b",
                  width=15, command=self.create_home).pack(pady=20)

        # Tombol Exit
        tk.Button(frame, text="Exit",
                  font=("Arial", 14, "bold"),
                  bg="#ff623b", fg="white",
                  width=15, command=self.root.quit).pack()

    # ===========================
    # HAPUS TAMPILAN DARI WINDOW
    # ===========================
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# JALANKAN APLIKASI
# ===========================
root = tk.Tk()
app = HeroQuizApp(root)
root.mainloop()
