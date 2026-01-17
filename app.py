import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="SPK Laptop AHP", layout="wide")
st.markdown("""
<style>
/* Tombol utama */
.stButton > button {
    background-color: #d81b60;      /* pink tua */
    color: white;
    border-radius: 12px;
    border: none;
    font-weight: 600;
    height: 3em;
    width: 100%;
    transition: 0.3s;
}

/* Hover */
.stButton > button:hover {
    background-color: #ad1457;      /* lebih gelap saat hover */
    color: white;
}

/* Tombol ditekan */
.stButton > button:active {
    background-color: #880e4f;
}

/* Disabled */
.stButton > button:disabled {
    background-color: #f3a1c4;
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
button[kind="secondary"] {
    background-color: #c2185b !important;
    color: white !important;
}
button[kind="secondary"]:hover {
    background-color: #880e4f !important;
}
</style>
""", unsafe_allow_html=True)

st.title("Sistem Pendukung Keputusan Laptop (Metode AHP)")

# ===============================
# KRITERIA
# ===============================
kriteria = [
    "Harga", "Performa", "RAM", "GPU",
    "Merek", "Kegiatan", "Baterai", "Portabilitas"
]
nK = len(kriteria)

# ===============================
# DATA DEFAULT (TERKUNCI)
# ===============================
data_default = [
    ["Asus Vivobook 14", 8, 6, 6, 5, 7, 6, 7, 6],
    ["HP Pavilion Aero 13", 6, 7, 6, 5, 9, 7, 8, 7],
    ["Dell Inspiron 14 5000", 7, 6, 6, 5, 6, 6, 8, 6],
    ["ASUS TUF Gaming F15", 5, 8, 7, 8, 4, 5, 7, 9],
    ["MSI Modern 14 C13M", 7, 7, 6, 5, 8, 7, 7, 7],
]

if "laptops" not in st.session_state:
    st.session_state.laptops = data_default.copy()

# ===============================
# MATRKS PERBANDINGAN AHP
# ===============================
st.subheader("Matriks Perbandingan Kriteria (AHP)")
matrix = np.ones((nK, nK))

for i in range(nK):
    cols = st.columns(nK + 1)
    cols[0].write(kriteria[i])
    for j in range(nK):
        if i == j:
            cols[j + 1].write("1")
        elif i < j:
            matrix[i][j] = cols[j + 1].number_input(
                f"{kriteria[i]} vs {kriteria[j]}",
                0.11, 9.0, 1.0, 0.1, key=f"k{i}{j}"
            )
            matrix[j][i] = 1 / matrix[i][j]
        else:
            cols[j + 1].write(f"{matrix[i][j]:.4f}")

def eigen_priority(matrix):
    col_sum = matrix.sum(axis=0)
    norm = matrix / col_sum
    return norm.mean(axis=1)

bobot = eigen_priority(matrix)

st.subheader("Bobot Kriteria")
for k, b in zip(kriteria, bobot):
    st.write(f"{k} : {b:.4f}")

# ===============================
# TAMBAH LAPTOP (USER ONLY)
# ===============================
st.subheader("Tambah Laptop Baru")

with st.expander("Form Input Laptop"):
    nama = st.text_input("Nama Laptop")
    cols = st.columns(nK)
    values = [cols[i].number_input(k, 1, 10, 5) for i, k in enumerate(kriteria)]

    if st.button("Simpan Laptop"):
        if nama:
            st.session_state.laptops.append([nama] + values)
            st.success(f"{nama} berhasil ditambahkan")
        else:
            st.error("Nama laptop wajib diisi!")

# ===============================
# TABEL DATA (READ-ONLY)
# ===============================
df = pd.DataFrame(
    st.session_state.laptops,
    columns=["Nama"] + kriteria
)

st.subheader("Daftar Laptop (Data Terkunci)")
st.dataframe(df, use_container_width=True)

# ===============================
# HAPUS LAPTOP
# ===============================
st.subheader("Hapus Laptop")

col1, col2 = st.columns([3, 1])

with col1:
    index = st.selectbox(
        "Pilih laptop yang ingin dihapus",
        df.index,
        format_func=lambda x: df.loc[x, "Nama"]
    )

with col2:
    st.write("")  # spacer
    if st.button("Hapus"):
        nama = st.session_state.laptops[index][0]
        st.session_state.laptops.pop(index)
        st.success(f"{nama} berhasil dihapus")
        st.experimental_rerun()


# ===============================
# PROSES AHP
# ===============================
if st.button("--Hitung AHP--"):
    hasil = []

    for row in st.session_state.laptops:
        nama = row[0]
        skor = np.dot(row[1:], bobot)
        hasil.append((nama, skor))

    hasil.sort(key=lambda x: x[1], reverse=True)


    st.snow()

    st.subheader("🏆 Hasil Perangkingan")
    for i, (nama, skor) in enumerate(hasil, 1):
        st.write(f"{i}. **{nama}** → {skor:.4f}")

    st.success(f"Laptop terbaik: **{hasil[0][0]}**")
