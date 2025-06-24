# virtual_lab.py
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SPLDVLab:
    def __init__(self, master):
        self.fig, self.ax = plt.subplots(figsize=(6, 6)) # Ukuran plot lebih baik
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.axvline(0, color='gray', linestyle='--')
        self.ax.axhline(0, color='gray', linestyle='--')
        self.ax.grid(True)
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_aspect('equal', adjustable='box') # Pastikan skala sumbu sama
        self.line1, = self.ax.plot([], [], label='Persamaan 1', color='blue', linewidth=2)
        self.line2, = self.ax.plot([], [], label='Persamaan 2', color='red', linewidth=2)
        self.intersection_point, = self.ax.plot([], [], 'o', color='green', markersize=10, label='Solusi')
        self.ax.legend()

        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.status_label = ttk.Label(master, text="Status: Masukkan koefisien di bawah")
        self.status_label.pack(pady=5)

    def plot_equation(self, a, b, c, line):
        x_min, x_max = self.ax.get_xlim()
        y_min, y_max = self.ax.get_ylim()

        if b == 0:
            if a != 0:
                # Garis vertikal: ax = c => x = c/a
                x_val = c / a
                # Gambar dari y_min ke y_max untuk mencakup seluruh area plot
                line.set_data([x_val, x_val], [y_min, y_max])
            else: # a=0, b=0: tidak valid atau tak hingga solusi (bukan garis tunggal)
                line.set_data([], [])
        else:
            # y = (c - ax) / b
            x_vals = np.linspace(x_min, x_max, 500)
            y_vals = (c - a * x_vals) / b
            
            # Hanya tampilkan bagian garis yang ada di dalam batas plot
            valid_indices = np.where((y_vals >= y_min) & (y_vals <= y_max))
            line.set_data(x_vals[valid_indices], y_vals[valid_indices])
        
        self.canvas.draw_idle()

    def find_intersection(self, a1, b1, c1, a2, b2, c2):
        det = a1 * b2 - a2 * b1
        
        if det == 0:
            # Garis sejajar atau berimpit
            # Periksa apakah mereka berimpit (solusi tak hingga)
            # Jika a1/a2 = b1/b2 = c1/c2 (dengan asumsi a2,b2,c2 tidak nol)
            # Atau periksa konsistensi menggunakan determinan minor
            
            # Untuk kasus sejajar/berimpit, gunakan metode pemeriksaan konsistensi
            # Jika a1,b1,c1 dan a2,b2,c2 proporsional, maka berimpit
            # (a1/a2 = b1/b2 = c1/c2) --> cek silang: a1*b2 = a2*b1, a1*c2 = a2*c1, b1*c2 = b2*c1
            
            # Penanganan kasus khusus: semua koefisien nol
            if (a1 == 0 and b1 == 0 and c1 == 0) and (a2 == 0 and b2 == 0 and c2 == 0):
                 return "Infinite Solutions" # Kedua persamaan 0=0
            
            # Jika determinan nol, periksa apakah mereka konsisten (berimpit)
            # Caranya: Ambil satu titik dari garis pertama, cek apakah memenuhi garis kedua
            # Atau lebih robust: cek proporsionalitas
            is_consistent = False
            # Menghindari ZeroDivisionError
            if (a1 == 0 and b1 == 0 and c1 != 0) or \
               (a2 == 0 and b2 == 0 and c2 != 0):
                # Salah satu persamaan menyatakan 0 = non-nol (tidak konsisten)
                is_consistent = False
            elif det == 0: # Ini sudah ditangani di awal, tapi pastikan
                # Jika sejajar, cek apakah mereka konsisten (berimpit)
                # Contoh: x+y=1, 2x+2y=2 (berimpit) vs x+y=1, 2x+2y=3 (sejajar, tidak ada solusi)
                # Cek jika a1*c2 == a2*c1 dan b1*c2 == b2*c1
                # Ini adalah cek apakah matriks augmentasinya memiliki rank yang sama dengan matriks koefisien
                # atau jika barisnya proporsional
                if (a1 * c2 == a2 * c1 and b1 * c2 == b2 * c1) or \
                   (a1 == 0 and a2 == 0 and b1 * c2 == b2 * c1) or \
                   (b1 == 0 and b2 == 0 and a1 * c2 == a2 * c1):
                    # Jika a1, b1, a2, b2 semuanya nol, ini kasus 0=c1 dan 0=c2
                    if a1 == 0 and b1 == 0 and a2 == 0 and b2 == 0:
                        if c1 == c2: return "Infinite Solutions"
                        else: return "No Solution"
                    is_consistent = True
                
            if is_consistent:
                return "Infinite Solutions"
            else:
                return "No Solution"
        else:
            x = (c1 * b2 - c2 * b1) / det
            y = (a1 * c2 - a2 * c1) / det
            return x, y

    def update_plot(self, a1, b1, c1, a2, b2, c2):
        self.plot_equation(a1, b1, c1, self.line1)
        self.plot_equation(a2, b2, c2, self.line2)

        solution = self.find_intersection(a1, b1, c1, a2, b2, c2)
        if isinstance(solution, tuple):
            x_sol, y_sol = solution
            # Filter agar titik solusi hanya muncul jika di dalam rentang plot
            x_min, x_max = self.ax.get_xlim()
            y_min, y_max = self.ax.get_ylim()
            if x_min <= x_sol <= x_max and y_min <= y_sol <= y_max:
                self.intersection_point.set_data([x_sol], [y_sol])
                self.status_label.config(text=f"Solusi Unik: x = {x_sol:.2f}, y = {y_sol:.2f}")
            else:
                self.intersection_point.set_data([], [])
                self.status_label.config(text=f"Solusi Unik (di luar area grafik): x = {x_sol:.2f}, y = {y_sol:.2f}")
        else:
            self.intersection_point.set_data([], [])
            self.status_label.config(text=f"Status: {solution}")
        
        self.canvas.draw_idle()


def create_gui():
    root = tk.Tk()
    root.title("Virtual Lab SPLDV Interaktif")
    root.geometry("800x700") # Ukuran jendela awal

    lab = SPLDVLab(root)

    # Fungsi untuk mendapatkan nilai dari slider/entry dan update plot
    def update_from_gui(*args): # *args agar bisa dipanggil oleh scale event
        try:
            a1 = float(slider_a1.get())
            b1 = float(slider_b1.get())
            c1 = float(slider_c1.get())
            a2 = float(slider_a2.get())
            b2 = float(slider_b2.get())
            c2 = float(slider_c2.get())
            lab.update_plot(a1, b1, c1, a2, b2, c2)
        except ValueError:
            lab.status_label.config(text="Input tidak valid! Pastikan semua adalah angka.")

    # --- Frame Kontrol ---
    control_frame = ttk.Frame(root)
    control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

    # Frame untuk Persamaan 1
    frame1 = ttk.LabelFrame(control_frame, text="Persamaan 1 (a₁x + b₁y = c₁)")
    frame1.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    tk.Label(frame1, text="a₁:").grid(row=0, column=0, padx=5, pady=2)
    slider_a1 = ttk.Scale(frame1, from_=-5, to=5, orient="horizontal", command=update_from_gui)
    slider_a1.set(1) # Default value
    slider_a1.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

    tk.Label(frame1, text="b₁:").grid(row=1, column=0, padx=5, pady=2)
    slider_b1 = ttk.Scale(frame1, from_=-5, to=5, orient="horizontal", command=update_from_gui)
    slider_b1.set(-1) # Default value
    slider_b1.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

    tk.Label(frame1, text="c₁:").grid(row=2, column=0, padx=5, pady=2)
    slider_c1 = ttk.Scale(frame1, from_=-5, to=5, orient="horizontal", command=update_from_gui)
    slider_c1.set(0) # Default value
    slider_c1.grid(row=2, column=1, padx=5, pady=2, sticky="ew")

    frame1.grid_columnconfigure(1, weight=1) # Membuat slider melebar

    # Frame untuk Persamaan 2
    frame2 = ttk.LabelFrame(control_frame, text="Persamaan 2 (a₂x + b₂y = c₂)")
    frame2.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    tk.Label(frame2, text="a₂:").grid(row=0, column=0, padx=5, pady=2)
    slider_a2 = ttk.Scale(frame2, from_=-5, to=5, orient="horizontal", command=update_from_gui)
    slider_a2.set(1) # Default value
    slider_a2.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

    tk.Label(frame2, text="b₂:").grid(row=1, column=0, padx=5, pady=2)
    slider_b2 = ttk.Scale(frame2, from_=-5, to=5, orient="horizontal", command=update_from_gui)
    slider_b2.set(1) # Default value
    slider_b2.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

    tk.Label(frame2, text="c₂:").grid(row=2, column=0, padx=5, pady=2)
    slider_c2 = ttk.Scale(frame2, from_=-5, to=5, orient="horizontal", command=update_from_gui)
    slider_c2.set(2) # Default value
    slider_c2.grid(row=2, column=1, padx=5, pady=2, sticky="ew")

    frame2.grid_columnconfigure(1, weight=1) # Membuat slider melebar

    control_frame.grid_columnconfigure(0, weight=1)
    control_frame.grid_columnconfigure(1, weight=1)

    # Inisialisasi plot awal
    update_from_gui()

    root.mainloop()

if __name__ == "__main__":
    create_gui()
