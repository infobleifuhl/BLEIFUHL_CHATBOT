from flask import Flask
from flask_cors import CORS

from config import DevelopmentConfig
from app.database import init_db
from app.routes import api_blueprint, pages_blueprint


def create_app():
    app = Flask(__name__)

    # Geliştirme ayarlarını yükle
    app.config.from_object(DevelopmentConfig)

    # CORS ayarlarını etkinleştir
    CORS(app)

    # Veritabanını başlat
    init_db(app)

    # Blueprint'leri kaydet
    app.register_blueprint(api_blueprint, url_prefix="/api")
    app.register_blueprint(pages_blueprint)

    @app.route("/health")
    def health():
        return {
            "basari": True,
            "mesaj": "BLEIFÜHL chatbot çalışıyor."
        }

    return app