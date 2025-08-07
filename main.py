import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu

# Load data
data_peternak = pd.read_excel("pendataan_peternak.xlsx")
data_peternak.set_index("No", inplace=True)

# Hitung total ternak per RT
total_per_rt = data_peternak.groupby("RT")[["Sapi", "Kambing", "Ayam"]].sum().reset_index()

# Hitung total keseluruhan ternak
total_keseluruhan = pd.DataFrame([{
    "Sapi": data_peternak["Sapi"].sum(),
    "Kambing": data_peternak["Kambing"].sum(),
    "Ayam": data_peternak["Ayam"].sum()
}])

# Navigasi
with st.sidebar:
    menu = option_menu(
        "📌 Menu Navigasi",
        ["📖 Profil Padukuhan Besole", "📊 Dashboard Data Pertanian"],
        menu_icon="list",
        default_index=0,
    )

# Halaman Profil
if menu == "📖 Profil Padukuhan Besole":
    st.markdown("## 📖 Profil Padukuhan Besole")

    st.markdown("""
    **Padukuhan Besole** terletak di Kelurahan **Purwoharjo**, Kecamatan **Samigaluh**, Kabupaten **Kulon Progo**, DIY.
    Berada di ketinggian sekitar **500 meter di atas permukaan laut**, wilayah ini dikelilingi oleh alam yang **asri dan hijau**.

    ### 🧭 Batas Wilayah
    Padukuhan Besole berbatasan langsung dengan:
    - **Padukuhan Sendangrejo**
    - **Padukuhan Pagutan**
    - **Padukuhan Junut**
    - **Kalurahan Banjarsari**

    ### 👥 Pembagian Wilayah
    Padukuhan Besole terdiri dari 2 Rukun Warga (RW), yaitu RW 17 dan RW 18, yang terbagi ke dalam 4 Rukun Tetangga (RT), yakni RT 34, 35, 36, dan 37.

    ### 💼 Mata Pencaharian
    Mayoritas penduduk Padukuhan Besole bekerja sebagai:
    - **Petani**
    Dari total 157 warga, terdapat 54 orang yang bekerja sebagai petani. Namun, hasil pertanian ini umumnya digunakan untuk konsumsi sehari-hari dan bukan untuk dijual secara komersial.
    - **Peternak**
    Di antara para petani tersebut, sekitar 30 orang juga memiliki ternak. Penduduk lebih banyak menggantungkan penghasilan dari sektor peternakan, yang menjadi sumber utama ekonomi keluarga.

    ### 🕌 Fasilitas Umum
    - **Mushola Al-Fajar**: Digunakan untuk TPA dua kali seminggu dan pengajian malam Jumat.
    - **Masjid Nurul Muttaqin**: Tempat ibadah salat lima waktu.
    - **PAUD Srikandi**: Pendidikan anak usia dini.
    """)

    # Peta
    st.markdown("### 🗺️ Lokasi Padukuhan Besole")
    besole_coords = [-7.694674460180705, 110.18253469645788]
    m = folium.Map(location=besole_coords, zoom_start=15)

    folium.Marker(
        location=besole_coords,
        popup="Padukuhan Besole",
        tooltip="Lokasi Padukuhan Besole",
        icon=folium.Icon(color="green", icon="home")
    ).add_to(m)

    st_folium(m, width=700, height=500)



# Halaman Dashboard
elif menu == "📊 Dashboard Data Pertanian":
    st.title("📊 Dashboard Pendataan Peternak Warga")

    # Mapping RW berdasarkan RT
    def map_rt_to_rw(rt):
        if rt in [34, 35]:
            return "RW 17"
        elif rt in [36, 37]:
            return "RW 18"
        else:
            return "Lainnya"

    data_peternak["RW"] = data_peternak["RT"].apply(map_rt_to_rw)

    # === Sidebar ===
    st.sidebar.header("🔎 Filter Data")

    # Pilihan mode filter
    filter_mode = st.sidebar.radio(
        "Filter berdasarkan:", ["RW", "RT"]
    )

    # Filter data berdasarkan pilihan
    if filter_mode == "RW":
        selected_rw = st.sidebar.multiselect(
            "Pilih RW", 
            options=sorted(data_peternak["RW"].unique()),
            default=sorted(data_peternak["RW"].unique())
        )
        filtered_data = data_peternak[data_peternak["RW"].isin(selected_rw)]

    elif filter_mode == "RT":
        selected_rt = st.sidebar.multiselect(
            "Pilih RT",
            options=sorted(data_peternak["RT"].unique()),
            default=sorted(data_peternak["RT"].unique())
        )
        filtered_data = data_peternak[data_peternak["RT"].isin(selected_rt)]

    # === Dataframe ===
    st.subheader("📄 Data Peternak")
    st.dataframe(filtered_data, use_container_width=True)

    # === Bar chart per RT ===
    st.subheader("📊 Total Ternak per RT")
    total_per_rt = filtered_data.groupby("RT")[["Sapi", "Kambing", "Ayam"]].sum().reset_index()
    fig_rt = px.bar(
        total_per_rt,
        x="RT", y=["Sapi", "Kambing", "Ayam"],
        barmode="group",
    )
    st.plotly_chart(fig_rt, use_container_width=True)

    # === Bar chart per RW ===
    st.subheader("🏘️ Total Ternak per RW")
    total_per_rw = filtered_data.groupby("RW")[["Sapi", "Kambing", "Ayam"]].sum().reset_index()
    fig_rw = px.bar(
        total_per_rw,
        x="RW", y=["Sapi", "Kambing", "Ayam"],
        barmode="group",
    )
    st.plotly_chart(fig_rw, use_container_width=True)

    # === Pie chart total ===
    st.subheader("🥧 Distribusi Ternak Keseluruhan")
    total_all = filtered_data[["Sapi", "Kambing", "Ayam"]].sum()
    fig_pie = px.pie(
        names=total_all.index,
        values=total_all.values,
    )
    st.plotly_chart(fig_pie, use_container_width=True)
