# 1. Gunakan base image Python yang resmi
FROM python:3.10-slim

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Buat direktori kerja di dalam container
WORKDIR /app

# 4. Copy file requirements dan install dependensi terlebih dahulu
#    Ini memanfaatkan Docker caching
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# 5. Copy seluruh kode proyek ke dalam direktori kerja
COPY . /app/

# Memberi tahu bahwa container ini akan listen di port 8000
EXPOSE 8000

# Jalankan server bawaan Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]