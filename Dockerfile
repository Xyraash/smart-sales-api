# 1. Gunakan image dasar Python resmi ala Linux yang ringan
FROM python:3.10-slim

# 2. Atur folder kerja di dalam container nanti
WORKDIR /app

# 3. Copy file daftar library ke dalam container
COPY requirements.txt .

# 4. Instal seluruh library di dalam container tanpa menggunakan cache
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy seluruh file proyek kita dari laptop ke dalam container
COPY . .

# 6. Buka jalur port 8000 agar aplikasi bisa diakses dari luar
EXPOSE 8000

# 7. Perintah untuk menyalakan server Uvicorn saat container dijalankan
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]