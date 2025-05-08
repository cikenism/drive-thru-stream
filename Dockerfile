# Gunakan image Python yang ringan
FROM python:3.10-slim

# Install build tools dan dependensi untuk pyaudio
RUN apt-get update && apt-get install -y \
    build-essential \
    libportaudio2 \
    libsndfile1 \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Tentukan direktori kerja
WORKDIR /app

# Salin requirements.txt ke dalam container
COPY requirements.txt .

# Install dependensi Python
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode aplikasi ke dalam container
COPY . .

# Tentukan perintah untuk menjalankan aplikasi
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
