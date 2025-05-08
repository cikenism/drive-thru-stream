# Gunakan image dasar Python
FROM python:3.10-slim

# Install dependencies system-level (termasuk PortAudio)
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Set direktori kerja di dalam container
WORKDIR /app

# Salin file requirements.txt ke container
COPY requirements.txt .

# Install dependensi Python
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode aplikasi ke dalam container
COPY . .

# Expose port aplikasi
EXPOSE 8000

# Perintah untuk menjalankan aplikasi
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
