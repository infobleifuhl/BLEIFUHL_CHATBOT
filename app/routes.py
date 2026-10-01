from flask import Blueprint, request, jsonify, render_template, redirect, session
from app.services.ai_service import ai_service, AIServiceError
from app import database


api = Blueprint("api", __name__)
pages = Blueprint("pages", __name__)


# Ana sayfa
@pages.route("/")
def index():
    return render_template("index.html")


# Admin giriş
@pages.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    from config import Config

    if username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD:
        session["admin_logged_in"] = True

        print("LOGIN SESSION:", session.get("admin_logged_in"))

        return redirect("/dashboard")

    return "Kullanıcı adı veya şifre hatalı.", 401


# Admin dashboard
@pages.route("/dashboard")
def dashboard():
    print("DASHBOARD SESSION:", session.get("admin_logged_in"))

    if not session.get("admin_logged_in"):
        return redirect("/login")

    return render_template("dashboard.html")


# Chatbot
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


# Yeni lead kaydet
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


# Leadleri getir - sadece admin
@api.route("/leads", methods=["GET"])
def leadleri_getir():

    if not session.get("admin_logged_in"):
        return jsonify({
            "basari": False,
            "hata": "Yetkisiz erişim."
        }), 401

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