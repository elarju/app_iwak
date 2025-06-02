import streamlit as st # type: ignore
import json
import os
import time

# --- Konfigurasi Halaman (Pastikan ini ada di paling atas file .py) ---
st.set_page_config(
    page_title="Iwak App | Fisch-RBL",
    page_icon="🐟",
    layout="centered"
)

# --- Nama File Database (JSON) ---
DATA_FILE = "D:/Iwak/app/iwak_data.json"

# --- Fungsi untuk Memuat dan Menyimpan Data ---
def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "fish_types": [],
            "mutation_types": []
        }
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    # Buat direktori jika belum ada (untuk memastikan path-nya aman)
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- Inisialisasi Data ke Session State ---
if 'data' not in st.session_state:
    st.session_state.data = load_data()

# --- Fungsi CRUD untuk Jenis Ikan (Tetap ada fungsinya, cuma formnya aja yang diilangin) ---
def add_fish(name, leverage):
    if name and leverage is not None:
        if not any(f['name'].lower() == name.lower() for f in st.session_state.data['fish_types']):
            st.session_state.data['fish_types'].append({"name": name, "leverage": leverage})
            save_data(st.session_state.data)
            return {"type": "success", "content": f"Jenis ikan <span style='color: #FFD700;'>{name}</span> berhasil ditambahkan!"}
        else:
            return {"type": "warning", "content": f"Jenis ikan <span style='color: orange;'>{name}</span> sudah ada."}
    else:
        return {"type": "error", "content": "Nama ikan dan leverage tidak boleh kosong."}

def update_fish(old_name, new_name, new_leverage):
    if old_name and new_name and new_leverage is not None:
        if old_name != new_name and any(f['name'].lower() == new_name.lower() for f in st.session_state.data['fish_types']):
            return {"type": "error", "content": f"Nama ikan <span style='color: red;'>{new_name}</span> sudah ada. Pilih nama lain."}

        found = False
        for i, fish in enumerate(st.session_state.data['fish_types']):
            if fish['name'] == old_name:
                st.session_state.data['fish_types'][i] = {"name": new_name, "leverage": new_leverage}
                save_data(st.session_state.data)
                found = True
                return {"type": "success", "content": f"Ikan <span style='color: #FFD700;'>{new_name}</span> berhasil diupdate"}
        if not found:
            return {"type": "error", "content": f"Jenis ikan <span style='color: red;'>{old_name}</span> tidak ditemukan."}
    else:
        return {"type": "error", "content": "Semua input untuk update ikan tidak boleh kosong."}

def delete_fish(name):
    initial_len = len(st.session_state.data['fish_types'])
    st.session_state.data['fish_types'] = [f for f in st.session_state.data['fish_types'] if f['name'] != name]
    if len(st.session_state.data['fish_types']) < initial_len:
        save_data(st.session_state.data)
        return {"type": "success", "content": f"Ikan <span style='color: #FFD700;'>{name}</span> berhasil dihapus!"}
    else:
        return {"type": "warning", "content": f"Ikan <span style='color: orange;'>{name}</span> ga ada lol :)"}

# --- Fungsi CRUD untuk Jenis Mutasi (Tetap ada fungsinya, cuma formnya aja yang diilangin) ---
def add_mutation(name, leverage):
    if name and leverage is not None:
        if not any(m['name'].lower() == name.lower() for m in st.session_state.data['mutation_types']):
            st.session_state.data['mutation_types'].append({"name": name, "leverage": leverage})
            save_data(st.session_state.data)
            return {"type": "success", "content": f"Jenis mutasi **{name}** berhasil ditambahkan!"}
        else:
            return {"type": "warning", "content": f"Jenis mutasi **{name}** sudah ada."}
    else:
        return {"type": "error", "content": "Nama mutasi dan leverage tidak boleh kosong."}

def update_mutation(old_name, new_name, new_leverage):
    if old_name and new_name and new_leverage is not None:
        if old_name != new_name and any(m['name'].lower() == new_name.lower() for m in st.session_state.data['mutation_types']):
            return {"type": "error", "content": f"Nama mutasi **{new_name}** sudah ada. Pilih nama lain."}

        found = False
        for i, mut in enumerate(st.session_state.data['mutation_types']):
            if mut['name'] == old_name:
                st.session_state.data['mutation_types'][i] = {"name": new_name, "leverage": new_leverage}
                save_data(st.session_state.data)
                found = True
                return {"type": "success", "content": f"Mutasi **{old_name}** berhasil diupdate menjadi ***{new_name}***."}
        if not found:
            return {"type": "error", "content": f"Jenis mutasi **{old_name}** tidak ditemukan."}
    else:
        return {"type": "error", "content": "Semua input untuk update mutasi tidak boleh kosong."}

def delete_mutation(name):
    initial_len = len(st.session_state.data['mutation_types'])
    st.session_state.data['mutation_types'] = [m for m in st.session_state.data['mutation_types'] if m['name'] != name]
    if len(st.session_state.data['mutation_types']) < initial_len:
        save_data(st.session_state.data)
        return {"type": "success", "content": f"Mutasi **{name}** berhasil dihapus!"}
    else:
        return {"type": "warning", "content": f"Mutasi **{name}** ga ada lol :)"}

# --- Judul Aplikasi ---
st.title("🐟 Timbang Iwak")
st.markdown(
    """
    Hitung Perkiraan Harga Ikan di Fisch - RBL.
    """
)

# --- Tabs (Pemisah Halaman) ---
tab_calculator, tab_fish_mgmt, tab_mutation_mgmt, tab_target_price = st.tabs(
    ["Hitung Iwak", "Nama Iwak", "Mutasi", "Target Harga"]
)

with tab_calculator:
    st.header("⚙️ Yuk, Atur Spek Iwakmu!")
    st.markdown("""
        Pilih jenis ikan, masukkan berat, dan centang kalo ada mutasi atau atribut spesial.
        Nanti harga ikanmu langsung dihitung otomatis!
    """)

    # Mengurangi spasi dengan custom HTML hr
    st.markdown("<hr style='margin: 0.5em 0;'>", unsafe_allow_html=True)

    # Kolom untuk Nama Iwak (Kiri Atas) dan Mutasi (Kanan Atas)
    col_fish_type, col_mutation = st.columns(2)

    with col_fish_type:
        st.markdown("##### 🐟 Pilih Jenis Iwakmu")
        
        # Ambil semua nama ikan dari session_state dan urutkan
        all_fish_names = [f['name'] for f in st.session_state.data['fish_types']]
        all_fish_names.sort() # Mengurutkan secara abjad (A-Z)

        fish_names_for_selectbox = ["Pilih Jenis Iwak..."] + all_fish_names
        selected_fish_name = st.selectbox(
            "**Nama Iwak:**",
            fish_names_for_selectbox,
            index=0,
            help="Wajib dipilih ya, Bos. Kalau belum ada, tambahin di tab 'Nama Iwak' dulu.",
            key='calculator_main_fish_select' # Key unik
        )
        
        leverage_ikan = 1.0
        if selected_fish_name != "Pilih Jenis Iwak...":
            for fish in st.session_state.data['fish_types']:
                if fish['name'] == selected_fish_name:
                    leverage_ikan = fish['leverage']
                    break

    with col_mutation:
        st.markdown("##### 🧬 Pilih Mutasi")
        
        # Ambil semua nama mutasi dari session_state dan urutkan
        all_mutation_names = [m['name'] for m in st.session_state.data['mutation_types']]
        all_mutation_names.sort() # Mengurutkan secara abjad (A-Z)

        mutation_names = ["Ga ada mutasi"] + all_mutation_names
        selected_mutasi = st.selectbox(
            "**Jenis Mutasi:**",
            mutation_names,
            index=0,
            help="Pilih **'Ga ada mutasi'** kalau iwakmu normal aja.",
            key='calculator_main_mutation_select' # Key unik
        )

        leverage_mutasi = 1.0
        if selected_mutasi != "Ga ada mutasi":
            for mut in st.session_state.data['mutation_types']:
                if mut['name'] == selected_mutasi:
                    leverage_mutasi = mut['leverage']
                    break

    # Mengurangi spasi dengan custom HTML hr
    st.markdown("<hr style='margin: 0.5em 0;'>", unsafe_allow_html=True)

    # Bagian Atribut Shiny & Sparkling (di bawah, bersebelahan)
    st.markdown("##### ✨ Atribut Spesial (Opsional)")
    col_shiny, col_sparkling = st.columns(2)

    LEVERAGE_SHINY_FIXED = 1.85
    LEVERAGE_SPARKLING_FIXED = 1.85

    with col_shiny:
        is_shiny = st.checkbox(
            f"**Shiny**",
            key='calculator_main_shiny_checkbox'
        )
        leverage_shiny = LEVERAGE_SHINY_FIXED if is_shiny else 1.0

    with col_sparkling:
        is_sparkling = st.checkbox(
            f"**Sparkling**",
            key='calculator_main_sparkling_checkbox'
        )
        leverage_sparkling = LEVERAGE_SPARKLING_FIXED if is_sparkling else 1.0

    # Mengurangi spasi dengan custom HTML hr
    st.markdown("<hr style='margin: 0.5em 0;'>", unsafe_allow_html=True)

    # --- Bagian Input Berat Iwak Dinamis & Hasil Per Iwak ---
    st.markdown("##### ⚖️ Masukkan Berat Iwak & Lihat Harga Per Item")

    # Inisialisasi jumlah input berat
    if 'num_berat_inputs' not in st.session_state:
        st.session_state.num_berat_inputs = 1
    
    # Batasan jumlah input
    MAX_WEIGHT_INPUTS = 10

    # List untuk menyimpan semua berat ikan yang diinput
    berat_iwak_list = []
    # List untuk menyimpan harga per ikan untuk dihitung total nanti
    prices_per_fish_for_total = []

    # Loop untuk menampilkan input berat dan hasilnya
    for i in range(st.session_state.num_berat_inputs):
        # Buat kolom untuk input berat dan hasil per ikan
        col_input_berat, col_hasil_berat = st.columns([0.6, 0.4]) # Rasio lebar kolom

        with col_input_berat:
            berat_input = st.number_input(
                f"Berat Iwak #{i+1} (kg)",
                min_value=0.0,
                value=0.0,
                step=0.1,
                format="%.1f",
                key=f"berat_iwak_input_{i}" # Key unik untuk setiap input
            )
            berat_iwak_list.append(float(berat_input) if berat_input is not None else 0.0)

        with col_hasil_berat:
            # Kalkulasi harga untuk input berat ini
            if selected_fish_name != "Pilih Jenis Iwak..." and berat_iwak_list[i] > 0:
                calc_leverage_ikan = leverage_ikan if leverage_ikan is not None else 1.0
                calc_berat_ikan = berat_iwak_list[i] if berat_iwak_list[i] is not None else 1.0
                calc_leverage_mutasi = leverage_mutasi if leverage_mutasi is not None else 1.0
                calc_leverage_shiny = leverage_shiny if leverage_shiny is not None else 1.0
                calc_leverage_sparkling = leverage_sparkling if leverage_sparkling is not None else 1.0

                final_price_per_fish = (
                    calc_leverage_shiny *
                    calc_leverage_sparkling *
                    calc_leverage_mutasi *
                    calc_leverage_ikan *
                    calc_berat_ikan
                )
                prices_per_fish_for_total.append(final_price_per_fish) # Simpan untuk total nanti

                # Format harga per ikan dengan pemisah ribuan (titik)
                st.markdown(f"<div style='background-color: #333333; padding: 10px; border-radius: 5px; margin-top: 28px; text-align: center;'>"
                            f"<span style='color: #FFD700; font-weight: bold;'>{final_price_per_fish:,.0f} Coin</span></div>", 
                            unsafe_allow_html=True)
            else:
                prices_per_fish_for_total.append(0.0) # Jika tidak dihitung, anggap 0
                st.markdown(f"<div style='background-color: #333333; padding: 10px; border-radius: 5px; margin-top: 28px; text-align: center;'>"
                            f"<span style='color: #AAAAAA; font-weight: bold;'>0 Coin</span></div>", 
                            unsafe_allow_html=True) # Tampilan default jika belum valid/0

    # Tombol Tambah/Kurang Input Berat
    col_add_btn, col_remove_btn = st.columns(2)
    with col_add_btn:
        if st.button("➕ Tambah Input Berat", use_container_width=True, disabled=(st.session_state.num_berat_inputs >= MAX_WEIGHT_INPUTS)):
            st.session_state.num_berat_inputs += 1
            st.rerun() # Rerun agar input baru muncul

    with col_remove_btn:
        if st.button("➖ Kurangi Input Berat", use_container_width=True, disabled=(st.session_state.num_berat_inputs <= 1)):
            st.session_state.num_berat_inputs -= 1
            st.rerun() # Rerun agar input hilang

    # Mengurangi spasi dengan custom HTML hr
    st.markdown("<hr style='margin: 0.5em 0;'>", unsafe_allow_html=True)

    # --- Kalkulasi TOTAL Harga (SEKARANG BENERAN DI BAWAH) ---
    st.header("💰 Estimasi Total Harga Iwakmu!")

    # Cek kondisi minimal untuk menampilkan TOTAL harga: nama ikan sudah dipilih dan minimal ada 1 berat > 0
    if selected_fish_name != "Pilih Jenis Iwak..." and any(b > 0 for b in berat_iwak_list):
        total_final_price = sum(prices_per_fish_for_total) # Jumlahkan semua harga per ikan yang sudah dihitung

        if total_final_price == 0: # Jika semua berat 0 setelah filter
             st.warning("⚠️ Belum ada iwak yang dihitung. Masukkan berat iwak yang valid ya!")
        else:
            # Format total harga dengan pemisah ribuan (titik)
            st.success(f"### 🎉 TOTAL HARGA SEMUA IWAK: **{total_final_price:,.0f} Coin** $")
    else:
        # Tampilkan pesan kalau belum memenuhi syarat untuk kalkulasi TOTAL
        if selected_fish_name == "Pilih Jenis Iwak...":
            st.info("Pilih **Jenis Iwak** dulu ya, Bos, biar totalnya bisa dihitung.")
        elif all(b <= 0 for b in berat_iwak_list):
            st.info("Masukin minimal **satu Berat Iwak** yang valid dulu ya, Bos, biar totalnya bisa dihitung.")

# --- Tab Manajemen Jenis Ikan ---
with tab_fish_mgmt:
    st.header("Manajemen Jenis Ikan")
    st.write("Tambah, ubah, atau hapus jenis ikan dan nilai leveragenya.")

   # Tampilkan Data Saat Ini
    st.subheader("Daftar Jenis Ikan Saat Ini:")
    sorted_fish_types = sorted(st.session_state.data['fish_types'], key=lambda x: x['name'].lower())
    st.dataframe(sorted_fish_types, use_container_width=True)

    # --- Hapus semua bagian Tambah, Update, Hapus ---
    # GemiKan v2 sengaja biarkan bagian ini kosong, agar tidak ada form CUD
    # st.write("---") 
    # st.subheader("Tambah Ikan Baru")
    # ... (form tambah ikan) ...
    # st.write("---")
    # st.subheader("Ubah Nama Ikan")
    # ... (form ubah ikan) ...
    # st.write("---")
    # st.subheader("Hapus Ikan")
    # ... (form hapus ikan) ...

# --- Tab Manajemen Jenis Mutasi ---
with tab_mutation_mgmt:
    st.header("Manajemen Mutasi")
    st.write("Tambah, ubah, atau hapus jenis mutasi dan nilai leveragenya.")

    # Tampilkan Data Saat Ini
    st.subheader("Daftar Jenis Mutasi Saat Ini:")
    sorted_mutation_types = sorted(st.session_state.data['mutation_types'], key=lambda x: x['name'].lower())
    st.dataframe(sorted_mutation_types, use_container_width=True)

    # --- Hapus semua bagian Tambah, Update, Hapus ---
    # GemiKan v2 sengaja biarkan bagian ini kosong, agar tidak ada form CUD
    # st.write("---")
    # st.subheader("Tambah Jenis Mutasi Baru")
    # ... (form tambah mutasi) ...
    # st.write("---")
    # st.subheader("Ubah Jenis Mutasi")
    # ... (form ubah mutasi) ...
    # st.write("---")
    # st.subheader("Hapus Jenis Mutasi")
    # ... (form hapus mutasi) ...

# --- Tab Target Harga (NEW) ---
with tab_target_price:
    st.header("🎯 Cari Berat Iwak Idealmu Berdasarkan Harga Target!")
    st.markdown("""
        Punya target harga koin tertentu? Masukkan targetmu di sini (dalam satuan M, misal `2.5` = `2.500.000`),
        pilih jenis ikan, mutasi, dan atribut spesial. Berat ideal iwak akan langsung muncul!
    """)

    # Mengurangi spasi dengan custom HTML hr
    st.markdown("<hr style='margin: 0.5em 0;'>", unsafe_allow_html=True)

    # Input Harga Target
    target_price_input = st.number_input( # Mengubah nama variabel untuk kejelasan
        "**Target Coin:** (M)",
        min_value=0.0,
        value=1.0, # Default 1.0 berarti 1.000.000
        step=0.5,  # Step 0.1 berarti 100.000
        format="%.1f",
        help="Contoh: `2.5` = `2.500.000` Coin."
    )
    # Mengalikan input dengan 1.000.000
    target_price = target_price_input * 1_000_000 

    # Mengurangi spasi dengan custom HTML hr
    st.markdown("<hr style='margin: 0.5em 0;'>", unsafe_allow_html=True)

    # Kolom untuk Nama Iwak (Kiri Atas) dan Mutasi (Kanan Atas) - Sama seperti tab Hitung Iwak
    col_fish_type_target, col_mutation_target = st.columns(2)

    with col_fish_type_target:
        st.markdown("##### 🐟 Pilih Jenis Iwakmu")
        
        # Ambil semua nama ikan dari session_state dan urutkan untuk tab Target Harga
        all_fish_names_target = [f['name'] for f in st.session_state.data['fish_types']]
        all_fish_names_target.sort() # Mengurutkan secara abjad (A-Z)

        fish_names_for_selectbox_target = ["Pilih Jenis Iwak..."] + all_fish_names_target
        selected_fish_name_target = st.selectbox(
            "**Nama Iwak:**",
            fish_names_for_selectbox_target,
            index=0,
            help="Wajib dipilih ya, Bos. Kalau belum ada, tambahin di tab 'Nama Iwak' dulu.",
            key='target_price_fish_select' # Key unik untuk tab ini
        )
        
        leverage_ikan_target = 1.0
        if selected_fish_name_target != "Pilih Jenis Iwak...":
            for fish in st.session_state.data['fish_types']:
                if fish['name'] == selected_fish_name_target:
                    leverage_ikan_target = fish['leverage']
                    break

    with col_mutation_target:
        st.markdown("##### 🧬 Pilih Mutasi")
        
        # Ambil semua nama mutasi dari session_state dan urutkan untuk tab Target Harga
        all_mutation_names_target = [m['name'] for m in st.session_state.data['mutation_types']]
        all_mutation_names_target.sort() # Mengurutkan secara abjad (A-Z)

        mutation_names_target = ["Ga ada mutasi"] + all_mutation_names_target
        selected_mutasi_target = st.selectbox(
            "**Jenis Mutasi:**",
            mutation_names_target,
            index=0,
            help="Pilih **'Ga ada mutasi'** kalau iwakmu normal aja.",
            key='target_price_mutation_select' # Key unik untuk tab ini
        )

        leverage_mutasi_target = 1.0
        if selected_mutasi_target != "Ga ada mutasi":
            for mut in st.session_state.data['mutation_types']:
                if mut['name'] == selected_mutasi_target:
                    leverage_mutasi_target = mut['leverage']
                    break

    # Mengurangi spasi dengan custom HTML hr
    st.markdown("<hr style='margin: 0.5em 0;'>", unsafe_allow_html=True)

    # Bagian Atribut Shiny & Sparkling (Opsional) - Sama seperti tab Hitung Iwak
    st.markdown("##### ✨ Atribut Spesial (Opsional)")
    col_shiny_target, col_sparkling_target = st.columns(2)

    LEVERAGE_SHINY_FIXED = 1.85 # Tetap pakai konstanta yang sama
    LEVERAGE_SPARKLING_FIXED = 1.85 # Tetap pakai konstanta yang sama

    with col_shiny_target:
        is_shiny_target = st.checkbox(
            f"**Shiny**",
            key='target_price_shiny_checkbox' # Key unik untuk tab ini
        )
        leverage_shiny_target = LEVERAGE_SHINY_FIXED if is_shiny_target else 1.0

    with col_sparkling_target:
        is_sparkling_target = st.checkbox(
            f"**Sparkling**",
            key='target_price_sparkling_checkbox' # Key unik untuk tab ini
        )
        leverage_sparkling_target = LEVERAGE_SPARKLING_FIXED if is_sparkling_target else 1.0

    # Mengurangi spasi dengan custom HTML hr
    st.markdown("<hr style='margin: 0.5em 0;'>", unsafe_allow_html=True)

    st.header("⚖️ Berat Iwak Idealmu:")

    # Logika Kalkulasi Berat Ideal
    if selected_fish_name_target != "Pilih Jenis Iwak..." and target_price > 0:
        # Hitung total leverage dari semua faktor
        total_leverage = (
            leverage_ikan_target *
            leverage_mutasi_target *
            leverage_shiny_target *
            leverage_sparkling_target
        )

        if total_leverage > 0: # Hindari pembagian dengan nol
            ideal_weight = target_price / total_leverage
            # Format berat ideal dengan pemisah ribuan (titik)
            st.success(f"### ✨ Berat Iwak Idealmu: **{ideal_weight:,.2f} kg**")
            st.info("Ini adalah berat **per satu ekor** iwak untuk mencapai harga target.")
        else:
            st.warning("⚠️ Kombinasi pilihanmu tidak menghasilkan leverage yang valid (mungkin leverage ikan 0 atau masalah data).")
    else:
        if selected_fish_name_target == "Pilih Jenis Iwak...":
            st.info("Pilih **Jenis Iwak** dulu ya, Bos, biar berat idealnya bisa dihitung.")
        elif target_price <= 0:
            st.info("Masukkan **Harga Target** yang valid (lebih dari 0) ya, Bos.")
