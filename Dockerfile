# Gunakan image Python sebagai base image
FROM python:3.10-slim

# Set working directory di dalam container
WORKDIR /app

# Install dependensi sistem yang diperlukan
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy file requirements.txt ke dalam container
COPY requirements.txt .

# Install dependensi Python
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode aplikasi ke dalam container
COPY . .

# Tentukan port yang akan digunakan oleh FastAPI
EXPOSE 8000

# Perintah untuk menjalankan aplikasi dengan Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
