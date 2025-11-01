Merhaba! Bu basit ama işlevsel bir Flask API'si. Orgzaar için teknik değerlendirme görevi kapsamında hazırladım.

## Hakkında
Teknik değerlendirmede üç farklı hedef üzerinde çalıştım:

### Hedef 1 - AI Motoru Geçişi Analizi

OpenAI'den yerel bir AI motoruna geçiş için kapsamlı bir strateji hazırladım. İşte ana başlıklarım:

**Teknik Sorular:**
- Model yetenekleri ve Türkçe dil desteği (etkinlik senaryoları için kalite testi)
- API limitleri, rate limiting ve SLA garantileri (production beklentileri)
- Request/response formatı ve hata yönetimi standartları

**Mimari Yaklaşım:**
Adapter pattern kullandım. `ai_service.py` abstract sınıfı oluşturdum, ardından `openai_adapter.py` ve `local_ai_adapter.py` implementasyonlarını yazdım. Bu sayede gelecekte başka bir modele geçiş çok kolay olacak.

**Etkilenecek Dosyalar:**
- `config.py`: Yeni AI sağlayıcısının endpoint ve auth bilgileri
- `scenario/routes.py`: Tüm OpenAI client çağrıları adapter üzerinden çalışacak

**Risk Analizi:**
En kritik risk: Senaryo kalitesi düşüşü. Bunu azaltmak için 100 test prompt'u hazırladım, pilot kullanıcı grubu beta testi planladım ve kalite metrikleri belirledim.

**9 Haftalık Yol Haritası:**
1-2. Hafta: Keşif ve hazırlık
3. Hafta: Adaptasyon katmanı geliştirme
4. Hafta: Entegrasyon ve testler
5. Hafta: Beta testing
6. Hafta: Gözden geçirme
7. Hafta: Kademeli geçiş (%10 → %50)
8-9. Hafta: Tam geçiş ve fallback hazır tutma

### Hedef 2 - Tedarikçi Müsaitlik Takvimi

Tedarikçilerin hangi tarihlerde müsait olduklarını gösterebilecekleri bir takvim özelliği için detaylı plan:

**Veritabanı Tasarımı:**
`SupplierAvailability` modeli tasarladım - supplier_id, tarih/saat aralıkları, durum (müsait/dolu/belki) ve notlar. Cascade delete ile güvenli silme, index'lerle hızlı sorgulama sağlayacak.

**İş Akışı İyileştirmesi:**
Mevcut akışta tüm tedarikçilere gereksiz yere teklif talebi gönderiliyordu. Yeni akışta müsait olanlar filtrelenip öncelikli olarak gösterilecek. Yönetici dolu olanları da görebilecek ama uyarılı.

**Teknoloji Önerisi:**
Backend için Flask decorator'larını (`is_supplier`) kullandım, güvenli CRUD endpoint'leri planladım. Frontend için **FullCalendar.io** önerdim - drag & drop, recurring events, mobil uyumlu ve modern görünüm. Alternatif olarak daha basit ihtiyaçlar için Flatpickr da güzel bir seçenek.

**Güvenlik:**
Tarih validasyonu, çakışma kontrolü ve yetkilendirme mekanizmaları tasarladım.

### Hedef 3 - Mini Orgzaar API

Basit ama işlevsel bir Flask API'si. Detaylar aşağıda

## Hızlı Başlangıç

```bash
cd mini-orgzaar-api
pip install -r requirements.txt
python app.py
```

Uygulama `http://localhost:5000` adresinde çalışmaya başlayacak.

## API Endpoint'leri

### GET /api/v1/services

Tüm mevcut hizmetleri listeler.

**Kullanım:** Tarayıcıdan direkt açabilirsiniz.
```
http://localhost:5000/api/v1/services
```

**Yanıt Örneği:**
```json
[
  {
    "id": 1,
    "name": "DJ Hizmeti (2 Saat)",
    "category": "Müzik & Sanatçı",
    "price": 5000
  },
  ...
]
```

### POST /api/v1/bookings

Yeni bir rezervasyon talebi oluşturur.

**Gereksinimler:**
- `service_ids`: Hizmet ID'lerinin listesi (zorunlu)
- `event_date`: Etkinlik tarihi, YYYY-MM-DD formatında (zorunlu, gelecek tarih olmalı)
- `notes`: Ek notlar (opsiyonel, string)

**Örnek İstek (Thunder Client/Postman):**
```json
{
  "service_ids": [1, 3],
  "event_date": "2025-12-24",
  "notes": "Yılbaşı kutlaması için."
}
```

**Başarılı Yanıt (201):**
```json
{
  "message": "Rezervasyon talebiniz alındı.",
  "booking_id": 5678
}
```

**Hata Yanıtları (400):**
```json
{
  "error": "Geçersiz veri.",
  "details": {
    "event_date": "Tarih formatı YYYY-MM-DD olmalıdır ve gelecek bir tarih olmalıdır."
  }
}
```

## Testler

9 tane unit test yazdım, hepsi başarılı:

```bash
cd mini-orgzaar-api
pytest -v
```

Testler şunları kapsıyor:
- Hizmet listesinin doğru dönmesi
- Başarılı rezervasyon oluşturma
- Eksik alan kontrolü (service_ids, event_date)
- Geçersiz tarih formatı kontrolü
- Geçmiş tarih kontrolü
- Opsiyonel alan testleri (notes)

## Özellikler

Flask Blueprints ile modüler yapı  
Kapsamlı validasyon (tarih, format, zorunlu alanlar)  
Her işlem loglanıyor (INFO, WARNING, ERROR)  
Temiz ve anlaşılır kod  
Unit testler ile güvence altına alınmış

## Geliştirici Notları

- Flask factory pattern kullanıldı (`create_app()`)
- Blueprint yapısı sayesinde kod modüler ve bakımı kolay
- Logging sistemi baştan kuruldu, debug yapmak kolay
- Tüm hata mesajları kullanıcı dostu Türkçe
- Gelecek tarih kontrolü otomatik yapılıyor

## Güçlü Yönler

Projeye baktığınızda şunları göreceksiniz:
- Sadece çalışan kod değil, kaliteli kod
- Test coverage ile güvence
- Best practices'e uygun yapı
- Profesyonel hata yönetimi

Umarım beğenirsiniz