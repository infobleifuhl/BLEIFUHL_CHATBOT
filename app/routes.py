from flask import Blueprint, request, jsonify, render_template
from app.services.ai_service import ai_service, AIServiceError
from app import database


api = Blueprint("api", __name__)
pages = Blueprint("pages", __name__)


@pages.route("/")
def index():
    return render_template("index.html")


@pages.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@api.route("/sohbet", methods=["POST"])
def sohbet():
    data = request.get_json()

    mesaj = data.get("mesaj")
    gecmis = data.get("gecmis", [])

    if not mesaj:
        return jsonify({
            "basari": False,
            "hata": "Mesaj gerekli."
        }), 400

    try:
        cevap = ai_service.yanit_uret(mesaj, gecmis)

        return jsonify({
            "basari": True,
            "cevap": cevap
        })

    except AIServiceError as e:
        return jsonify({
            "basari": False,
            "hata": str(e)
        }), 503


@api.route("/leads", methods=["POST"])
def lead_ekle():
    data = request.get_json()

    isim = data.get("isim")
    telefon = data.get("telefon")
    mesaj = data.get("mesaj", "")

    if not isim or not telefon:
        return jsonify({
            "basari": False,
            "hata": "İsim ve telefon gerekli."
        }), 400

    try:
        database.lead_ekle(isim, telefon, mesaj)

        return jsonify({
            "basari": True,
            "mesaj": "Lead kaydedildi."
        }), 201

    except Exception as e:
        return jsonify({
            "basari": False,
            "hata": str(e)
        }), 500


@api.route("/leads", methods=["GET"])
def leadleri_getir():
    try:
        leads = database.tum_leadler()

        return jsonify({
            "basari": True,
            "leadler": [dict(lead) for lead in leads]
        })

    except Exception as e:
        return jsonify({
            "basari": False,
            "hata": str(e)
        }), 500


api_blueprint = api
pages_blueprint = pages