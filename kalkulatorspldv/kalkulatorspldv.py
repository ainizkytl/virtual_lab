import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time # Untuk simulasi loading/animasi

# --- Fungsi-fungsi Utama (tidak banyak berubah) ---

def hitung_y(persamaan, x_val):
    """
    Menghitung nilai y berdasarkan persamaan dan nilai x.
    Persamaan diberikan dalam bentuk (a, b, c) untuk ax + by = c.
    """
    a, b, c = persamaan
    if b == 0:
        return np.full_like(x_val, np.nan) # Mengembalikan NaN untuk y jika b=0
    return (c - a * x_val) / b

def plot_garis(persamaan1, persamaan2, x_range, color1, color2, point_x=None, point_y=None, show_exact_point=False):
    """
    Membuat plot dua garis dan menandai titik potong jika ada.
    """
    fig, ax = plt.subplots(figsize=(10, 7)) # Ukuran plot lebih besar

    a1, b1, c1 = persamaan1
    a2, b2, c2 = persamaan2

    # Plot Persamaan 1
    if b1 != 0:
        y1 = hitung_y(persamaan1, x_range)
        ax.plot(x_range, y1, label=f'{a1:.2f}x + {b1:.2f}y = {c1:.2f} (Garis 1)', color=color1, linewidth=2)
    else: # Garis vertikal
        if a1 != 0:
            ax.axvline(x=c1/a1, color=color1, linestyle='--', label=f'x = {c1/a1:.2f} (Garis 1)', linewidth=2)

    # Plot Persamaan 2
    if b2 != 0:
        y2 = hitung_y(persamaan2, x_range)
        ax.plot(x_range, y2, label=f'{a2:.2f}x + {b2:.2f}y = {c2:.2f} (Garis 2)', color=color2, linewidth=2)
    else: # Garis vertikal
        if a2 != 0:
            ax.axvline(x=c2/a2, color=color2, linestyle='--', label=f'x = {c2/a2:.2f} (Garis 2)', linewidth=2)

    # Plot titik coba atau titik solusi yang ditemukan
    if point_x is not None and point_y is not None and not np.isnan(point_x) and not np.isinf(point_x) and not np.isnan(point_y) and not np.isinf(point_y):
        marker_color = 'purple' if not show_exact_point else 'green'
        label_text = f'Titik Coba ({point_x:.2f}, {point_y:.2f})' if not show_exact_point else f'Solusi Akurat ({point_x:.2f}, {point_y:.2f})'
        ax.scatter(point_x, point_y, color=marker_color, s=150, zorder=5, label=label_text, edgecolor='black', linewidth=1.5)

    ax.set_xlabel("Nilai X", fontsize=12)
    ax.set_ylabel("Nilai Y", fontsize=12)
    ax.set_title("Grafik Persamaan Linear", fontsize=14, fontweight='bold')
    ax.axhline(0, color='grey', linewidth=0.7, linestyle=':')
    ax.axvline(0, color='grey', linewidth=0.7, linestyle=':')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(fontsize=10)
    ax.set_xlim(x_range.min(), x_range.max())

    # Auto-adjust Y limits, handling inf/nan values from vertical lines
    all_y_vals = []
    if b1 != 0:
        valid_y1 = y1[~np.isnan(y1) & ~np.isinf(y1)]
        if valid_y1.size > 0: all_y_vals.extend(valid_y1)
    if b2 != 0:
        valid_y2 = y2[~np.isnan(y2) & ~np.isinf(y2)]
        if valid_y2.size > 0: all_y_vals.extend(valid_y2)

    if all_y_vals:
        min_y = np.min(all_y_vals) - 1.5
        max_y = np.max(all_y_vals) + 1.5
        # Prevent very narrow or inverted Y limits
        if max_y - min_y < 5:
            mid_y = (min_y + max_y) / 2
            min_y = mid_y - 2.5
            max_y = mid_y + 2.5
        ax.set_ylim(min_y, max_y)
    else: # Default range if no valid Y values (e.g., both vertical)
        ax.set_ylim(-5, 5)

    plt.tight_layout() # Memperbaiki layout plot
    return fig

def hitung_solusi_spldv(persamaan1, persamaan2):
    """
    Menghitung solusi SPLDV menggunakan metode eliminasi/substitusi.
    Mengembalikan (x, y) atau (None, None) jika paralel/identik, atau (float('inf'), float('inf')) untuk vertikal identik.
    """
    a1, b1, c1 = persamaan1
    a2, b2, c2 = persamaan2

    determinant = a1 * b2 - a2 * b1

    if abs(determinant) < 1e-9: # Perbandingan dengan toleransi untuk floating point
        # Garis paralel atau identik
        if abs(a1 * c2 - a2 * c1) < 1e-9 and abs(b1 * c2 - b2 * c1) < 1e-9:
            return float('inf'), float('inf') # Mengindikasikan tak terhingga solusi
        else:
            return None, None # Garis paralel
    else:
        x = (c1 * b2 - c2 * b1) / determinant
        y = (a1 * c2 - a2 * c1) / determinant
        return x, y

# --- Konfigurasi Halaman Streamlit ---
st.set_page_config(
    layout="wide",
    page_title="Kalkulator SPLDV Interaktif",
    initial_sidebar_state="expanded" # Sidebar dibuka secara default
)

# --- Sidebar ---
with st.sidebar:
    st.image("https://www.freeiconspng.com/uploads/graph-icon-png-1.png", width=100) # Ikon menarik
    st.header("Pengaturan Aplikasi")
    st.markdown("""
        Selamat datang di Kalkulator SPLDV Interaktif!
        Gunakan aplikasi ini untuk memahami bagaimana dua persamaan linear
        berpotongan dengan **bereksperimen** dan **melihat visualisasinya**.
    """)

    st.subheader("Pengaturan Tampilan Garis")
    line1_color = st.color_picker("Warna Garis 1", "#4CAF50") # Hijau
    line2_color = st.color_picker("Warna Garis 2", "#FF5733") # Oranye

    st.markdown("---")
    st.write("Dibuat dengan ❤️ oleh Mahasiswa/i") # Footer di sidebar
    if st.button("Reset Aplikasi"):
        st.experimental_rerun()

# --- Judul dan Deskripsi Utama ---
st.title("✨ Kalkulator SPLDV Interaktif (Metode Discovery Learning)")
st.markdown("""
    Pelajari cara menemukan **titik potong** dari dua persamaan linear
    dengan **eksplorasi interaktif** dan **visualisasi grafis** yang menawan.
    Ikuti langkah-langkah di bawah ini!
""")

# --- Bagian Input Persamaan ---
st.header("1. Masukkan Persamaan Anda")
st.markdown("Masukkan koefisien untuk setiap persamaan dalam bentuk umum: $ax + by = c$")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Persamaan 1")
    a1 = st.number_input("Koefisien a1 (untuk x):", value=1.0, key="a1_main", help="Koefisien variabel x pada Persamaan 1")
    b1 = st.number_input("Koefisien b1 (untuk y):", value=-1.0, key="b1_main", help="Koefisien variabel y pada Persamaan 1")
    c1 = st.number_input("Konstanta c1:", value=2.0, key="c1_main", help="Nilai konstanta pada Persamaan 1")
    st.info(f"**Persamaan 1:** ${a1:.2f}x + {b1:.2f}y = {c1:.2f}$")

with col2:
    st.subheader("Persamaan 2")
    a2 = st.number_input("Koefisien a2 (untuk x):", value=2.0, key="a2_main", help="Koefisien variabel x pada Persamaan 2")
    b2 = st.number_input("Koefisien b2 (untuk y):", value=1.0, key="b2_main", help="Koefisien variabel y pada Persamaan 2")
    c2 = st.number_input("Konstanta c2:", value=7.0, key="c2_main", help="Nilai konstanta pada Persamaan 2")
    st.info(f"**Persamaan 2:** ${a2:.2f}x + {b2:.2f}y = {c2:.2f}$")

persamaan1 = (a1, b1, c1)
persamaan2 = (a2, b2, c2)

# Validasi awal
if (b1 == 0 and a1 == 0):
    st.error("🚨 Kesalahan: Koefisien 'a1' dan 'b1' tidak boleh keduanya nol untuk Persamaan 1. Harap perbaiki input Anda.")
    st.stop()
if (b2 == 0 and a2 == 0):
    st.error("🚨 Kesalahan: Koefisien 'a2' dan 'b2' tidak boleh keduanya nol untuk Persamaan 2. Harap perbaiki input Anda.")
    st.stop()

# --- Bagian Discovery Learning ---
st.header("2. Temukan Titik Potong dengan Eksplorasi!")
st.markdown("""
    Geser slider **Nilai X Coba** di bawah ini dan perhatikan bagaimana nilai Y berubah untuk kedua garis di plot.
    **Tujuan Anda adalah menemukan nilai X di mana kedua garis berpotongan, yaitu saat nilai Y dari kedua garis sama!**
""")

# Slider untuk nilai X yang dicoba
x_coba = st.slider("➡️ Geser Nilai X Coba:", min_value=-10.0, max_value=10.0, value=0.0, step=0.1,
                   help="Geser slider ini untuk mencoba berbagai nilai X.")

with st.spinner('Menghitung nilai Y...'):
    y1_coba_raw = hitung_y(persamaan1, np.array([x_coba]))[0]
    y2_coba_raw = hitung_y(persamaan2, np.array([x_coba]))[0]
    time.sleep(0.1) # Sedikit delay untuk melihat spinner

st.subheader("📊 Hasil Percobaan Anda:")

col_res1, col_res2, col_diff = st.columns(3)

with col_res1:
    if b1 == 0:
        if a1 != 0:
            st.code(f"Persamaan 1: x = {c1/a1:.2f} (Garis Vertikal)")
        else:
            st.error("Persamaan 1 tidak valid.")
    else:
        st.metric(label="Y1 (dari Persamaan 1)", value=f"{y1_coba_raw:.4f}")

with col_res2:
    if b2 == 0:
        if a2 != 0:
            st.code(f"Persamaan 2: x = {c2/a2:.2f} (Garis Vertikal)")
        else:
            st.error("Persamaan 2 tidak valid.")
    else:
        st.metric(label="Y2 (dari Persamaan 2)", value=f"{y2_coba_raw:.4f}")

with col_diff:
    tolerance = 0.05 # Toleransi untuk dianggap "sama"
    diff_y = abs(y1_coba_raw - y2_coba_raw) if b1 != 0 and b2 != 0 else float('inf')

    if b1 != 0 and b2 != 0:
        if diff_y < tolerance:
            st.metric(label="Perbedaan |Y1 - Y2|", value=f"{diff_y:.4f}", delta="✅ Sangat dekat!", delta_color="normal")
        else:
            st.metric(label="Perbedaan |Y1 - Y2|", value=f"{diff_y:.4f}", delta="Perlu disesuaikan", delta_color="inverse")
    else:
        st.markdown("Perbedaan Y tidak relevan untuk garis vertikal.")


# Umpan Balik / Petunjuk
is_solution_found_by_discovery = False

if b1 != 0 and b2 != 0: # Kedua garis non-vertikal
    if abs(y1_coba_raw - y2_coba_raw) < tolerance:
        st.success(f"🎉 **SELAMAT!** Anda telah menemukan titik di mana $y_1$ dan $y_2$ sangat dekat!")
        st.balloons()
        st.markdown(f"**Titik potong kira-kira adalah:** $({x_coba:.2f}, {(y1_coba_raw + y2_coba_raw) / 2:.2f})$")
        is_solution_found_by_discovery = True
    else:
        st.warning(f"**Petunjuk:** $y_1$ dan $y_2$ belum sama. ")
        if y1_coba_raw < y2_coba_raw:
            st.info("💡 **Tips:** Coba geser **Nilai X Coba** ke kanan untuk membuat $y_1$ dan $y_2$ bertemu.")
        else:
            st.info("💡 **Tips:** Coba geser **Nilai X Coba** ke kiri untuk membuat $y_1$ dan $y_2$ bertemu.")
elif b1 == 0 and b2 == 0: # Kedua garis vertikal
    if a1 != 0 and a2 != 0 and abs(c1/a1 - c2/a2) < tolerance:
        st.success("🎉 **SELAMAT!** Kedua persamaan adalah garis vertikal yang sama. Terdapat **tak terhingga solusi**.")
        is_solution_found_by_discovery = True
    else:
        st.error("🚨 Kedua persamaan adalah garis vertikal yang paralel. **Tidak ada solusi**.")
        is_solution_found_by_discovery = True
elif b1 == 0 and a1 != 0: # Persamaan 1 vertikal, Persamaan 2 non-vertikal
    x_intersect_p1 = c1 / a1
    y_from_p2 = hitung_y(persamaan2, np.array([x_intersect_p1]))[0]
    st.success(f"🎉 **SELAMAT!** Persamaan 1 adalah garis vertikal $x = {x_intersect_p1:.2f}$.")
    st.markdown(f"Jika $x = {x_intersect_p1:.2f}$, maka $y_2$ dari Persamaan 2 adalah $\mathbf{{{y_from_p2:.2f}}}$.")
    st.markdown(f"**Titik potongnya adalah:** $({x_intersect_p1:.2f}, {y_from_p2:.2f})$")
    is_solution_found_by_discovery = True
elif b2 == 0 and a2 != 0: # Persamaan 2 vertikal, Persamaan 1 non-vertikal
    x_intersect_p2 = c2 / a2
    y_from_p1 = hitung_y(persamaan1, np.array([x_intersect_p2]))[0]
    st.success(f"🎉 **SELAMAT!** Persamaan 2 adalah garis vertikal $x = {x_intersect_p2:.2f}$.")
    st.markdown(f"Jika $x = {x_intersect_p2:.2f}$, maka $y_1$ dari Persamaan 1 adalah $\mathbf{{{y_from_p1:.2f}}}$.")
    st.markdown(f"**Titik potongnya adalah:** $({x_intersect_p2:.2f}, {y_from_p1:.2f})$")
    is_solution_found_by_discovery = True


# --- Bagian Visualisasi ---
st.header("3. Visualisasi Grafik")
st.markdown("Perhatikan bagaimana kedua garis berinteraksi saat Anda mengubah nilai X.")
x_range = np.linspace(-10, 10, 400) # Range X untuk plotting

# Tentukan titik yang akan ditandai di plot
plot_x_marker = x_coba
plot_y_marker = None

# Logika penentuan plot_x_marker dan plot_y_marker
if b1 == 0 and a1 != 0: # Persamaan 1 vertikal
    plot_x_marker = c1 / a1
    if b2 != 0: # Jika P2 non-vertikal
        plot_y_marker = hitung_y(persamaan2, np.array([plot_x_marker]))[0]
    # Jika P2 juga vertikal, plot_y_marker tetap None
elif b2 == 0 and a2 != 0: # Persamaan 2 vertikal
    plot_x_marker = c2 / a2
    if b1 != 0: # Jika P1 non-vertikal
        plot_y_marker = hitung_y(persamaan1, np.array([plot_x_marker]))[0]
    # Jika P1 juga vertikal, plot_y_marker tetap None
else: # Kedua garis non-vertikal
    if abs(y1_coba_raw - y2_coba_raw) < tolerance: # Jika sudah dekat
        plot_y_marker = (y1_coba_raw + y2_coba_raw) / 2
    else: # Jika belum dekat, plot di titik coba x
        # Untuk visualisasi, kita bisa plot kedua titik y saat ini
        # Namun, plot_garis hanya mendukung 1 titik marker.
        # Kita akan plot titik tengah antara y1_coba_raw dan y2_coba_raw di x_coba
        plot_y_marker = (y1_coba_raw + y2_coba_raw) / 2

# Pastikan plot_y_marker bukan NaN atau Inf
if plot_y_marker is not None and (np.isnan(plot_y_marker) or np.isinf(plot_y_marker)):
    plot_y_marker = None
if plot_x_marker is not None and (np.isnan(plot_x_marker) or np.isinf(plot_x_marker)):
    plot_x_marker = None


fig = plot_garis(persamaan1, persamaan2, x_range, line1_color, line2_color,
                 point_x=plot_x_marker, point_y=plot_y_marker, show_exact_point=False)
st.pyplot(fig)
st.caption("Titik ungu pada grafik menunjukkan perkiraan titik potong berdasarkan nilai X coba Anda.")


# --- Bagian Solusi Matematis (untuk konfirmasi) ---
st.header("4. Konfirmasi Solusi Matematis (Opsional)")
st.markdown("Jika Anda ingin mengkonfirmasi jawaban atau kesulitan menemukannya, Anda bisa melihat solusi matematisnya di sini.")

with st.expander("Klik untuk Menampilkan Solusi Matematis"):
    solusi_x, solusi_y = hitung_solusi_spldv(persamaan1, persamaan2)

    if solusi_x is not None and solusi_y is not None:
        if solusi_x == float('inf') and solusi_y == float('inf'):
            st.info("ℹ️ Kedua persamaan adalah **garis yang sama**. Terdapat **tak terhingga solusi**.")
        else:
            st.success(f"✅ Secara matematis, titik potongnya adalah: $x = \\mathbf{{{solusi_x:.4f}}}$, $y = \\mathbf{{{solusi_y:.4f}}}$")
            st.markdown(f"**Titik potong akurat:** $\\left({solusi_x:.4f}, {solusi_y:.4f}\\right)$")
            # Tambahkan plot solusi matematis
            st.markdown("---")
            st.subheader("Plot dengan Titik Solusi Akurat")
            fig_sol = plot_garis(persamaan1, persamaan2, x_range, line1_color, line2_color,
                                 point_x=solusi_x, point_y=solusi_y, show_exact_point=True)
            st.pyplot(fig_sol)
            st.caption("Titik hijau pada grafik ini menunjukkan titik potong yang akurat secara matematis.")

    else:
        st.error("❌ Tidak ada solusi unik. Kedua garis **paralel** dan tidak berpotongan.")

st.markdown("---")
st.markdown("Dibuat dengan Python oleh **rarayuniaini** | Universitas Pekalongan")
st.markdown("---")
