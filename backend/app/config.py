import os
from pathlib import Path


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Render PostgreSQL often provides DATABASE_URL. Use it when available.
    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    else:
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT", "5432")
        DB_NAME = os.getenv("DB_NAME")
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")

        if all([DB_HOST, DB_NAME, DB_USER, DB_PASSWORD]):
            SQLALCHEMY_DATABASE_URI = (
                f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            )
        else:
            # Local fallback so the app can run without PostgreSQL during testing.
            BASE_DIR = Path(__file__).resolve().parents[1]
            INSTANCE_DIR = BASE_DIR / "instance"
            INSTANCE_DIR.mkdir(exist_ok=True)
            SQLALCHEMY_DATABASE_URI = f"sqlite:///{INSTANCE_DIR / 'major_recommender.db'}"
