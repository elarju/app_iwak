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
DATA_FILE = "../iwak_data.json" # <--- INI SUDAH DIBENERIN!

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

# --- Fungsi CRUD untuk Jenis Ikan ---
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
        # Validasi tambahan: Cek kalau nama baru sudah ada (tapi bukan nama yang lama)
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

# --- Fungsi CRUD untuk Jenis Mutasi ---
def add_mutation(name, leverage):
    if name and leverage is not None:
        if not any(m['name'].lower() == name.lower() for m in st.session_state.data['mutation_types']): # Tambahan .lower()
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
tab_calculator, tab_fish_mgmt, tab_mutation_mgmt = st.tabs(
    ["Hitung Iwak", "Nama Iwak", "Mutasi"]
)

with tab_calculator:
    st.header("⚙️ Yuk, Atur Spek Iwakmu!")
    st.markdown("""
        Pilih jenis ikan, masukkan berat, dan centang kalo ada mutasi atau atribut spesial.
        Nanti harga ikanmu langsung dihitung otomatis!
    """)

    st.write("---")

    # Kolom untuk Nama Iwak (Kiri Atas) dan Mutasi (Kanan Atas)
    col_fish_type, col_mutation = st.columns(2)

    with col_fish_type:
        st.markdown("##### 🐟 Pilih Jenis Iwakmu")
        fish_names_for_selectbox = ["Pilih Jenis Iwak..."] + [f['name'] for f in st.session_state.data['fish_types']]
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
        mutation_names = ["Ga ada mutasi"] + [m['name'] for m in st.session_state.data['mutation_types']]
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

    st.write("---")

    # Bagian Atribut Shiny & Sparkling (di bawah, bersebelahan)
    st.markdown("##### ✨ Atribut Spesial (Opsional)")
    col_shiny, col_sparkling = st.columns(2)

    LEVERAGE_SHINY_FIXED = 1.85
    LEVERAGE_SPARKLING_FIXED = 1.85

    with col_shiny:
        is_shiny = st.checkbox(
            f"**Shiny** (x{LEVERAGE_SHINY_FIXED})",
            key='calculator_main_shiny_checkbox'
        )
        leverage_shiny = LEVERAGE_SHINY_FIXED if is_shiny else 1.0

    with col_sparkling:
        is_sparkling = st.checkbox(
            f"**Sparkling** (x{LEVERAGE_SPARKLING_FIXED})",
            key='calculator_main_sparkling_checkbox'
        )
        leverage_sparkling = LEVERAGE_SPARKLING_FIXED if is_sparkling else 1.0

    st.write("---")

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

    st.write("---")

    # --- Kalkulasi TOTAL Harga (SEKARANG BENERAN DI BAWAH) ---
    st.header("💰 Estimasi Total Harga Iwakmu!")

    # Cek kondisi minimal untuk menampilkan TOTAL harga: nama ikan sudah dipilih dan minimal ada 1 berat > 0
    if selected_fish_name != "Pilih Jenis Iwak..." and any(b > 0 for b in berat_iwak_list):
        total_final_price = sum(prices_per_fish_for_total) # Jumlahkan semua harga per ikan yang sudah dihitung

        # Langsung tampilkan di sini, tidak pakai placeholder kosong di atas lagi.
        if total_final_price == 0: # Jika semua berat 0 setelah filter
             st.warning("⚠️ Belum ada iwak yang dihitung. Masukkan berat iwak yang valid ya!")
        else:
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
    # Urutkan berdasarkan nama ikan (case-insensitive)
    sorted_fish_types = sorted(st.session_state.data['fish_types'], key=lambda x: x['name'].lower())
    st.dataframe(sorted_fish_types, use_container_width=True)

    st.write("---")

    # --- Tambah Ikan ---
    st.subheader("Tambah Ikan Baru")
    # Buat placeholder kosong di atas form
    message_placeholder_add_fish = st.empty() 

    with st.form("add_fish_form"):
        new_fish_name = st.text_input("Nama Ikan Baru")
        new_fish_leverage = st.number_input(
            "Base $/Kg nya berapa?",
            min_value=0.1,
            value=1.0,
            step=0.05
        )
        add_fish_button = st.form_submit_button("Tambah Ikan")
        if add_fish_button:
            result_message = add_fish(new_fish_name, new_fish_leverage) # Tangkap hasil pesan dari fungsi
            
            # Tampilkan pesan di placeholder (di bagian Tambah Ikan)
            if result_message["type"] == "success":
                message_placeholder_add_fish.markdown(f"<p style='color: #FFFFFF;'>{result_message['content']}</p>", unsafe_allow_html=True) 
            elif result_message["type"] == "warning":
                message_placeholder_add_fish.markdown(f"<p style='color: #FFFFFF;'>{result_message['content']}</p>", unsafe_allow_html=True)
            elif result_message["type"] == "error":
                message_placeholder_add_fish.markdown(f"<p style='color: #FFFFFF;'>{result_message['content']}</p>", unsafe_allow_html=True)

            time.sleep(2) # <--- JEDA 2 DETIK DI SINI!

            st.rerun() # <--- BARU RERUN SETELAH JEDA

    st.write("---")

    # --- Update Ikan ---
    st.subheader("Ubah Nama Ikan")
    # Buat placeholder kosong di atas form UPDATE
    message_placeholder_update_fish = st.empty()
    fish_to_update_options = [f['name'] for f in st.session_state.data['fish_types']]
    # Pastikan ada pilihan untuk diupdate, kalau kosong kasih default None
    if not fish_to_update_options:
        fish_to_update_options = ["Belum ada ikan"]

    fish_to_update = st.selectbox(
        "Pilih Ikan yang akan diubah",
        fish_to_update_options,
        key='update_fish_select', # Kunci unik untuk selectbox
        disabled=(not st.session_state.data['fish_types']) # Disable jika tidak ada ikan
    )
    
    # Ambil nilai default dari ikan yang dipilih (hanya jika ada ikan yang dipilih)
    current_fish = {"name": "", "leverage": 1.0}
    if fish_to_update != "Belum ada ikan":
        current_fish = next((f for f in st.session_state.data['fish_types'] if f['name'] == fish_to_update), {"name": "", "leverage": 1.0})

    with st.form("update_fish_form"):
        updated_fish_name = st.text_input(
            "Nama Ikan Baru",
            value=current_fish['name'],
            key='updated_fish_name_input',
            disabled=(not st.session_state.data['fish_types']) # Disable jika tidak ada ikan
        )
        updated_fish_leverage = st.number_input(
            "Base $/Kg Baru",
            min_value=0.1,
            value=current_fish['leverage'],
            step=0.05,
            key='updated_fish_leverage_input',
            disabled=(not st.session_state.data['fish_types']) # Disable jika tidak ada ikan
        )
        update_fish_button = st.form_submit_button("Ubah Ikan", disabled=(not st.session_state.data['fish_types'])) # Disable button
        if update_fish_button:
            result_message = update_fish(fish_to_update, updated_fish_name, updated_fish_leverage)
            

            # Tampilkan pesan di placeholder (di bagian Tambah Ikan)
            if result_message["type"] == "success":
                message_placeholder_update_fish.markdown(f"<p style='color: #FFFFFF;'>{result_message['content']}</p>", unsafe_allow_html=True) 
            elif result_message["type"] == "warning":
                message_placeholder_update_fish.markdown(f"<p style='color: #FFFFFF;'>{result_message['content']}</p>", unsafe_allow_html=True)
            elif result_message["type"] == "error":
                message_placeholder_update_fish.markdown(f"<p style='color: #FFFFFF;'>{result_message['content']}</p>", unsafe_allow_html=True)
            
            time.sleep(2) # <--- JEDA 2 DETIK DI SINI!
            
            st.rerun()

    st.write("---")

    # --- Hapus Ikan ---
    st.subheader("Hapus Ikan")
    # Buat placeholder kosong di atas button DELETE
    message_placeholder_delete_fish = st.empty()
    fish_to_delete_options = [f['name'] for f in st.session_state.data['fish_types']]
    if not fish_to_delete_options:
        fish_to_delete_options = ["Belum ada ikan"]

    fish_to_delete = st.selectbox(
        "Pilih Ikan yang akan dihapus",
        fish_to_delete_options,
        key='delete_fish_select',
        disabled=(not st.session_state.data['fish_types'])
    )
    delete_fish_button = st.button("Hapus", disabled=(not st.session_state.data['fish_types'])) # Disable button
    if delete_fish_button:
        result_message = delete_fish(fish_to_delete)
        
    # Tampilkan pesan di placeholder (di bagian Tambah Ikan)
        if result_message["type"] == "success":
            message_placeholder_delete_fish.markdown(f"<p style='color: #FFFFFF;'>{result_message['content']}</p>", unsafe_allow_html=True) 
        elif result_message["type"] == "warning":
            message_placeholder_delete_fish.markdown(f"<p style='color: #FFFFFF;'>{result_message['content']}</p>", unsafe_allow_html=True)
        elif result_message["type"] == "error":
            message_placeholder_delete_fish.markdown(f"<p style='color: #FFFFFF;'>{result_message['content']}</p>", unsafe_allow_html=True)
            
        time.sleep(2) # <--- JEDA 2 DETIK DI SINI!
        st.rerun()

# --- Tab Manajemen Jenis Mutasi ---
with tab_mutation_mgmt:
    st.header("Manajemen Mutasi")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
    st.write("Tambah, ubah, atau hapus jenis mutasi dan nilai leveragenya.")

    # Tampilkan Data Saat Ini
    st.subheader("Daftar Jenis Mutasi Saat Ini:")
    # Urutkan berdasarkan nama mutasi (case-insensitive)
    sorted_mutation_types = sorted(st.session_state.data['mutation_types'], key=lambda x: x['name'].lower())
    st.dataframe(sorted_mutation_types, use_container_width=True)

    st.write("---")

    # --- Tambah Mutasi ---
    st.subheader("Tambah Jenis Mutasi Baru")
    # Buat placeholder kosong di atas form
    message_placeholder_add_mutation = st.empty()
    with st.form("add_mutation_form"):
        new_mutation_name = st.text_input("Nama Mutasi Baru")
        new_mutation_leverage = st.number_input(
            "Leverage Mutasi Baru",
            min_value=0.1,
            value=1.0,
            step=0.05
        )
        add_mutation_button = st.form_submit_button("Tambah Mutasi")
        if add_mutation_button:
            result_message = add_mutation(new_mutation_name, new_mutation_leverage)
            
            if result_message["type"] == "success":
                message_placeholder_add_mutation.success(result_message["content"])
            elif result_message["type"] == "warning":
                message_placeholder_add_mutation.warning(result_message["content"])
            elif result_message["type"] == "error":
                message_placeholder_add_mutation.error(result_message["content"])

            time.sleep(2)
            st.rerun()

    st.write("---")

    # --- Update Mutasi ---
    st.subheader("Ubah Jenis Mutasi")
    # Buat placeholder kosong di atas form UPDATE
    message_placeholder_update_mutation = st.empty()
    mutation_to_update_options = [m['name'] for m in st.session_state.data['mutation_types']]
    if not mutation_to_update_options:
        mutation_to_update_options = ["Belum ada mutasi"]

    mutation_to_update = st.selectbox(
        "Pilih Mutasi yang akan diubah",
        mutation_to_update_options,
        key='update_mutation_select',
        disabled=(not st.session_state.data['mutation_types'])
    )
    current_mutation = {"name": "", "leverage": 1.0}
    if mutation_to_update != "Belum ada mutasi":
        current_mutation = next((m for m in st.session_state.data['mutation_types'] if m['name'] == mutation_to_update), {"name": "", "leverage": 1.0})

    with st.form("update_mutation_form"):
        updated_mutation_name = st.text_input(
            "Nama Mutasi Baru",
            value=current_mutation['name'],
            key='updated_mutation_name_input',
            disabled=(not st.session_state.data['mutation_types'])
        )
        updated_mutation_leverage = st.number_input(
            "Leverage Mutasi Baru",
            min_value=0.1,
            value=current_mutation['leverage'],
            step=0.05,
            key='updated_mutation_leverage_input',
            disabled=(not st.session_state.data['mutation_types'])
        )
        update_mutation_button = st.form_submit_button("Ubah Mutasi", disabled=(not st.session_state.data['mutation_types']))
        if update_mutation_button:
            result_message = update_mutation(mutation_to_update, updated_mutation_name, updated_mutation_leverage)
            
            if result_message["type"] == "success":
                message_placeholder_update_mutation.success(result_message["content"])
            elif result_message["type"] == "warning":
                message_placeholder_update_mutation.warning(result_message["content"])
            elif result_message["type"] == "error":
                message_placeholder_update_mutation.error(result_message["content"])

            time.sleep(2)
            st.rerun()

    st.write("---")

    # --- Hapus Mutasi ---
    st.subheader("Hapus Jenis Mutasi")
    # Buat placeholder kosong di atas button DELETE
    message_placeholder_delete_mutation = st.empty()
    mutation_to_delete_options = [m['name'] for m in st.session_state.data['mutation_types']]
    if not mutation_to_delete_options:
        mutation_to_delete_options = ["Belum ada mutasi"]

    mutation_to_delete = st.selectbox(
        "Pilih Mutasi yang akan dihapus",
        mutation_to_delete_options,
        key='delete_mutation_select',
        disabled=(not st.session_state.data['mutation_types'])
    )
    delete_mutation_button = st.button("Hapus Mutasi", disabled=(not st.session_state.data['mutation_types']))
    if delete_mutation_button:
        result_message = delete_mutation(mutation_to_delete)
        
        if result_message["type"] == "success":
            message_placeholder_delete_mutation.success(result_message["content"])
        elif result_message["type"] == "warning":
            message_placeholder_delete_mutation.warning(result_message["content"])
        elif result_message["type"] == "error":
            message_placeholder_delete_mutation.error(result_message["content"])
            
        time.sleep(2)
        st.rerun()