from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mailman import Mail
from flask_caching import Cache
from flask_wtf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
cache = Cache()
csrf = CSRFProtect()

__all__ = ["db", "migrate", "login_manager", "mail", "cache", "csrf"]
