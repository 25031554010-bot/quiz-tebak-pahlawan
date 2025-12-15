# quiz-tebak-pahlawan
Game Quis Tebak Pahlawan

Kode Berisi: 
Tampilan GUI menggunakan Tkinter
Background gambar otomatis menyesuaikan ukuran layar (responsive)
Soal pilihan ganda tentang pahlawan Indonesia
Mengambil 10 soal secara acak dari total soal yang tersedia
Tombol interaktif (Mulai, Jawab, Play Again, Exit)
Gambar soal bisa diklik untuk zoom
Perhitungan skor otomatis

Folder Berisi: 
quiz-tebak-pahlawan/
│
├── kuis.py # File utama aplikasi
├── questions.txt # Data soal (format JSON)
├── background_kuis_pahlawan.jpg # Background halaman awal
├── bg_kuis.jpg # Background halaman soal & hasil
└── README.md # Dokumentasi proyek

Teknologi yang digunakan:
Python 3.10+ (disarankan)
Tkinter (GUI)
Pillow (PIL) untuk pengolahan gambar
JSON untuk penyimpanan data soal

Cara menjalankan:
Pastikan Python sudah terinstall
Install library Pillow jika belum ada: Terminal (pip install pillow)
run python kuis_fiks.py

format pertanyaan: 
[
{
"question": "Pahlawan yang dikenal sebagai \"Ayam Jantan dari Timur\" adalah…",
"options": [
"A. Sultan Hasanuddin",
"B. Pattimura",
"C. Cut Nyak Meutia",
"D. Pangeran Antasari"
],
"answer": 0,
"image": "hasanuddin.jpg"
}
]

Note: 
Gunakan kutip lurus (" "), bukan kutip miring (“ ”)
Jika ada tanda petik di dalam teks, gunakan escape: \"
Jangan gunakan \ tunggal (harus \\ jika perlu)