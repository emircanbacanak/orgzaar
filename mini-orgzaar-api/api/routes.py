from flask import Blueprint, jsonify, request
from datetime import datetime
import random
import logging

api_bp = Blueprint('api', __name__)
logger = logging.getLogger(__name__)

# Hardcoded servis listesi
SERVICES = [
    {"id": 1, "name": "DJ Hizmeti (2 Saat)", "category": "Müzik & Sanatçı", "price": 5000},
    {"id": 2, "name": "Masa Süsleme (Romantik)", "category": "Dekorasyon & Süsleme", "price": 1500},
    {"id": 3, "name": "Catering (Kişi Başı)", "category": "Yemek & İkram", "price": 800},
    {"id": 4, "name": "Canlı Müzik Grubu (3 Saat)", "category": "Müzik & Sanatçı", "price": 8500},
    {"id": 5, "name": "Fotoğraf Çekimi (Tüm Gün)", "category": "Fotoğraf & Video", "price": 3500},
    {"id": 6, "name": "Pasta ve Tatlı İkramı", "category": "Yemek & İkram", "price": 1200},
    {"id": 7, "name": "Çiçek Düzenleme", "category": "Dekorasyon & Süsleme", "price": 2000},
    {"id": 8, "name": "Işık ve Ses Sistemi", "category": "Teknik Ekipman", "price": 4000},
    {"id": 9, "name": "Animatör Hizmeti (Çocuklar İçin)", "category": "Eğlence", "price": 2500},
    {"id": 10, "name": "Vale Hizmeti", "category": "Ek Hizmetler", "price": 1500}
]
#tüm hizmetleri listeler
@api_bp.route('/services', methods=['GET'])
def get_services():
    logger.info("Hizmet listesi istendi")
    return jsonify(SERVICES), 200

#rezervasyon talepleri
@api_bp.route('/bookings', methods=['POST'])
def create_booking():
    try:
        data = request.get_json()
        
        # Veri yoksa hata döndür
        if not data:
            logger.warning("Rezervasyon isteği boş veri ile geldi")
            return jsonify({
                "error": "Geçersiz veri.",
                "details": {"request": "JSON verisi gönderilmelidir."}
            }), 400
        
        # Validasyon
        validation_error = validate_booking_data(data)
        if validation_error:
            logger.warning(f"Validasyon hatası: {validation_error}")
            return jsonify(validation_error), 400
        
        # Rezervasyon ID'si oluştur
        booking_id = random.randint(1000, 9999)
        logger.info(f"Yeni rezervasyon oluşturuldu - ID: {booking_id}, Tarih: {data.get('event_date')}")
        return jsonify({
            "message": "Rezervasyon talebiniz alındı.",
            "booking_id": booking_id
        }), 201
        
    except Exception as e:
        logger.error(f"Rezervasyon oluşturulurken hata: {str(e)}")
        return jsonify({
            "error": "Beklenmeyen bir hata oluştu.",
            "details": {"message": str(e)}
        }), 500

def validate_booking_data(data):
    # service_ids kontrolü
    if 'service_ids' not in data:
        return {
            "error": "Geçersiz veri.",
            "details": {"service_ids": "Bu alan zorunludur."}
        }
    
    if not isinstance(data['service_ids'], list):
        return {
            "error": "Geçersiz veri.",
            "details": {"service_ids": "Bu alan bir liste olmalıdır."}
        }
    
    # event_date kontrolü
    if 'event_date' not in data:
        return {
            "error": "Geçersiz veri.",
            "details": {"event_date": "Bu alan zorunludur."}
        }
    
    # Tarih formatı kontrolü
    try:
        event_date = datetime.strptime(data['event_date'], '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return {
            "error": "Geçersiz veri.",
            "details": {"event_date": "Tarih formatı YYYY-MM-DD olmalıdır ve gelecek bir tarih olmalıdır."}
        }
    
    # Geçmiş tarih kontrolü
    today = datetime.now().date()
    if event_date < today:
        return {
            "error": "Geçersiz veri.",
            "details": {"event_date": "Tarih formatı YYYY-MM-DD olmalıdır ve gelecek bir tarih olmalıdır."}
        }
    
    # notes kontrolü (opsiyonel ama varsa string olmalı)
    if 'notes' in data and data['notes'] is not None and not isinstance(data['notes'], str):
        return {
            "error": "Geçersiz veri.",
            "details": {"notes": "Bu alan string formatında olmalıdır."}
        }
    
    return None