import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def solve_spldv(a1, b1, c1, a2, b2, c2):
    """Menyelesaikan SPLDV menggunakan metode Cramer."""
    determinan = a1 * b2 - a2 * b1
    if determinan == 0:
        # Check for consistent (infinite solutions) or inconsistent (no solutions)
        if (c1 * b2 - c2 * b1 == 0) and (a1 * c2 - a2 * c1 == 0):
            return None, None, "Sistem memiliki tak hingga solusi (garis berhimpit)."
        else:
            return None, None, "Sistem tidak memiliki solusi (garis sejajar)."
    else:
        dx = c1 * b2 - c2 * b1
        dy = a1 * c2 - a2 * c1
        x = dx / determinan
        y = dy / determinan
        return x, y, None

def plot_spldv(a1, b1, c1, a2, b2, c2, x_sol, y_sol):
    """Membuat plot kedua persamaan linear."""
    fig, ax = plt.subplots(figsize=(8, 6))
    x = np.linspace(-10, 10, 400) # Rentang nilai x

    # Plot Persamaan 1: a1x + b1y = c1 => y = (c1 - a1x) / b1
    if b1 != 0:
        y1 = (c1 - a1 * x) / b1
        ax.plot(x, y1, label=f'{a1}x + {b1}y = {c1}', color='blue')
    elif a1 != 0: # vertical line x = c1/a1
        ax.axvline(x=c1/a1, label=f'{a1}x = {c1}', color='blue')
    
    # Plot Persamaan 2: a2x + b2y = c2 => y = (c2 - a2x) / b2
    if b2 != 0:
        y2 = (c2 - a2 * x) / b2
        ax.plot(x, y2, label=f'{a2}x + {b2}y = {c2}', color='red')
    elif a2 != 0: # vertical line x = c2/a2
        ax.axvline(x=c2/a2, label=f'{a2}x = {c2}', color='red')

    # Plot solusi jika ada
    if x_sol is not None and y_sol is not None:
        ax.plot(x_sol, y_sol, 'o', color='green', markersize=10, label=f'Solusi: ({x_sol:.2f}, {y_sol:.2f})')
        ax.annotate(f'({x_sol:.2f}, {y_sol:.2f})', (x_sol, y_sol), textcoords="offset points", xytext=(5,5), ha='center')

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Grafik Sistem Persamaan Linear Dua Variabel')
    ax.grid(True)
    ax.legend()
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_xlim(min(x_sol - 5, -10) if x_sol is not None else -10, max(x_sol + 5, 10) if x_sol is not None else 10)
    ax.set_ylim(min(y_sol - 5, -10) if y_sol is not None else -10, max(y_sol + 5, 10) if y_sol is not None else 10)
    return fig

st.set_page_config(layout="wide", page_title="Kalkulator SPLDV Interaktif")

st.title("Kalkulator SPLDV Interaktif dengan Visualisasi & Discovery Learning 🚀")
st.markdown("""
Selamat datang di alat bantu belajar SPLDV! Di sini kamu akan **menjelajahi** bagaimana menemukan solusi sistem persamaan linear dua variabel.
Kita akan gunakan metode **eliminasi** dan **visualisasi grafik** untuk membantumu memahami konsepnya.
""")

---

## Langkah 1: Masukkan Persamaan SPLDV

st.markdown("""
Bentuk umum SPLDV adalah:
$a_1x + b_1y = c_1$
$a_2x + b_2y = c_2$

Masukkan koefisiennya di bawah ini:
""")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Persamaan 1")
    a1 = st.number_input("Koefisien a1", value=1.0, key="a1")
    b1 = st.number_input("Koefisien b1", value=1.0, key="b1")
    c1 = st.number_input("Konstanta c1", value=5.0, key="c1")

with col2:
    st.subheader("Persamaan 2")
    a2 = st.number_input("Koefisien a2", value=2.0, key="a2")
    b2 = st.number_input("Koefisien b2", value=1.0, key="b2")
    c2 = st.number_input("Konstanta c2", value=7.0, key="c2")

st.markdown(f"**Persamaan Anda:**\n1) `{a1}x + {b1}y = {c1}`\n2) `{a2}x + {b2}y = {c2}`")

x_sol_auto, y_sol_auto, error_msg_auto = solve_spldv(a1, b1, c1, a2, b2, c2)
if x_sol_auto is not None and y_sol_auto is not None:
    st.pyplot(plot_spldv(a1, b1, c1, a2, b2, c2, x_sol_auto, y_sol_auto))
elif error_msg_auto:
    st.warning(f"**Info Grafik:** {error_msg_auto}")
    st.pyplot(plot_spldv(a1, b1, c1, a2, b2, c2, None, None)) # Plot without solution point
else:
    st.warning("Masukkan koefisien untuk melihat grafik.")

---

## Langkah 2: Pahami Konsep Eliminasi

st.markdown("""
**Apa itu Eliminasi?**
Eliminasi berarti **menghilangkan** salah satu variabel (baik $x$ atau $y$) dari sistem persamaan. Caranya adalah dengan membuat koefisien variabel tersebut **sama besar** (atau berlawanan tanda) di kedua persamaan, lalu kita bisa mengurangkan atau menjumlahkan kedua persamaan tersebut. Hasilnya, kita akan mendapatkan persamaan baru yang hanya punya satu variabel, dan ini mudah diselesaikan!
""")

---

## Langkah 3: Mari Eliminasi!

st.markdown("""
Pilih variabel yang ingin kamu eliminasi terlebih dahulu:
""")
elim_var = st.radio("Saya ingin mengeliminasi:", ("x", "y"))

if elim_var == "x":
    st.info("💡 **Tujuan:** Buat koefisien $x$ sama besar di kedua persamaan.")
    
    st.markdown(f"Untuk membuat koefisien **x** sama,
