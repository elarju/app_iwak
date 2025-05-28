import streamlit as st # type: ignore
import json
import os

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Iwak App | Fisch-RBL",
    page_icon="🐟",
    layout="centered"
)

# --- Nama File Database (JSON) ---
DATA_FILE = "D:/Iwak/iwak_data.json"

# --- Fungsi untuk Memuat dan Menyimpan Data ---
def load_data():
    if not os.path.exists(DATA_FILE):
        # Data default jika file belum ada
        return {
            "fish_types": [
            ],
            "mutation_types": [
            ]
        }
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- Inisialisasi Data ke Session State ---
if 'data' not in st.session_state:
    st.session_state.data = load_data()

# --- Fungsi CRUD untuk Jenis Ikan ---
def add_fish(name, leverage):
    if name and leverage is not None:
        if not any(f['name'] == name for f in st.session_state.data['fish_types']):
            st.session_state.data['fish_types'].append({"name": name, "leverage": leverage})
            save_data(st.session_state.data)
            st.success(f"Jenis ikan '{name}' berhasil ditambahkan!")
        else:
            st.warning(f"Jenis ikan '{name}' sudah ada.")
    else:
        st.error("Nama ikan dan leverage tidak boleh kosong.")

def update_fish(old_name, new_name, new_leverage):
    if old_name and new_name and new_leverage is not None:
        for i, fish in enumerate(st.session_state.data['fish_types']):
            if fish['name'] == old_name:
                st.session_state.data['fish_types'][i] = {"name": new_name, "leverage": new_leverage}
                save_data(st.session_state.data)
                st.success(f"Jenis ikan '{old_name}' berhasil diupdate menjadi '{new_name}'.")
                return
        st.error(f"Jenis ikan '{old_name}' tidak ditemukan.")
    else:
        st.error("Semua input untuk update ikan tidak boleh kosong.")

def delete_fish(name):
    initial_len = len(st.session_state.data['fish_types'])
    st.session_state.data['fish_types'] = [f for f in st.session_state.data['fish_types'] if f['name'] != name]
    if len(st.session_state.data['fish_types']) < initial_len:
        save_data(st.session_state.data)
        st.success(f"Jenis ikan '{name}' berhasil dihapus!")
    else:
        st.warning(f"Jenis ikan '{name}' tidak ditemukan.")

# --- Fungsi CRUD untuk Jenis Mutasi ---
def add_mutation(name, leverage):
    if name and leverage is not None:
        if not any(m['name'] == name for m in st.session_state.data['mutation_types']):
            st.session_state.data['mutation_types'].append({"name": name, "leverage": leverage})
            save_data(st.session_state.data)
            st.success(f"Jenis mutasi '{name}' berhasil ditambahkan!")
        else:
            st.warning(f"Jenis mutasi '{name}' sudah ada.")
    else:
        st.error("Nama mutasi dan leverage tidak boleh kosong.")

def update_mutation(old_name, new_name, new_leverage):
    if old_name and new_name and new_leverage is not None:
        for i, mut in enumerate(st.session_state.data['mutation_types']):
            if mut['name'] == old_name:
                st.session_state.data['mutation_types'][i] = {"name": new_name, "leverage": new_leverage}
                save_data(st.session_state.data)
                st.success(f"Jenis mutasi '{old_name}' berhasil diupdate menjadi '{new_name}'.")
                return
        st.error(f"Jenis mutasi '{old_name}' tidak ditemukan.")
    else:
        st.error("Semua input untuk update mutasi tidak boleh kosong.")

def delete_mutation(name):
    initial_len = len(st.session_state.data['mutation_types'])
    st.session_state.data['mutation_types'] = [m for m in st.session_state.data['mutation_types'] if m['name'] != name]
    if len(st.session_state.data['mutation_types']) < initial_len:
        save_data(st.session_state.data)
        st.success(f"Jenis mutasi '{name}' berhasil dihapus!")
    else:
        st.warning(f"Jenis mutasi '{name}' tidak ditemukan.")

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

# --- Tab Kalkulator Iwak ---
with tab_calculator:
    st.header("Input Variable-nya")

    # Ambil data jenis ikan dari yang sudah di-load/di-manage
    fish_names = [f['name'] for f in st.session_state.data['fish_types']]
    selected_fish_name = st.selectbox(
        "Iwak apa?",
        fish_names,
        help="Pilih mau itung iwak apa ><"
    )

    # Dapatkan leverage_ikan berdasarkan pilihan
    leverage_ikan = 1.0 # Default jika tidak ditemukan
    for fish in st.session_state.data['fish_types']:
        if fish['name'] == selected_fish_name:
            leverage_ikan = fish['leverage']
            # st.info(f"Leverage Ikan '{selected_fish_name}': **{leverage_ikan}x**")
            break

    berat_ikan_raw = st.number_input(
        "Berat Iwak (kg)",
        min_value=0.1,
        value=1.0, # Default value yang valid
        step=0.05,
        help="Berat Iwak (Kg)"
    )
    berat_ikan = float(berat_ikan_raw) if berat_ikan_raw is not None else 1.0


    # --- Bagian Mutasi (Dalam Expander) ---
    with st.expander("⚙️ Mutasi (Opsional)"):
        st.markdown("Iwak-nya dapet **mutasi** ga?")
        
        # Ambil data mutasi dari yang sudah di-load/di-manage
        mutation_names = ["Ga ada"] + [m['name'] for m in st.session_state.data['mutation_types']]
        selected_mutasi = st.selectbox(
            "Pilih Mutasi",
            mutation_names,
            index=0, # Default 'Tidak Ada Mutasi'
            help="Pilih **'Ga ada'** kalau iwak normal."
        )

        leverage_mutasi = 1.0 # Default jika tidak ada mutasi
        if selected_mutasi != "Tidak Ada Mutasi":
            for mut in st.session_state.data['mutation_types']:
                if mut['name'] == selected_mutasi:
                    leverage_mutasi = mut['leverage']
                    # st.info(f"Leverage {selected_mutasi}: **{leverage_mutasi}x** (Tidak Dapat Diubah)")
                    break

    # --- Bagian Atribut Shiny & Sparkling (Dalam Expander) ---
    with st.expander("✨ Shiny | Sparkling (Opsional)"):
        st.markdown("Centang kalau iwaknya dapet atribut SS")

        # Nilai leverage shiny dan sparkling yang sudah fix
        LEVERAGE_SHINY_FIXED = 1.85
        LEVERAGE_SPARKLING_FIXED = 1.85

        col3, col4 = st.columns(2)

        with col3:
            is_shiny = st.checkbox(f"Shiny")
            leverage_shiny = LEVERAGE_SHINY_FIXED if is_shiny else 1.0

        with col4:
            is_sparkling = st.checkbox(f"Sparkling")
            leverage_sparkling = LEVERAGE_SPARKLING_FIXED if is_sparkling else 1.0


    st.write("---")

    # --- Kalkulasi Harga ---
    st.header("Hasil Kalkulasi")

    if st.button("Hitung Harga Iwak", use_container_width=True):
        calc_leverage_ikan = leverage_ikan if leverage_ikan is not None else 1.0
        calc_berat_ikan = berat_ikan if berat_ikan is not None else 1.0
        calc_leverage_mutasi = leverage_mutasi if leverage_mutasi is not None else 1.0
        calc_leverage_shiny = leverage_shiny if leverage_shiny is not None else 1.0
        calc_leverage_sparkling = leverage_sparkling if leverage_sparkling is not None else 1.0

        final_price = (
            calc_leverage_shiny *
            calc_leverage_sparkling *
            calc_leverage_mutasi *
            calc_leverage_ikan *
            calc_berat_ikan
        )

        if final_price > 0:
            st.success(f"### Coin : {final_price:,.0f} $")
        else:
            st.warning("Berat-nya belum wak, mau itung ikan apa sih?")

# --- Tab Manajemen Jenis Ikan ---
with tab_fish_mgmt:
    st.header("Manajemen Jenis Ikan")
    st.write("Tambah, ubah, atau hapus jenis ikan dan nilai leveragenya.")

    # Tampilkan Data Saat Ini
    st.subheader("Daftar Jenis Ikan Saat Ini:")
    st.dataframe(st.session_state.data['fish_types'], use_container_width=True)

    st.write("---")

    # --- Tambah Ikan ---
    st.subheader("Tambah Jenis Ikan Baru")
    with st.form("add_fish_form"):
        new_fish_name = st.text_input("Nama Ikan Baru")
        new_fish_leverage = st.number_input(
            "Leverage Ikan Baru",
            min_value=0.1,
            value=1.0,
            step=0.05
        )
        add_fish_button = st.form_submit_button("Tambah Ikan")
        if add_fish_button:
            add_fish(new_fish_name, new_fish_leverage)
            st.rerun() # Refresh aplikasi untuk update tampilan data

    st.write("---")

    # --- Update Ikan ---
    st.subheader("Ubah Jenis Ikan")
    fish_to_update = st.selectbox(
        "Pilih Ikan yang akan diubah",
        [f['name'] for f in st.session_state.data['fish_types']],
        key='update_fish_select' # Kunci unik untuk selectbox
    )
    # Ambil nilai default dari ikan yang dipilih
    current_fish = next((f for f in st.session_state.data['fish_types'] if f['name'] == fish_to_update), {"name": "", "leverage": 1.0})

    with st.form("update_fish_form"):
        updated_fish_name = st.text_input(
            "Nama Ikan Baru",
            value=current_fish['name'],
            key='updated_fish_name_input'
        )
        updated_fish_leverage = st.number_input(
            "Leverage Ikan Baru",
            min_value=0.1,
            value=current_fish['leverage'],
            step=0.05,
            key='updated_fish_leverage_input'
        )
        update_fish_button = st.form_submit_button("Ubah Ikan")
        if update_fish_button:
            update_fish(fish_to_update, updated_fish_name, updated_fish_leverage)
            st.rerun()

    st.write("---")

    # --- Hapus Ikan ---
    st.subheader("Hapus Jenis Ikan")
    fish_to_delete = st.selectbox(
        "Pilih Ikan yang akan dihapus",
        [f['name'] for f in st.session_state.data['fish_types']],
        key='delete_fish_select'
    )
    delete_fish_button = st.button("Hapus Ikan")
    if delete_fish_button:
        delete_fish(fish_to_delete)
        st.rerun()

# --- Tab Manajemen Jenis Mutasi ---
with tab_mutation_mgmt:
    st.header("Manajemen Jenis Mutasi")
    st.write("Tambah, ubah, atau hapus jenis mutasi dan nilai leveragenya.")

    # Tampilkan Data Saat Ini
    st.subheader("Daftar Jenis Mutasi Saat Ini:")
    st.dataframe(st.session_state.data['mutation_types'], use_container_width=True)

    st.write("---")

    # --- Tambah Mutasi ---
    st.subheader("Tambah Jenis Mutasi Baru")
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
            add_mutation(new_mutation_name, new_mutation_leverage)
            st.rerun()

    st.write("---")

    # --- Update Mutasi ---
    st.subheader("Ubah Jenis Mutasi")
    mutation_to_update = st.selectbox(
        "Pilih Mutasi yang akan diubah",
        [m['name'] for m in st.session_state.data['mutation_types']],
        key='update_mutation_select'
    )
    current_mutation = next((m for m in st.session_state.data['mutation_types'] if m['name'] == mutation_to_update), {"name": "", "leverage": 1.0})

    with st.form("update_mutation_form"):
        updated_mutation_name = st.text_input(
            "Nama Mutasi Baru",
            value=current_mutation['name'],
            key='updated_mutation_name_input'
        )
        updated_mutation_leverage = st.number_input(
            "Leverage Mutasi Baru",
            min_value=0.1,
            value=current_mutation['leverage'],
            step=0.05,
            key='updated_mutation_leverage_input'
        )
        update_mutation_button = st.form_submit_button("Ubah Mutasi")
        if update_mutation_button:
            update_mutation(mutation_to_update, updated_mutation_name, updated_mutation_leverage)
            st.rerun()

    st.write("---")

    # --- Hapus Mutasi ---
    st.subheader("Hapus Jenis Mutasi")
    mutation_to_delete = st.selectbox(
        "Pilih Mutasi yang akan dihapus",
        [m['name'] for m in st.session_state.data['mutation_types']],
        key='delete_mutation_select'
    )
    delete_mutation_button = st.button("Hapus Mutasi")
    if delete_mutation_button:
        delete_mutation(mutation_to_delete)
        st.rerun()