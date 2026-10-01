# BLEIFÜHL – SmartLead AI Chatbot

BLEIFÜHL SmartLead AI, ziyaretçilerle iletişim kurabilen, yapay zekâ destekli yanıtlar üreten ve potansiyel müşteri (lead) bilgilerini kaydeden bir chatbot uygulamasıdır.

Proje; **Wix, Velo, Python, Flask, SQLite ve Groq API** kullanılarak geliştirilmiştir.

## Projenin Amacı

Projenin amacı, BLEIFÜHL web sitesini ziyaret eden kullanıcıların hizmetler hakkında bilgi alabilmesini ve ihtiyaçlarını chatbot üzerinden iletebilmesini sağlamaktır.

Chatbot üzerinden alınan isim ve telefon bilgileri SQLite veritabanına kaydedilir ve yönetici tarafından kontrol paneli üzerinden görüntülenebilir.

## Kullanılan Teknolojiler

* **Python** – Backend geliştirme
* **Flask** – Web uygulaması ve API
* **SQLite** – Lead verilerinin saklanması
* **Groq API** – Yapay zekâ destekli chatbot yanıtları
* **Wix / Velo** – Web sitesi ve frontend
* **Render** – Backend deployment
* **GitHub** – Kod ve versiyon kontrolü

## Proje Yapısı

```text
BLEIFUHL_CHATBOT/
│
├── run.py
├── config.py
├── requirements.txt
├── .env
├── .gitignore
│
└── app/
    ├── __init__.py
    ├── database.py
    ├── routes.py
    │
    ├── templates/
    │   ├── index.html
    │   └── dashboard.html
    │
    └── services/
        ├── __init__.py
        └── ai_service.py
```

## Backend Katmanları

Proje modüler bir yapıda geliştirilmiştir.

### `run.py`

Flask uygulamasını başlatır.

### `config.py`

Uygulama ayarlarını, API anahtarlarını ve BLEIFÜHL işletme bağlamını yönetir.

### `database.py`

SQLite veritabanı işlemlerinden sorumludur.

Lead ekleme ve lead listeleme işlemleri bu katman üzerinden gerçekleştirilir.

### `routes.py`

HTTP isteklerini karşılar ve ilgili servis veya veritabanı fonksiyonlarını çağırır.

### `ai_service.py`

Groq API ile yapay zekâ iletişimini yönetir.

Yapay zekâ API çağrıları bu dosya üzerinden gerçekleştirilir.

## API Endpoint'leri

### `GET /`

Ana backend sayfasını kontrol eder.

### `GET /dashboard`

Kontrol panelini açar.

### `POST /api/sohbet`

Chatbot mesajını yapay zekâ servisine gönderir ve oluşturulan yanıtı döndürür.

Örnek istek:

```json
{
    "mesaj": "Düğün davetiyesi hakkında bilgi almak istiyorum.",
    "gecmis": []
}
```

### `POST /api/leads`

Kullanıcının isim, telefon ve mesaj bilgilerini SQLite veritabanına kaydeder.

Örnek:

```json
{
    "isim": "Test Kullanıcı",
    "telefon": "05550000000",
    "mesaj": "Davet tasarımı hakkında bilgi almak istiyorum."
}
```

### `GET /api/leads`

Kaydedilen lead bilgilerini getirir ve kontrol panelinde görüntülenmesini sağlar.

### `GET /health`

Backend servisinin çalışıp çalışmadığını kontrol etmek için kullanılır.

Başarılı durumda:

```json
{
    "basari": true,
    "mesaj": "BLEIFÜHL chatbot çalışıyor."
}
```

## Yapay Zekâ Entegrasyonu

Chatbot, Groq API üzerinden yapay zekâ modeli kullanmaktadır.

Kullanılan model:

```text
openai/gpt-oss-20b
```

Yapay zekâya gönderilen mesaj yapısı:

```text
System → Conversation History → User Message
```

BLEIFÜHL'e ait işletme bilgileri ve chatbot davranışı `BUSINESS_CONTEXT` üzerinden yönetilir.

API anahtarı kod içerisinde tutulmaz ve `.env` dosyasında saklanır.

## Kurulum

Projeyi çalıştırmak için Python sanal ortamı oluşturulur:

```bash
python -m venv venv
```

Sanal ortam etkinleştirildikten sonra gerekli paketler yüklenir:

```bash
pip install -r requirements.txt
```

`.env` dosyasına gerekli bilgiler eklenir:

```env
GROQ_API_KEY=your_api_key
SECRET_KEY=your_secret_key
```

Uygulama aşağıdaki komutla çalıştırılır:

```bash
python run.py
```

Uygulama varsayılan olarak aşağıdaki adreste çalışır:

```text
http://127.0.0.1:5000
```

## Wix Entegrasyonu

Wix web sitesindeki chatbot arayüzü **Velo** kullanılarak geliştirilmiştir.

Wix tarafı, backend API'sine HTTP istekleri göndererek:

* Kullanıcı mesajlarını chatbot servisine iletir.
* Yapay zekâdan gelen cevabı kullanıcıya gösterir.
* Kullanıcı bilgilerini lead API'sine gönderir.
* Kaydedilen lead bilgilerini kontrol panelinde görüntüler.

## Deployment

Backend uygulaması **Render** üzerinde yayınlanmıştır.

Canlı backend:

```text
https://bleifuhl-chatbot.onrender.com
```

Wix sitesi, canlı backend API'si ile iletişim kurmaktadır.

## Güvenlik

* API anahtarı `.env` dosyasında tutulmaktadır.
* `.env` dosyası `.gitignore` içerisinde yer almaktadır.
* Veritabanı dosyası GitHub'a gönderilmemektedir.
* SQL sorgularında parametreli sorgular (`?` placeholders) kullanılmaktadır.
* Yapay zekâ API çağrıları ayrı bir servis katmanında tutulmaktadır.
* Harici API isteklerinde hata yönetimi uygulanmaktadır.

## Testler

Projenin canlı testleri gerçekleştirilmiştir.

Test edilen temel işlemler:

* Chatbot mesaj gönderme
* Yapay zekâdan yanıt alma
* İsim ve telefon bilgisi gönderme
* Lead kaydetme
* SQLite veritabanına kayıt
* Dashboard üzerinden lead görüntüleme
* Backend health kontrolü
* Wix ve Render arasındaki API iletişimi

Tüm temel uçtan uca işlemler başarıyla test edilmiştir.

## Canlı Bağlantılar

**Wix Web Sitesi:**

https://infobleifuhl.wixstudio.com/my-site-1

**Backend / Render:**

https://bleifuhl-chatbot.onrender.com

**GitHub Repository:**

https://github.com/infobleifuhl/BLEIFUHL_CHATBOT.git

## Proje Durumu

**BLEIFÜHL SmartLead AI MVP tamamlanmış ve canlı ortamda test edilmiştir.**
