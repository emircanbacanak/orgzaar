from flask import Flask
from api.routes import api_bp
import logging

def create_app():
    app = Flask(__name__)
    
    # Logging yapılandırması
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Blueprint'i kaydet
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)