from fastapi import FastAPI

# Inisialisasi FastAPI
app = FastAPI(title="Smart-Sales Analytics API")

# Endpoint 1: Halaman Utama
@app.get("/")
def home():
    return {
        "status": "Sukses",
        "pesan": "Percobaan membuat."
    }

# Endpoint 2: Simulasi Data Penjualan (Materi Olah Data)
@app.get("/api/penjualan/total")
def ambil_total_penjualan():
    return {
        "total_omzet": 5000000,
        "jumlah_transaksi": 120,
        "mata_uang": "IDR"
    }