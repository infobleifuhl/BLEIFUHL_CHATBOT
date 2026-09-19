import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    DATABASE_URL = os.environ.get("DATABASE_URL", "leads.db")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
    AI_PROVIDER = os.environ.get("AI_PROVIDER", "groq")

    BUSINESS_CONTEXT = os.environ.get(
        "BUSINESS_CONTEXT",
        """BLEIFÜHL is a creative brand focused on personalized invitations,
posters, cards, and wedding and event experiences.
The brand's core concept is "stay in the moment, feel, live the moment,
atmosphere architect and design".
The target audience is young and dynamic couples who are getting married
and people looking for personalized invitations and event experiences."""
    )

    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}