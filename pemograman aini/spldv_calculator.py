import streamlit as st
import numpy as np # Masih digunakan untuk linspace jika diperlukan untuk perhitungan, tapi tidak untuk plotting
from sympy import symbols, Eq, solve, sympify

# Mengatur konfigurasi halaman Streamlit
st.set_page_config(page_title="Kalkulator SPLDV", layout="centered")
st.title("📊 Kalkulator SPLDV") # Judul diperbarui
st.write("Masukkan dua persamaan linear dua variabel dalam bentuk seperti `2*x + 3*y - 6 = 0`")

# Input pengguna untuk persamaan
pers1_input = st.text_input("Persamaan 1", value="2*x + 3*y - 6 = 0")
pers2_input = st.text_input("Persamaan 2", value="x - y - 1 = 0")

# Mendefinisikan simbol x dan y untuk SymPy
x, y = symbols('x y')

try:
    # Menguraikan input persamaan menjadi objek SymPy Eq (Equation)
    pers1 = Eq(*map(sympify, pers1_input.split("=")))
    pers2 = Eq(*map(sympify, pers2_input.split("=")))

    # Menyelesaikan sistem persamaan
    solusi = solve((pers1, pers2), (x, y), dict=True)

    st.subheader("📌 Solusi SPLDV:")
    if solusi:
        # Menampilkan solusi tunggal jika ada
        st.success(f"x = {solusi[0][x]}, y = {solusi[0][y]}")
        jenis = "Satu solusi (garis berpotongan)"
    else:
        # Menentukan jenis solusi (tak hingga atau tidak ada) jika tidak ada solusi tunggal
        # Untuk menentukan jenis, kita perlu menganalisis koefisien dan konstanta
        # Mengambil koefisien dan konstanta dari kedua persamaan
        # Bentuk umum Ax + By + C = 0
        # Jadi, dari Eq(LHS, RHS), kita ubah menjadi LHS - RHS = 0
        # A = coeff(x), B = coeff(y), C = -RHS
        koef1_x = pers1.lhs.coeff(x)
        koef1_y = pers1.lhs.coeff(y)
        konst1 = -pers1.rhs

        koef2_x = pers2.lhs.coeff(x)
        koef2_y = pers2.lhs.coeff(y)
        konst2 = -pers2.rhs

        # Menghindari ZeroDivisionError
        # Cek apakah rasio koefisien sama
        # a1/a2 = b1/b2 = c1/c2 -> tak hingga solusi (berhimpit)
        # a1/a2 = b1/b2 != c1/c2 -> tidak ada solusi (sejajar)
        
        # Menggunakan epsilon untuk perbandingan float
        epsilon = 1e-9

        rasio_x = koef1_x / koef2_x if koef2_x != 0 else None
        rasio_y = koef1_y / koef2_y if koef2_y != 0 else None
        rasio_konst = konst1 / konst2 if konst2 != 0 else None

        # Handle kasus di mana salah satu koefisien adalah nol
        # Misalnya, persamaan seperti y = 5 atau x = 3
        
        is_parallel_coeffs = False
        is_same_line = False

        if rasio_x is not None and rasio_y is not None:
            if abs(rasio_x - rasio_y) < epsilon:
                is_parallel_coeffs = True
                if rasio_konst is not None and abs(rasio_x - rasio_konst) < epsilon:
                    is_same_line = True
        elif (koef2_x == 0 and koef1_x == 0) and (koef2_y != 0 and koef1_y != 0): # Kedua garis vertikal
            if abs(koef1_y / koef2_y - konst1 / konst2) < epsilon:
                is_same_line = True
            is_parallel_coeffs = True # Keduanya vertikal, jadi sejajar
        elif (koef2_y == 0 and koef1_y == 0) and (koef2_x != 0 and koef1_x != 0): # Kedua garis horizontal
            if abs(koef1_x / koef2_x - konst1 / konst2) < epsilon:
                is_same_line = True
            is_parallel_coeffs = True # Keduanya horizontal, jadi sejajar

        if is_same_line:
            jenis = "Tak hingga solusi (garis berhimpit)"
        elif is_parallel_coeffs and not is_same_line:
            jenis = "Tidak ada solusi (garis sejajar)"
        else:
            jenis = "Tidak diketahui (kemungkinan ada kesalahan input atau kasus khusus)"
            
        st.warning("SPLDV tidak memiliki solusi tunggal.")

    st.write(f"**Jenis solusi:** {jenis}")

    st.info("Visualisasi grafik tidak tersedia karena `matplotlib` telah dihapus dari kode.")

except Exception as e:
    # Menangani kesalahan yang mungkin terjadi selama eksekusi
    st.error(f"Terjadi kesalahan: {e}")
    st.error("Pastikan format persamaan benar, contoh: `2*x + 3*y - 6 = 0`.")
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, Eq, solve, sympify

st.set_page_config(page_title="Kalkulator SPLDV", layout="centered")
st.title("📊 Kalkulator SPLDV dengan Grafik Interaktif")
st.write("Masukkan dua persamaan linear dua variabel dalam bentuk seperti `2*x + 3*y - 6 = 0`")

# Input pengguna
pers1_input = st.text_input("Persamaan 1", value="2*x + 3*y - 6 = 0")
pers2_input = st.text_input("Persamaan 2", value="x - y - 1 = 0")

x, y = symbols('x y')

try:
    pers1 = Eq(*map(sympify, pers1_input.split("=")))
    pers2 = Eq(*map(sympify, pers2_input.split("=")))

    solusi = solve((pers1, pers2), (x, y), dict=True)

    st.subheader("📌 Solusi SPLDV:")
    if solusi:
        st.success(f"x = {solusi[0][x]}, y = {solusi[0][y]}")
        titik_potong = (float(solusi[0][x]), float(solusi[0][y]))
        jenis = "Satu solusi (garis berpotongan)"
    else:
        koef1 = [pers1.lhs.coeff(x), pers1.lhs.coeff(y), -pers1.rhs]
        koef2 = [pers2.lhs.coeff(x), pers2.lhs.coeff(y), -pers2.rhs]
        rasio = [k1/k2 if k2 != 0 else None for k1, k2 in zip(koef1, koef2)]
        if rasio[0] == rasio[1] == rasio[2]:
            jenis = "Tak hingga solusi (garis berhimpit)"
        elif rasio[0] == rasio[1] and rasio[2] != rasio[1]:
            jenis = "Tidak ada solusi (garis sejajar)"
        else:
            jenis = "Tidak diketahui"
        st.warning("SPLDV tidak memiliki solusi tunggal.")
        titik_potong = None

    st.write(f"**Jenis solusi:** {jenis}")

    st.subheader("📉 Visualisasi Grafik")
    fig, ax = plt.subplots()
    x_vals = np.linspace(-10, 10, 400)

    def garis_y(expr):
        solved_y = solve(expr, y)
        if solved_y:
            return [float(s.evalf(subs={x: val})) for val in x_vals]
        else:
            return [None] * len(x_vals)

    y1_vals = garis_y(pers1)
    y2_vals = garis_y(pers2)

    ax.plot(x_vals, y1_vals, label='Persamaan 1', color='blue')
    ax.plot(x_vals, y2_vals, label='Persamaan 2', color='green')

    if titik_potong:
        ax.plot(*titik_potong, 'ro', label='Titik Potong')

    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(True)
    ax.legend()
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Grafik SPLDV")

    st.pyplot(fig)

except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
