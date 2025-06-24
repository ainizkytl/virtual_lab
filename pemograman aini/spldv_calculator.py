
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
