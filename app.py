import streamlit as st
import numpy as np

st.set_page_config(page_title="SPK Laptop - AHP", layout="wide")
st.title("Sistem Pendukung Keputusan Laptop (Metode AHP)")

# ===============================
# KRITERIA
# ===============================
kriteria = [
    "Harga", "Performa", "RAM", "GPU",
    "Merek", "Kegiatan", "Baterai", "Portabilitas"
]
nK = len(kriteria)

st.subheader("Matriks Perbandingan Kriteria (Skala Saaty 1–9)")

matrix = np.ones((nK, nK))

cols = st.columns(nK + 1)
cols[0].write("Kriteria")

for i in range(nK):
    cols[i + 1].write(kriteria[i])

for i in range(nK):
    row = st.columns(nK + 1)
    row[0].write(kriteria[i])

    for j in range(nK):
        if i == j:
            row[j + 1].write("1")
        elif i < j:
            matrix[i][j] = row[j + 1].number_input(
                "", min_value=0.11, max_value=9.0,
                value=1.0, step=0.1, key=f"k{i}{j}"
            )
            matrix[j][i] = 1 / matrix[i][j]
        else:
            row[j + 1].write(f"{matrix[i][j]:.4f}")

# ===============================
# EIGEN PRIORITY
# ===============================
def eigen_priority(matrix):
    col_sum = matrix.sum(axis=0)
    norm = matrix / col_sum
    return norm.mean(axis=1)

bobot = eigen_priority(matrix)

st.subheader("Bobot Kriteria")
for k, b in zip(kriteria, bobot):
    st.write(f"{k} : {b:.4f}")

# ===============================
# ALTERNATIF
# ===============================
st.subheader("Nilai Alternatif Laptop")

alternatif = [
    "Asus Vivobook 14",
    "HP Pavilion Aero 13",
    "Dell Inspiron 14 5000",
    "ASUS TUF Gaming F15",
    "MSI Modern 14 C13M"
]

nilai_alt = []

for alt in alternatif:
    st.markdown(f"**{alt}**")
    cols = st.columns(nK)
    values = []
    for j in range(nK):
        values.append(cols[j].number_input(
            kriteria[j], 1, 10, 5, key=f"{alt}{j}"
        ))
    nilai_alt.append(values)

# ===============================
# PROSES AHP
# ===============================
if st.button("Hitung AHP"):
    hasil = []
    for nama, nilai in zip(alternatif, nilai_alt):
        skor = np.dot(nilai, bobot)
        hasil.append((nama, skor))

    hasil.sort(key=lambda x: x[1], reverse=True)

    st.subheader("Hasil Perangkingan")
    for i, (nama, skor) in enumerate(hasil, 1):
        st.write(f"{i}. **{nama}** → {skor:.4f}")
