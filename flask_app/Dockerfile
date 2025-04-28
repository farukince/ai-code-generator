# Python tabanlı hafif bir imajdan başla
FROM python:3.10-slim

# Uygulama klasörünü oluştur ve içine geç
WORKDIR /app

# Proje dosyalarını konteynere kopyala
COPY . .

# Gerekli Python paketlerini yükle
RUN pip install --no-cache-dir -r requirements.txt

# Sunucuyu dışarı aç (port 5001'de çalışıyorduk)
EXPOSE 5001

# Uygulamayı çalıştır
CMD ["python", "app/main.py"]
