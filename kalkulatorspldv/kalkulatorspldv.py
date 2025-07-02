import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def hitung_y(persamaan, x_val):
    """
    Menghitung nilai y berdasarkan persamaan dan nilai x.
    Persamaan diberikan dalam bentuk (a, b, c) untuk ax + by = c.
    """
    a, b, c = persamaan
    if b == 0:
        # Untuk garis vertikal, y tidak terdefinisi unik, kembalikan array inf/nan
        # Tergantung bagaimana kita ingin menanganinya di plot, tapi umumnya kita plot x=konstanta
        return np.full_like(x_val, np.nan) # Mengembalikan NaN untuk y jika b=0
    return (c - a * x_val) / b

def plot_garis(persamaan1, persamaan2, x_range, point_x=None, point_y=None):
    """
    Membuat plot dua garis dan menandai titik potong jika ada.
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    a1, b1, c1 = persamaan1
    a2, b2, c2 = persamaan2

    # Plot Persamaan 1
    if b1 != 0:
        y1 = hitung_y(persamaan1, x_range)
        ax.plot(x_range, y1, label=f'{a1}x + {b1}y = {c1} (Garis 1)', color='blue')
    else: # Garis vertikal
        # Menghindari ZeroDivisionError jika a1=0 (yang seharusnya sudah divalidasi di awal)
        if a1 != 0:
            ax.axvline(x=c1/a1, color='blue', linestyle='--', label=f'x = {c1/a1:.2f} (Garis 1)')
        else:
            # Kasus di mana a1=0 dan b1=0, ini seharusnya sudah terdeteksi di validasi awal
            pass # Tidak menggambar apa-apa, atau bisa juga memberi pesan error di UI

    # Plot Persamaan 2
    if b2 != 0:
        y2 = hitung_y(persamaan2, x_range)
        ax.plot(x_range, y2, label=f'{a2}x + {b2}y = {c2} (Garis 2)', color='red')
    else: # Garis vertikal
        # Menghindari ZeroDivisionError jika a2=0 (yang seharusnya sudah divalidasi di awal)
        if a2 != 0:
            ax.axvline(x=c2/a2, color='red', linestyle='--', label=f'x = {c2/a2:.2f} (Garis 2)')
        else:
            # Kasus di mana a2=0 dan b2=0, ini seharusnya sudah terdeteksi di validasi awal
            pass # Tidak menggambar apa-apa

    # Plot titik coba jika diberikan
    if point_x is not None and point_y is not None:
        ax.scatter(point_x, point_y, color='purple', s=100, zorder=5, label=f'Titik Coba ({point_x:.2f}, {point_y:.2f})')

    ax.set_xlabel("Nilai X")
    ax.set_ylabel("Nilai Y")
    ax.set_title("Grafik Persamaan Linear")
    ax.axhline(0, color='grey', linewidth=0.5)
    ax.axvline(0, color='grey', linewidth=0.5)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    ax.set_xlim(x_range.min(), x_range.max())

    # Sesuaikan ylim secara dinamis agar grafik tidak terpotong
    all_y_vals = []
    if b1 != 0:
        valid_y1 = y1[~np.isnan(y1) & ~np.isinf(y1)]
        if valid_y1.size > 0:
            all_y_vals.extend(valid_y1)
    if b2 != 0:
        valid_y2 = y2[~np.isnan(y2) & ~np.isinf(y2)]
        if valid_y2.size > 0:
            all_y_vals.extend(valid_y2)

    if all_y_vals:
        min_y = np.min(all_y_vals) - 1
        max_y = np.max(all_y_vals) + 1
        ax.set_ylim(min_y, max_y)
    else: # Jika tidak ada y yang valid (misal keduanya vertikal)
        ax.set_ylim(-5, 5) # Default range

    return fig

def hitung_solusi_spldv(persamaan1, persamaan2):
    """
    Menghitung solusi SPLDV menggunakan metode eliminasi/substitusi.
    Mengembalikan (x, y) atau (None, None) jika paralel/identik, atau (float('inf'), float('inf')) untuk vertikal identik.
    """
    a1, b1, c1 = persamaan1
    a2, b2, c2 = persamaan2

    determinant = a1 * b2 - a2 * b1

    if determinant == 0:
        # Garis paralel atau identik
        # Cek apakah identik (rasio koefisien sama dan rasio konstanta juga sama)
        # Menggunakan cross-multiplication untuk memeriksa konsistensi
        # Cek a1*c2 - a2*c1 dan b1*c2 - b2*c1
        if abs(a1 * c2 - a2 * c1) < 1e-9 and abs(b1 * c2 - b2 * c1) < 1e-9:
            # Kedua persamaan adalah garis yang sama (tak terhingga solusi).
            return float('inf'), float('inf') # Mengindikasikan tak terhingga solusi
        else:
            # Kedua persamaan adalah garis paralel (tidak ada solusi).
            return None, None
    else:
        x = (c1 * b2 - c2 * b1) / determinant
        y = (a1 * c2 - a2 * c1) / determinant
        return x, y

# --- Aplikasi Streamlit ---
st.set_page_config(layout="wide", page_title="Kalkulator SPLDV Interaktif")

st.title("💡 Kalkulator SPLDV Interaktif (Metode Discovery Learning)")
st.markdown("Coba temukan titik potong dari dua persamaan linear dengan **bereksperimen** dan **memvisualisasikan**!")

# Bagian Input Persamaan
st.header("1. Masukkan Persamaan Anda")
st.markdown("Bentuk umum persamaan adalah: $ax + by = c$")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Persamaan 1")
    a1 = st.number_input("Koefisien a1 (untuk x):", value=1.0, key="a1")
    b1 = st.number_input("Koefisien b1 (untuk y):", value=-1.0, key="b1")
    c1 = st.number_input("Konstanta c1:", value=2.0, key="c1")
    persamaan1_str = f"**Persamaan 1:** ${a1:.2f}x + {b1:.2f}y = {c1:.2f}$"
    st.markdown(persamaan1_str)

with col2:
    st.subheader("Persamaan 2")
    a2 = st.number_input("Koefisien a2 (untuk x):", value=2.0, key="a2")
    b2 = st.number_input("Koefisien b2 (untuk y):", value=1.0, key="b2")
    c2 = st.number_input("Konstanta c2:", value=7.0, key="c2")
    persamaan2_str = f"**Persamaan 2:** ${a2:.2f}x + {b2:.2f}y = {c2:.2f}$"
    st.markdown(persamaan2_str)

persamaan1 = (a1, b1, c1)
persamaan2 = (a2, b2, c2)

# Validasi awal
if (b1 == 0 and a1 == 0):
    st.error("Koefisien 'a1' dan 'b1' tidak boleh keduanya nol untuk Persamaan 1. Harap perbaiki input Anda.")
    st.stop() # Hentikan eksekusi jika input tidak valid
if (b2 == 0 and a2 == 0):
    st.error("Koefisien 'a2' dan 'b2' tidak boleh keduanya nol untuk Persamaan 2. Harap perbaiki input Anda.")
    st.stop() # Hentikan eksekusi jika input tidak valid

# Bagian Discovery Learning
st.header("2. Temukan Titik Potong!")
st.markdown("Geser slider **Nilai X Coba** di bawah ini dan perhatikan bagaimana nilai Y berubah untuk kedua garis di plot. Tujuannya adalah membuat nilai Y dari kedua garis bertemu!")

# Slider untuk nilai X yang dicoba
x_coba = st.slider("Nilai X Coba:", min_value=-10.0, max_value=10.0, value=0.0, step=0.1)

# Hitung Y untuk nilai X coba
y1_coba_raw = hitung_y(persamaan1, np.array([x_coba]))[0] # Ambil elemen pertama dari array
y2_coba_raw = hitung_y(persamaan2, np.array([x_coba]))[0]

st.subheader("Hasil Percobaan Anda:")
col_res1, col_res2 = st.columns(2)

with col_res1:
    if b1 == 0:
        if a1 != 0:
            st.info(f"Dari Persamaan 1 ($x = {c1/a1:.2f}$): Ini adalah **garis vertikal**.")
        else: # Seharusnya tidak tercapai karena validasi awal
            st.info("Persamaan 1 tidak valid (a1 dan b1 keduanya nol).")
    else:
        st.markdown(f"Dari Persamaan 1, jika $x = {x_coba:.2f}$, maka $y_1 = \mathbf{{{y1_coba_raw:.4f}}}$")
with col_res2:
    if b2 == 0:
        if a2 != 0:
            st.info(f"Dari Persamaan 2 ($x = {c2/a2:.2f}$): Ini adalah **garis vertikal**.")
        else: # Seharusnya tidak tercapai karena validasi awal
            st.info("Persamaan 2 tidak valid (a2 dan b2 keduanya nol).")
    else:
        st.markdown(f"Dari Persamaan 2, jika $x = {x_coba:.2f}$, maka $y_2 = \mathbf{{{y2_coba_raw:.4f}}}$")

# Umpan Balik / Petunjuk
tolerance = 0.01 # Toleransi untuk dianggap "sama"

is_solution_found_by_discovery = False

# Kasus 1: Kedua garis non-vertikal
if b1 != 0 and b2 != 0:
    if abs(y1_coba_raw - y2_coba_raw) < tolerance:
        st.success(f"🎉 **Hebat!** Anda telah menemukan titik di mana $y_1$ dan $y_2$ sangat dekat!")
        st.balloons()
        st.markdown(f"**Titik potong kira-kira adalah:** $({x_coba:.2f}, {(y1_coba_raw + y2_coba_raw) / 2:.2f})$")
        is_solution_found_by_discovery = True
    else:
        st.warning(f"**Petunjuk:** $y_1$ dan $y_2$ belum sama. ")
        if y1_coba_raw < y2_coba_raw:
            st.info("Coba geser **Nilai X Coba** ke kanan untuk mendekatkan $y_1$ dan $y_2$.")
        else:
            st.info("Coba geser **Nilai X Coba** ke kiri untuk mendekatkan $y_1$ dan $y_2$.")
        st.markdown(f"**Perbedaan $|y_1 - y_2|$: ** $\mathbf{{{abs(y1_coba_raw - y2_coba_raw):.4f}}}$")
# Kasus 2: Kedua garis vertikal
elif b1 == 0 and b2 == 0:
    # Memastikan a1 dan a2 bukan nol karena sudah divalidasi
    if abs(c1/a1 - c2/a2) < tolerance:
        st.success("🎉 **Hebat!** Kedua persamaan adalah garis vertikal yang sama. Ada tak terhingga solusi.")
        is_solution_found_by_discovery = True
    else:
        st.error("Kedua persamaan adalah garis vertikal yang paralel. Tidak ada solusi.")
        is_solution_found_by_discovery = True
# Kasus 3: Persamaan 1 vertikal, Persamaan 2 non-vertikal
elif b1 == 0 and b2 != 0:
    if a1 != 0: # Pastikan a1 bukan nol
        x_intersect_p1 = c1 / a1
        y_from_p2 = hitung_y(persamaan2, np.array([x_intersect_p1]))[0]
        st.success(f"🎉 **Hebat!** Persamaan 1 adalah garis vertikal $x = {x_intersect_p1:.2f}$.")
        st.markdown(f"Jika $x = {x_intersect_p1:.2f}$, maka $y_2$ dari Persamaan 2 adalah $\mathbf{{{y_from_p2:.2f}}}$.")
        st.markdown(f"**Titik potongnya adalah:** $({x_intersect_p1:.2f}, {y_from_p2:.2f})$")
        is_solution_found_by_discovery = True
    else: # a1=0 sudah divalidasi, ini untuk berjaga-jaga
        st.error("Kesalahan internal: a1 = 0 padahal b1 juga 0, seharusnya sudah terdeteksi.")
# Kasus 4: Persamaan 2 vertikal, Persamaan 1 non-vertikal
elif b2 == 0 and b1 != 0:
    if a2 != 0: # Pastikan a2 bukan nol
        x_intersect_p2 = c2 / a2
        y_from_p1 = hitung_y(persamaan1, np.array([x_intersect_p2]))[0]
        st.success(f"🎉 **Hebat!** Persamaan 2 adalah garis vertikal $x = {x_intersect_p2:.2f}$.")
        st.markdown(f"Jika $x = {x_intersect_p2:.2f}$, maka $y_1$ dari Persamaan 1 adalah $\mathbf{{{y_from_p1:.2f}}}$.")
        st.markdown(f"**Titik potongnya adalah:** $({x_intersect_p2:.2f}, {y_from_p1:.2f})$")
        is_solution_found_by_discovery = True
    else: # a2=0 sudah divalidasi, ini untuk berjaga-jaga
        st.error("Kesalahan internal: a2 = 0 padahal b2 juga 0, seharusnya sudah terdeteksi.")


# Bagian Visualisasi
st.header("3. Visualisasi Grafik")
x_range = np.linspace(-10, 10, 400) # Range X untuk plotting

# Tentukan titik yang akan ditandai di plot
plot_x = x_coba
plot_y = None # Inisialisasi

# Logika untuk plot_x dan plot_y saat menemukan titik potong vertikal
if b1 == 0 and a1 != 0: # Persamaan 1 vertikal
    plot_x = c1 / a1
    if b2 != 0: # Jika P2 non-vertikal
        plot_y = hitung_y(persamaan2, np.array([plot_x]))[0]
    # Jika P2 juga vertikal, plot_y tetap None, karena tidak ada titik tunggal yang "potong"
elif b2 == 0 and a2 != 0: # Persamaan 2 vertikal
    plot_x = c2 / a2
    if b1 != 0: # Jika P1 non-vertikal
        plot_y = hitung_y(persamaan1, np.array([plot_x]))[0]
    # Jika P1 juga vertikal, plot_y tetap None
else: # Kedua garis non-vertikal
    plot_y = (y1_coba_raw + y2_coba_raw) / 2 # Rata-rata y jika dekat

# Pastikan plot_y bukan NaN atau Inf
if plot_y is not None and (np.isnan(plot_y) or np.isinf(plot_y)):
    plot_y = None
if np.isnan(plot_x) or np.isinf(plot_x):
    plot_x = None

fig = plot_garis(persamaan1, persamaan2, x_range, point_x=plot_x, point_y=plot_y)
st.pyplot(fig)
st.markdown("Titik ungu menunjukkan nilai X yang sedang Anda coba, atau perkiraan titik potong jika ditemukan.")

# Bagian Solusi Matematis (opsional, untuk konfirmasi)
st.header("4. Konfirmasi Solusi Matematis")
st.markdown("Jika Anda ingin mengkonfirmasi jawaban atau kesulitan menemukannya, lihat solusi matematisnya di sini.")

if st.button("Tampilkan Solusi Matematis"):
    solusi_x, solusi_y = hitung_solusi_spldv(persamaan1, persamaan2)

    if solusi_x is not None and solusi_y is not None:
        if solusi_x == float('inf') and solusi_y == float('inf'):
            st.info("Kedua garis adalah **garis yang sama**. Terdapat **tak terhingga solusi**.")
        else:
            st.success(f"Secara matematis, titik potongnya adalah: $x = \\mathbf{{{solusi_x:.4f}}}$, $y = \\mathbf{{{solusi_y:.4f}}}$")
            st.markdown(f"Titik potong: $\\left({solusi_x:.4f}, {solusi_y:.4f}\\right)$")
            # Tambahkan plot solusi matematis
            st.markdown("---")
            st.subheader("Plot dengan Titik Solusi Akurat")
            fig_sol = plot_garis(persamaan1, persamaan2, x_range, point_x=solusi_x, point_y=solusi_y)
            st.pyplot(fig_sol)
            st.markdown("Titik ungu sekarang menunjukkan titik potong yang akurat secara matematis.")

    else:
        st.error("Kedua garis **paralel** dan tidak berpotongan. **Tidak ada solusi**.")

st.markdown("---")
# Baris yang diperbaiki:
st.markdown("Dibuat dengan Python oleh rarayuniaini")
