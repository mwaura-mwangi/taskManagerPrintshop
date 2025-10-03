import os

class Base:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "sqlite:///instance/printshop.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security / CSRF
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT", "salt")

    # Mail
    MAIL_SERVER = os.getenv("MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 25))
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "no-reply@printshop.local")

    # Cache
    CACHE_TYPE = "SimpleCache" if "sqlite" in SQLALCHEMY_DATABASE_URI else "RedisCache"
    CACHE_REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Files / printing
    FILE_STORAGE_DIR = os.getenv("FILE_STORAGE_DIR", "./storage")
    PRINTER_NAME = os.getenv("PRINTER_NAME", "PDF")
    ALLOWED_EXT = set((os.getenv("ALLOWED_EXT") or "").split(","))

class Dev(Base):
    DEBUG = True

class Prod(Base):
    DEBUG = False
