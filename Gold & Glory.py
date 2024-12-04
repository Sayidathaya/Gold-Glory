import time
from datetime import datetime, timedelta
from collections import defaultdict
from prettytable import PrettyTable

# Data awal pengguna
pengguna = {
    'pengguna1': {'sandi': 'sandi1', 'role': 'Member', 'gold': 0000, 'rupiah': 0000000, 'percobaan_gagal': 0, 'akun_terkunci': False, 'items_beli': []},
    'pengguna2': {'sandi': 'sandi2', 'role': 'VVIP', 'gold': 0000, 'rupiah': 0000000, 'percobaan_gagal': 0, 'akun_terkunci': False, 'items_beli': []},
}

# Daftar item yang tersedia
items_pagi = {'Dual_Daggers': 100, 'Giant_Halberd': 150}  # Barang di pagi hari
items_siang = {'Spellbook': 100, 'Wizard_Staff': 150}  # Barang di siang hari
items_malam = {'Longbow': 100, 'Heavy_Crossbow': 150}  # Barang di malam hari

# Item khusus untuk VVIP
items_vvip = {
    'Obsidian_Sword': 500, 
    'Diamond_Shield': 500, 
    'Cursed_Blade': 1000, 
    'Crystal_Claws': 1000, 
    'Lava_Spear': 1500, 
    'Ice_Longbow': 1500
}

# Voucher dengan masa kedaluarsa dan pembatasan
vouchers = {
    'Warriors': {'diskon': 0.25, 'tgl_kedaluarsa': datetime.now() + timedelta(days=30), 'max_usage': 10},  # Berlaku 10 kali per bulan
    'Golds': {'diskon': 0.50, 'tgl_kedaluarsa': datetime.now() + timedelta(days=5), 'max_usage': 5},  # Berlaku 5 kali per bulan
    'Treasures': {'diskon': 0.75, 'tgl_kedaluarsa': datetime.now() + timedelta(days=1), 'max_usage': 1},  # Berlaku 1 kali per bulan
}

# Menyimpan log penggunaan voucher per pengguna
voucher_usage_log = defaultdict(lambda: defaultdict(list))


# Opsi top up gold
top_up_options = {
    100: 50000,    # 100 gold for 50,000 IDR
    250: 100000,   # 250 gold for 100,000 IDR
    500: 200000,   # 500 gold for 200,000 IDR
    1000: 400000,  # 1000 gold for 400,000 IDR
    2000: 750000   # 2000 gold for 750,000 IDR
}

# Fungsi untuk memberikan warna pada nama item berdasarkan harga
def get_item_color(harga):
    if harga == 100:
        return '\033[32m'  # Hijau
    elif harga == 150:
        return '\033[34m'  # Biru
    elif harga == 500:
        return '\033[35m'  # Ungu
    elif harga == 1000:
        return '\033[33m'  # Kuning
    elif harga == 1500:
        return '\033[31m'  # Merah
    else:
        return '\033[0m'  # Warna default (tidak ada warna)

# Fungsi untuk mendapatkan harga item berdasarkan nama
def get_item_price(item_name):
    # Daftar harga item, misalnya:
    item_prices = {
        "Dual_Daggers": 100,
        "Spellbook": 100,
        "Longbow" : 100,
        "Giant_Halberd" : 150,
        "Wizard_Staff" : 150,
        "Heavy_Crossbow" : 150,
        "Obsidian_Sword": 500,
        "Diamond_Shield": 500,
        "Cursed_Blade": 1000,
        "Crystal_Claws": 1000,
        "Lava_Spear": 1500,
        "Ice_Longbow": 1500
    }
    return item_prices.get(item_name, 0)  # Mengembalikan harga item atau 0 jika tidak ditemukan

# Fungsi untuk menampilkan daftar item yang telah dibeli
def show_purchased_items(pengguna):
    if not pengguna['items_beli']:
        print("Anda belum membeli item apapun.")
    else:
        print("\nDaftar item yang telah dibeli:")
        for index, item in enumerate(pengguna['items_beli'], 1):
            # Menentukan harga item yang telah dibeli berdasarkan nama item
            harga_item = get_item_price(item)
            item_color = get_item_color(harga_item)  # Menentukan warna berdasarkan harga item
            print(f"{index}. {item_color}{item}\033[0m")  # Menampilkan item dengan warna
        print("\n")

# Fungsi untuk memeriksa waktu dan menampilkan item berdasarkan role pengguna
def get_items_for_user(pengguna):
    print(f"Role pengguna saat ini: {pengguna['role']}")  # Log tambahan
    if pengguna['role'] == 'VVIP':  # Periksa role dengan tegas
        items = items_vvip
    else:
        current_hour = datetime.now().hour
        if 6 <= current_hour < 12:
            items = items_pagi
        elif 12 <= current_hour < 18:
            items = items_siang
        else:
            items = items_malam
    print(f"Item yang tersedia: {items}")  # Log tambahan untuk verifikasi
    return items


# Fungsi login untuk Member
def login_member():
    print("Menu Login Member")
    username = input("Username: ")
    if username not in pengguna or pengguna[username]['role'].lower() != 'member':
        print("Username tidak ditemukan atau Anda bukan Member.")
        return None
    
    pengguna_data = pengguna[username]
    
    if pengguna_data['akun_terkunci']:
        print("Akun Anda terkunci karena terlalu banyak percobaan login gagal.")
        return None
    
    sandi = input("Sandi: ")
    if sandi == pengguna_data['sandi']:
        print(f"Selamat datang {username}!")
        print(f"Role Anda: {pengguna_data['role']}")
        pengguna_data['percobaan_gagal'] = 0  # Reset percobaan gagal
        return pengguna_data
    else:
        pengguna_data['percobaan_gagal'] += 1
        if pengguna_data['percobaan_gagal'] >= 3:
            pengguna_data['akun_terkunci'] = True
            print("Akun Anda terkunci karena terlalu banyak percobaan login gagal.")
        else:
            print(f"Sandi salah. Percobaan {pengguna_data['percobaan_gagal']} dari 3.")
        return None

# Fungsi login untuk VVIP
def login_vvip():
    print("Menu Login VVIP")
    username = input("Username: ")
    if username not in pengguna or pengguna[username]['role'] != 'VVIP':
        print("Username tidak ditemukan atau Anda bukan VVIP.")
        return None
    
    pengguna_data = pengguna[username]
    
    if pengguna_data['akun_terkunci']:
        print("Akun Anda terkunci karena terlalu banyak percobaan login gagal.")
        return None
    
    sandi = input("Sandi: ")
    if sandi == pengguna_data['sandi']:
        print(f"Selamat datang {username}!")
        print(f"Role Anda: {pengguna_data['role']}")
        return pengguna_data
    else:
        pengguna_data['percobaan_gagal'] += 1
        if pengguna_data['percobaan_gagal'] >= 3:
            pengguna_data['akun_terkunci'] = True
            print("Akun Anda terkunci karena terlalu banyak percobaan login gagal.")
        else:
            print(f"Sandi salah. Percobaan {pengguna_data['percobaan_gagal']} dari 3.")
        return None

# Fungsi utama untuk login dengan pilihan Member atau VVIP
def login():
    print("Pilih Mode Login")
    print("1. Login Member")
    print("2. Login VVIP")
    mode = input("Masukkan pilihan (1/2): ")
    if mode == "1":
        return login_member()
    elif mode == "2":
        return login_vvip()
    else:
        print("Pilihan tidak valid.")
        return None


# Fungsi registrasi
def register():
    print("Menu Registrasi")
    username = input("Username: ")
    if username in pengguna:
        print("Username sudah terdaftar.")
        return
    sandi = input("Sandi: ")
    role = input("Pilih role (Member/VVIP): ").strip().upper()
    if role not in ['MEMBER', 'VVIP']:
        print("Role tidak valid.")
        return
    pengguna[username] = {
        'sandi': sandi,
        'role': 'VVIP' if role == 'VVIP' else 'Member',
        'gold': 0,
        'rupiah': 0,
        'percobaan_gagal': 0,
        'akun_terkunci': False,
        'items_beli': []  # Tambahkan atribut items_beli
    }
    print(f"Registrasi berhasil! Selamat datang, {username}.")


# Fungsi untuk memeriksa penggunaan voucher
def apply_voucher(pengguna_data):
    voucher_code = input("Masukkan kode voucher: ").strip()
    username = next((user for user, data in pengguna.items() if data is pengguna_data), None)  # Mendapatkan username pengguna
    
    if username is None:
        print("Terjadi kesalahan: Tidak dapat menemukan username.")
        return 0

    if voucher_code in vouchers:
        voucher = vouchers[voucher_code]
        if datetime.now() > voucher['tgl_kedaluarsa']:
            print("Voucher sudah kadaluarsa.")
            return 0
        else:
            # Cek berapa kali voucher telah digunakan dalam sebulan
            current_month = datetime.now().month
            used_count = sum(1 for use_date in voucher_usage_log[username][voucher_code]
                            if use_date.month == current_month)
            
            if used_count >= voucher['max_usage']:
                print(f"Voucher {voucher_code} telah digunakan maksimal {voucher['max_usage']} kali bulan ini.")
                return 0
            
            # Simpan tanggal penggunaan voucher
            voucher_usage_log[username][voucher_code].append(datetime.now())
            print(f"Voucher {voucher_code} diterapkan! Diskon: {voucher['diskon'] * 100}%")
            return voucher['diskon']
    else:
        print("Kode voucher tidak valid.")
        return 0


# Fungsi untuk pembelian barang
def buy_item(pengguna):
    items = get_items_for_user(pengguna)  # Dapatkan item berdasarkan role pengguna
    
    # Display items in a table format using PrettyTable
    table = PrettyTable()
    table.field_names = ["No", "Item", "Golds"]
    
    # Add items to the table with numbering and colored item names
    for index, (item, price) in enumerate(items.items(), 1):
        item_color = get_item_color(price)  # Menentukan warna berdasarkan harga item
        table.add_row([index, f"{item_color}{item}\033[0m", price])  # Warna pada nama item
    
    # Tambahkan opsi untuk kembali
    table.add_row(["0", "Kembali ke Menu Sebelumnya", "-"])
    
    print("Barang yang tersedia:")
    print(table)

    try:
        opsi_item = int(input("Pilih nomor barang yang ingin dibeli (0 untuk kembali): "))
        
        if opsi_item == 0:
            print("Kembali ke Menu Sebelumnya...")
            return
        
        # Get the selected item
        nama_item = list(items.keys())[opsi_item - 1]
        harga_item = items[nama_item]
        
        # Apply voucher
        diskon = apply_voucher(pengguna)
        final_price = harga_item * (1 - diskon)
        
        if pengguna['gold'] >= final_price:
            pengguna['gold'] -= final_price
            pengguna['items_beli'].append(nama_item)  # Tambahkan item ke daftar pembelian
            print(f"Pembelian berhasil! Anda membeli {nama_item} dengan harga {final_price} Gold. Sisa Gold: {pengguna['gold']}")
        else:
            print("Gold Anda tidak cukup untuk melakukan pembelian.")
    except (ValueError, IndexError):
        print("Pilihan tidak valid. Harap pilih nomor yang benar.")


# Fungsi untuk top up saldo rupiah
def top_up_rupiah(pengguna_data):
    try:
        nominal = int(input("Masukkan jumlah rupiah yang ingin di-top-up: "))
        if nominal <= 0:
            print("Nominal harus lebih besar dari 0.")
        else:
            pengguna_data['rupiah'] += nominal
            print(f"Top up berhasil! Saldo rupiah Anda sekarang: {pengguna_data['rupiah']}")
    except ValueError:
        print("Input tidak valid. Harap masukkan angka.")

# Fungsi untuk menampilkan saldo rupiah pengguna
def show_rupiah_balance(pengguna_data):
    print(f"Saldo Rupiah Anda saat ini: {pengguna_data['rupiah']}")


# Fungsi untuk menampilkan saldo Gold pengguna
def show_gold_balance(pengguna_data):
    print(f"Saldo Gold Anda: {pengguna_data['gold']} Gold")

# Fungsi untuk top up saldo menggunakan pilihan jumlah gold
def top_up_saldo(pengguna):
    print("\nPilih jumlah gold yang ingin Anda beli:")
    
    # Menampilkan opsi dengan nomor
    options_list = list(top_up_options.items())
    for i, (gold, cost) in enumerate(options_list, 1):
        print(f"{i}. {gold} Gold - {cost} IDR")
    
    print("6. Tidak ingin membeli gold.")
    
    try:
        pilih_opsi = int(input("Masukkan pilihan Anda (1-6): "))
        
        if pilih_opsi == 6:
            print("Anda memilih untuk tidak membeli gold. Kembali ke menu utama.")
            return
        
        if pilih_opsi < 1 or pilih_opsi > 5:
            print("Pilihan tidak valid. Silakan pilih opsi yang tersedia.")
            return
        
        # Get the corresponding gold and cost based on the selected option
        gold, harga_rupiah = options_list[pilih_opsi - 1]
        
        # Check if the pengguna has enough Rupiah for the purchase
        if pengguna['rupiah'] < harga_rupiah:
            print(f"Saldo Rupiah Anda tidak cukup untuk membeli {gold} gold. Anda membutuhkan {harga_rupiah - pengguna['rupiah']} lebih banyak.")
            return
        
        pengguna['rupiah'] -= harga_rupiah
        pengguna['gold'] += gold
        print(f"Top up berhasil! Anda sekarang memiliki {pengguna['gold']} Gold.")
    
    except ValueError:
        print("Pilihan tidak valid, masukkan angka yang benar.")


# Fungsi untuk menampilkan menu utama
def show_main_menu():
    print("=" * 50)
    print(" " * 10 + "GOLD & GLORY")
    print("=" * 50)
    print("Menu Utama")
    print("1. Login")
    print("2. Registrasi")
    print("3. Keluar")


# Fungsi untuk menampilkan tabel "YATTAAAA!!!!!" ketika keluar dari program
def show_yatta_message():
    table = PrettyTable()
    table.field_names = ["YATTAAAA!!!!!"]
    
    # Menambahkan "YATTAAAA!!!!!" di dalam tabel
    table.add_row(["YATTAAAA!!!!!"])
    
    # Menampilkan tabel besar
    print("=" * 50)
    print(table)
    print("=" * 50)


# Fungsi utama untuk menjalankan aplikasi
def main():
    while True:
        show_main_menu()
        pilihan = input("Pilih opsi: ")
        
        if pilihan == "1":
            pengguna_data = login()
            if pengguna_data:
                while True:
                    print("\nMenu Pembelian")
                    print("1. Belanja")
                    print("2. Top Up Saldo Rupiah")
                    print("3. Top Up Gold")
                    print("4. Lihat Saldo Gold")
                    print("5. Lihat Saldo Rupiah")
                    print("6. Lihat Item yang Telah Dibeli")
                    print("7. Keluar")
                    
                    menu_pembelian = input("Pilih opsi: ")
                    
                    if menu_pembelian == "1":
                        buy_item(pengguna_data)
                    elif menu_pembelian == "2":
                        top_up_rupiah(pengguna_data)
                    elif menu_pembelian == "3":
                        top_up_saldo(pengguna_data)
                    elif menu_pembelian == "4":
                        show_gold_balance(pengguna_data)
                    elif menu_pembelian == "5":
                        show_rupiah_balance(pengguna_data)
                    elif menu_pembelian == "6":
                        show_purchased_items(pengguna_data)
                    elif menu_pembelian == "7":
                        print("Keluar dari menu pembelian.")
                        break
                    else:
                        print("Opsi tidak valid.")
        elif pilihan == "2":
            register()
        elif pilihan == "3":
            print("Terima kasih telah membeli di toko persenjataan kami, saatnya menerobos dungeon bersama!")
            show_yatta_message()  # Menampilkan pesan YATTAAAA!!!!! saat keluar
            break
        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    main()