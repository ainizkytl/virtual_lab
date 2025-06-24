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

**Apa itu Eliminasi?**
Eliminasi berarti **menghilangkan** salah satu variabel (baik $x$ atau $y$) dari sistem persamaan. Caranya adalah dengan membuat koefisien variabel tersebut **sama besar** (atau berlawanan tanda) di kedua persamaan, lalu kita bisa mengurangkan atau menjumlahkan kedua persamaan tersebut. Hasilnya, kita akan mendapatkan persamaan baru yang hanya punya satu variabel, dan ini mudah diselesaikan!

---

## Langkah 3: Mari Eliminasi!

Pilih variabel yang ingin kamu eliminasi terlebih dahulu:

elim_var = st.radio("Saya ingin mengeliminasi:", ("x", "y"))

if elim_var == "x":
    st.info("💡 **Tujuan:** Buat koefisien $x$ sama besar di kedua persamaan.")
    
    st.markdown(f"Untuk membuat koefisien **x** sama, kita bisa mengalikan:")
    
    col_elim_x1, col_elim_x2 = st.columns(2)
    with col_elim_x1:
        st.markdown(f"**Persamaan 1 (`{a1}x + {b1}y = {c1}`) akan dikalikan dengan:**")
        # Suggest a common multiple if possible
        if a2 != 0:
            suggested_mult1_x = a2
        else:
            suggested_mult1_x = 1.0 # default
        mult1_x = st.number_input("", value=suggested_mult1_x, key="mult1_x")

    with col_elim_x2:
        st.markdown(f"**Persamaan 2 (`{a2}x + {b2}y = {c2}`) akan dikalikan dengan:**")
        if a1 != 0:
            suggested_mult2_x = a1
        else:
            suggested_mult2_x = 1.0 # default
        mult2_x = st.number_input("", value=suggested_mult2_x, key="mult2_x")

    new_a1 = a1 * mult1_x
    new_b1 = b1 * mult1_x
    new_c1 = c1 * mult1_x

    new_a2 = a2 * mult2_x
    new_b2 = b2 * mult2_x
    new_c2 = c2 * mult2_x

    st.markdown("---")
    st.subheader("Persamaan Setelah Dikali:")
    st.write(f"1') `{new_a1:.2f}x + {new_b1:.2f}y = {new_c1:.2f}`")
    st.write(f"2') `{new_a2:.2f}x + {new_b2:.2f}y = {new_c2:.2f}`")

    st.markdown("Sekarang, perhatikan koefisien $x$. Apa yang harus kamu lakukan untuk **menghilangkan** $x$?")
    
    operation_x = st.radio("Pilih Operasi:", ("Kurangkan (1' - 2')", "Jumlahkan (1' + 2')"))

    if st.button("Lakukan Operasi (Eliminasi x)"):
        if operation_x == "Kurangkan (1' - 2')":
            res_a = new_a1 - new_a2
            res_b = new_b1 - new_b2
            res_c = new_c1 - new_c2
        else: # Jumlahkan
            res_a = new_a1 + new_a2
            res_b = new_b1 + new_b2
            res_c = new_c1 + new_c2

        st.markdown("---")
        st.subheader("Hasil Setelah Eliminasi:")
        st.write(f"`{res_a:.2f}x + {res_b:.2f}y = {res_c:.2f}`")

        if abs(res_a) < 1e-9: # Cek apakah koefisien x mendekati nol
            st.success(f"🎉 **Selamat!** Anda berhasil mengeliminasi 'x'. Sekarang Anda memiliki persamaan satu variabel: `{res_b:.2f}y = {res_c:.2f}`.")
            if res_b != 0:
                found_y = res_c / res_b
                st.write(f"Dari sini, Anda bisa menemukan nilai $y$: $y = {found_y:.2f}$")
                st.session_state['found_y'] = found_y # Simpan nilai y ke session state
                st.info("Sekarang kita punya nilai y! Lanjut ke langkah selanjutnya untuk mencari x.")
            else:
                st.warning("Koefisien y juga nol. Ini berarti sistem memiliki tak hingga solusi atau tidak ada solusi. Coba periksa kembali persamaan atau operasinya.")
        else:
            st.error("❌ **Oops!** Koefisien 'x' belum nol. Coba periksa kembali nilai pengali atau operasi yang Anda pilih.")

elif elim_var == "y":
    st.info("💡 **Tujuan:** Buat koefisien $y$ sama besar di kedua persamaan.")

    st.markdown(f"Untuk membuat koefisien **y** sama, kita bisa mengalikan:")

    col_elim_y1, col_elim_y2 = st.columns(2)
    with col_elim_y1:
        st.markdown(f"**Persamaan 1 (`{a1}x + {b1}y = {c1}`) akan dikalikan dengan:**")
        if b2 != 0:
            suggested_mult1_y = b2
        else:
            suggested_mult1_y = 1.0
        mult1_y = st.number_input("", value=suggested_mult1_y, key="mult1_y")

    with col_elim_y2:
        st.markdown(f"**Persamaan 2 (`{a2}x + {b2}y = {c2}`) akan dikalikan dengan:**")
        if b1 != 0:
            suggested_mult2_y = b1
        else:
            suggested_mult2_y = 1.0
        mult2_y = st.number_input("", value=suggested_mult2_y, key="mult2_y")

    new_a1 = a1 * mult1_y
    new_b1 = b1 * mult1_y
    new_c1 = c1 * mult1_y

    new_a2 = a2 * mult2_y
    new_b2 = b2 * mult2_y
    new_c2 = c2 * mult2_y

    st.markdown("---")
    st.subheader("Persamaan Setelah Dikali:")
    st.write(f"1') `{new_a1:.2f}x + {new_b1:.2f}y = {new_c1:.2f}`")
    st.write(f"2') `{new_a2:.2f}x + {new_b2:.2f}y = {new_c2:.2f}`")

    st.markdown("Sekarang, perhatikan koefisien $y$. Apa yang harus kamu lakukan untuk **menghilangkan** $y$?")
    
    operation_y = st.radio("Pilih Operasi:", ("Kurangkan (1' - 2')", "Jumlahkan (1' + 2')"))

    if st.button("Lakukan Operasi (Eliminasi y)"):
        if operation_y == "Kurangkan (1' - 2')":
            res_a = new_a1 - new_a2
            res_b = new_b1 - new_b2
            res_c = new_c1 - new_c2
        else: # Jumlahkan
            res_a = new_a1 + new_a2
            res_b = new_b1 + new_b2
            res_c = new_c1 + new_c2

        st.markdown("---")
        st.subheader("Hasil Setelah Eliminasi:")
        st.write(f"`{res_a:.2f}x + {res_b:.2f}y = {res_c:.2f}`")

        if abs(res_b) < 1e-9: # Cek apakah koefisien y mendekati nol
            st.success(f"🎉 **Selamat!** Anda berhasil mengeliminasi 'y'. Sekarang Anda memiliki persamaan satu variabel: `{res_a:.2f}x = {res_c:.2f}`.")
            if res_a != 0:
                found_x = res_c / res_a
                st.write(f"Dari sini, Anda bisa menemukan nilai $x$: $x = {found_x:.2f}$")
                st.session_state['found_x'] = found_x # Simpan nilai x ke session state
                st.info("Sekarang kita punya nilai x! Lanjut ke langkah selanjutnya untuk mencari y.")
            else:
                st.warning("Koefisien x juga nol. Ini berarti sistem memiliki tak hingga solusi atau tidak ada solusi. Coba periksa kembali persamaan atau operasinya.")
        else:
            st.error("❌ **Oops!** Koefisien 'y' belum nol. Coba periksa kembali nilai pengali atau operasi yang Anda pilih.")

---

## Langkah 4: Substitusi (Temukan Variabel Lainnya)

Setelah menemukan salah satu variabel ($x$ atau $y$), sekarang saatnya mencari nilai variabel yang lain dengan **substitusi**.

**Apa itu Substitusi?**
Substitusi berarti **mengganti** nilai variabel yang sudah diketahui ke dalam salah satu persamaan awal. Dengan begitu, kita bisa menyelesaikan persamaan untuk variabel yang tersisa.


# Check if x or y was found in the previous step
found_x = st.session_state.get('found_x')
found_y = st.session_state.get('found_y')

if found_y is not None:
    st.markdown(f"Anda telah menemukan $y = {found_y:.2f}$. Sekarang substitusikan nilai $y$ ini ke salah satu persamaan awal.")
    st.markdown(f"Misalnya, gunakan Persamaan 1: `{a1}x + {b1}y = {c1}`")
    
    st.write(f"Jika $y = {found_y:.2f}$, maka: `{a1}x + {b1} * {found_y:.2f} = {c1}`")
    
    calculated_term = b1 * found_y
    st.write(f"`{a1}x + {calculated_term:.2f} = {c1}`")
    st.write(f"Sekarang, coba pindahkan konstanta: `{a1}x = {c1} - {calculated_term:.2f}`")
    
    result_rhs = c1 - calculated_term
    st.write(f"`{a1}x = {result_rhs:.2f}`")

    if a1 != 0:
        calculated_x = result_rhs / a1
        st.write(f"Maka $x = {result_rhs:.2f} / {a1:.2f} = {calculated_x:.2f}$")
        st.success(f"Nilai $x$ yang ditemukan adalah: **{calculated_x:.2f}**")
        st.session_state['calculated_x'] = calculated_x # Simpan x juga
    else:
        st.warning("Koefisien a1 adalah nol. Tidak dapat menyelesaikan x dengan metode ini dari persamaan 1.")

elif found_x is not None:
    st.markdown(f"Anda telah menemukan $x = {found_x:.2f}$. Sekarang substitusikan nilai $x$ ini ke salah satu persamaan awal.")
    st.markdown(f"Misalnya, gunakan Persamaan 1: `{a1}x + {b1}y = {c1}`")

    st.write(f"Jika $x = {found_x:.2f}$, maka: `{a1} * {found_x:.2f} + {b1}y = {c1}`")
    
    calculated_term = a1 * found_x
    st.write(f"`{calculated_term:.2f} + {b1}y = {c1}`")
    st.write(f"Sekarang, coba pindahkan konstanta: `{b1}y = {c1} - {calculated_term:.2f}`")

    result_rhs = c1 - calculated_term
    st.write(f"`{b1}y = {result_rhs:.2f}`")

    if b1 != 0:
        calculated_y = result_rhs / b1
        st.write(f"Maka $y = {result_rhs:.2f} / {b1:.2f} = {calculated_y:.2f}$")
        st.success(f"Nilai $y$ yang ditemukan adalah: **{calculated_y:.2f}**")
        st.session_state['calculated_y'] = calculated_y # Simpan y juga
    else:
        st.warning("Koefisien b1 adalah nol. Tidak dapat menyelesaikan y dengan metode ini dari persamaan 1.")
else:
    st.info("Selesaikan langkah eliminasi terlebih dahulu untuk menemukan salah satu variabel.")


---

## Langkah 5: Verifikasi Jawaban Anda

Setelah Anda menemukan nilai $x$ dan $y$, mari kita cek apakah jawaban Anda benar!


final_x = st.session_state.get('calculated_x') if st.session_state.get('calculated_x') is not None else st.session_state.get('found_x')
final_y = st.session_state.get('calculated_y') if st.session_state.get('calculated_y') is not None else st.session_state.get('found_y')

if final_x is not None and final_y is not None:
    st.markdown(f"Anda menemukan $x = {final_x:.2f}$ dan $y = {final_y:.2f}$. Mari kita cek ke persamaan awal:")
    
    st.subheader("Cek Persamaan 1:")
    check1_left = a1 * final_x + b1 * final_y
    st.write(f"`{a1}*{final_x:.2f} + {b1}*{final_y:.2f} = {check1_left:.2f}`")
    if abs(check1_left - c1) < 1e-6:
        st.success(f"Cocok dengan $c_1 = {c1:.2f}$! ✅")
    else:
        st.error(f"Tidak cocok dengan $c_1 = {c1:.2f}$. Ada kesalahan.")

    st.subheader("Cek Persamaan 2:")
    check2_left = a2 * final_x + b2 * final_y
    st.write(f"`{a2}*{final_x:.2f} + {b2}*{final_y:.2f} = {check2_left:.2f}`")
    if abs(check2_left - c2) < 1e-6:
        st.success(f"Cocok dengan $c_2 = {c2:.2f}$! ✅")
    else:
        st.error(f"Tidak cocok dengan $c_2 = {c2:.2f}$. Ada kesalahan.")

    if st.button("Lihat Solusi Resmi"):
        x_sol, y_sol, error_msg = solve_spldv(a1, b1, c1, a2, b2, c2)
        if error_msg:
            st.error(f"Maaf, sistem persamaan ini {error_msg}")
        else:
            st.success(f"**Solusi sebenarnya adalah:** $x = {x_sol:.2f}$, $y = {y_sol:.2f}$")
            if abs(x_sol - final_x) < 1e-6 and abs(y_sol - final_y) < 1e-6:
                st.balloons()
                st.markdown("🎉 **HEBAT! Jawaban Anda BENAR!** 🎉")
            else:
                st.error("Jawaban Anda sedikit berbeda. Coba periksa kembali langkah-langkah perhitungan Anda.")
else:
    st.info("Lakukan semua langkah di atas untuk memverifikasi jawaban.")

st.markdown("""
---
**Tentang Aplikasi Ini:**
Aplikasi ini dirancang untuk membimbing Anda melalui proses penyelesaian SPLDV.
Dengan mempraktikkan langkah-langkah eliminasi dan substitusi serta memvisualisasikan hasilnya,
diharapkan pemahaman Anda tentang SPLDV akan semakin kuat.


if st.button("Ulangi dari Awal"):
    st.session_state['found_x'] = None
    st.session_state['found_y'] = None
    st.session_state['calculated_x'] = None
    st.session_state['calculated_y'] = None
    st.experimental_rerun()
