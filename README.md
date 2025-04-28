# AI Code Generator - Kubernetes Dağıtımı

## 🚀 Proje Hakkında

Flask tabanlı, Llama3 destekli Yapay Zeka Kod Üretici API Projesi. Kubernetes ortamında çalışacak şekilde geliştirildi ve Docker ile containerize edildi.

Bu proje, kullanıcılardan alınan doğal dil isteklerine göre Python kodu üreten bir yapay zeka asistanı sağlamaktadır. Yerel çalıştırılan Llama3 modeli kullanılarak Flask API üzerinden kod ve başlık üretilmektedir.

API, Docker imajı olarak paketlenmiş, Kubernetes üzerinde çalışacak şekilde dağıtılmıştır.

Docker Hub imaj linki: https://hub.docker.com/r/farukiince/ai-code-generator  

## 🛠️ Kullanılan Teknolojiler

*   Python 3.10
*   Flask
*   Docker
*   Kubernetes (Minikube)
*   Ollama (Llama3 modeli)
*   curl (API testleri için)

## ⚙️ Kurulum Adımları

### 1. Ön Gereksinimler

*   Minikube
*   kubectl
*   Ollama (Llama3 modeli)

### 2. Adım Adım Kurulum

```bash
# Repository'yi klonla
git clone <repo-link>
cd ai-code-generator

# Ollama ile Llama3 modelini kur (Eğer kurulu değilse)
ollama run llama3

# Docker imajını oluştur
docker build -t ai-code-generator .

# Minikube'u başlat
minikube start

# Yerel Docker ortamını Minikube'a yönlendir
eval $(minikube docker-env)

# Kubernetes Deployment ve Service kaynaklarını uygula
kubectl apply -f deployment.yaml

# Podların durumunu kontrol et
kubectl get pods

# Servis durumunu kontrol et
kubectl get svc

# Port yönlendirme ile local erişimi sağla
kubectl port-forward deployment/ai-code-generator 5005:5001
```

## 📡 API Kullanımı

### Endpoint ve İstek Yapısı

*   **Endpoint:** `POST /generate`
*   **Request Body (JSON):**
    ```json
    {
      "prompt": "Bir listeyi sıralayan Python kodu yaz"
    }
    ```

### Örnek `curl` Komutu

```bash
curl -X POST http://127.0.0.1:5005/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Bir listeyi sıralayan Python kodu yaz"}'
```

### Örnek Yanıt

```json
{
  "code": "# -*- coding: utf-8 -*-\n\nliste = [5, 2, 8, 1, 9]\nliste.sort()\nprint(liste)\n",
  "title": "Liste Sıralama"
}
```

## 🚀 Helm ile Kurulum ve Yönetim

### Helm ile Dağıtım Yapmak

```bash
helm install ai-code-generator ./ai-code-generator
```

### Helm ile Dağıtımı Güncellemek

```bash
helm upgrade ai-code-generator ./ai-code-generator
```

### Helm ile Dağıtımı Silmek

```bash
helm uninstall ai-code-generator
```

## 💡 Gelecek Geliştirmeler (Güvenlik)

*   Basic Authentication desteği eklenecek
*   SSL (HTTPS) desteği düşünülebilir

## 📞 İletişim

Bu proje ile ilgili sorularınız veya önerileriniz için:

*   **İsim:** Faruk İnce
*   **Email:** farukiince@gmail.com

