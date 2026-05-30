import pandas as pd

print("--- MEMULAI PROSES OLAH DATA ---")

# 1. Membaca file CSV menggunakan Pandas
df = pd.read_csv("penjualan.csv")

# Tampilkan data mentah di terminal
print("\n> Data Mentah Penjualan:")
print(df)

# 2. Menghitung Kolom Baru: Total Harga per Transaksi (Jumlah x Harga)
df["total_bayar"] = df["jumlah"] * df["harga"]

# 3. Menghitung Total Omzet Keseluruhan
total_omzet = df["total_bayar"].sum()
print(f"\n> Total Omzet Toko: Rp {total_omzet:,}")

# 4. Menyaring data (Filter): Hanya ambil kategori 'Elektronik'
data_elektronik = df[df["kategori"] == "Elektronik"]
print("\n> Transaksi Kategori Elektronik Saja:")
print(data_elektronik)

# 5. Menyimpan hasil olahan ke file Excel baru (Materi openpyxl dasar)
# Catatan: Kita eksport ke CSV baru dulu agar tidak perlu install library excel tambahan malam ini
df.to_csv("laporan_penjualan_clean.csv", index=False)
print("\n[Sukses] Hasil olahan disimpan ke 'laporan_penjualan_clean.csv'")