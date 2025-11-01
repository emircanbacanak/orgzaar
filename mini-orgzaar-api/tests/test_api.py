import pytest
from datetime import datetime, timedelta
from app import create_app

@pytest.fixture
def client():
    #Test client oluşturur
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_services(client):
    #GET /api/v1/services endpoint'ini test eder
    response = client.get('/api/v1/services')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 3  # En az 3 hizmet olmalı
    assert len(data) == 10  # Şu an 10 hizmet var
    assert data[0]['id'] == 1
    assert data[0]['name'] == "DJ Hizmeti (2 Saat)"
    assert 'category' in data[0]
    assert 'price' in data[0]

def test_create_booking_success(client):
    #POST /api/v1/bookings endpoint'ini başarılı senaryo ile test eder
    # Gelecek bir tarih
    future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    response = client.post('/api/v1/bookings', json={
        "service_ids": [1, 3],
        "event_date": future_date,
        "notes": "Yılbaşı kutlaması için."
    })
    
    assert response.status_code == 201
    data = response.get_json()
    
    assert 'message' in data
    assert 'booking_id' in data
    assert data['message'] == "Rezervasyon talebiniz alındı."
    assert 1000 <= data['booking_id'] <= 9999

def test_create_booking_missing_service_ids(client):
    #service_ids alanı eksik olduğunda hata döndürür
    future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    response = client.post('/api/v1/bookings', json={
        "event_date": future_date
    })
    
    assert response.status_code == 400
    data = response.get_json()
    
    assert 'error' in data
    assert 'details' in data
    assert 'service_ids' in data['details']

def test_create_booking_missing_event_date(client):
    #event_date alanı eksik olduğunda hata döndürür
    response = client.post('/api/v1/bookings', json={
        "service_ids": [1, 2]
    })
    
    assert response.status_code == 400
    data = response.get_json()
    
    assert 'error' in data
    assert 'details' in data
    assert 'event_date' in data['details']

def test_create_booking_invalid_date_format(client):
    #Geçersiz tarih formatı ile hata döndürür
    response = client.post('/api/v1/bookings', json={
        "service_ids": [1],
        "event_date": "24-12-2025"  # Yanlış format
    })
    
    assert response.status_code == 400
    data = response.get_json()
    
    assert 'error' in data
    assert 'details' in data
    assert 'event_date' in data['details']

def test_create_booking_past_date(client):
    #Geçmiş tarih ile hata döndürür
    past_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    response = client.post('/api/v1/bookings', json={
        "service_ids": [1],
        "event_date": past_date
    })
    
    assert response.status_code == 400
    data = response.get_json()
    
    assert 'error' in data
    assert 'details' in data
    assert 'event_date' in data['details']

def test_create_booking_empty_service_ids(client):
    #Boş service_ids listesi ile başarılı rezervasyon oluşturur
    future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    response = client.post('/api/v1/bookings', json={
        "service_ids": [],
        "event_date": future_date
    })
    assert response.status_code == 201

def test_create_booking_with_notes(client):
    #notes alanı ile başarılı rezervasyon oluşturur
    future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    response = client.post('/api/v1/bookings', json={
        "service_ids": [1, 2, 3],
        "event_date": future_date,
        "notes": "Özel not"
    })
    assert response.status_code == 201

def test_create_booking_invalid_notes_type(client):
    #notes alanı string değilse hata döndürür
    future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    response = client.post('/api/v1/bookings', json={
        "service_ids": [1],
        "event_date": future_date,
        "notes": 12345  # String olmalı
    })
    
    assert response.status_code == 400
    data = response.get_json()

    assert 'error' in data
    assert 'details' in data
    assert 'notes' in data['details']