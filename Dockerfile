# Gunakan image Python resmi yang ringan
FROM python:3.12-slim

# Folder kerja di dalam container
WORKDIR /app

# Copy dan install dependensi terlebih dahulu (memanfaatkan Docker layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh source code ke container
COPY . .

# Buka port 8000
EXPOSE 8000

# Jalankan server Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]