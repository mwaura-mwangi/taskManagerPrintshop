import os
from flask import Flask, render_template
from flask_wtf.csrf import CSRFError, generate_csrf

from .config import Dev
from .extensions import db, migrate, login_manager, mail, cache, csrf


def create_app(config_object=Dev):
    app = Flask(
        __name__,
        instance_relative_config=True,
        static_folder="static",
        template_folder="templates",
    )
    app.config.from_object(config_object)

    # Ensure instance & storage dirs exist
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config.get("FILE_STORAGE_DIR", "./storage"), exist_ok=True)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    csrf.init_app(app)

    # Make csrf_token() available in ANY template (even when not using FlaskForm)
    app.jinja_env.globals["csrf_token"] = generate_csrf

    login_manager.login_view = "users.login"

    # Lazy imports to avoid circular / duplicate model registration
    with app.app_context():
        from .models import User

        @login_manager.user_loader
        def load_user(user_id: str):
            try:
                return User.query.get(int(user_id))
            except Exception:
                return None

        # Register blueprints
        from .views.admin import bp as admin_bp
        from .views.jobs import bp as jobs_bp
        from .views.users import bp as users_bp

        app.register_blueprint(jobs_bp)
        app.register_blueprint(users_bp)
        app.register_blueprint(admin_bp)

    # Routes
    @app.get("/")
    def index():
        return render_template("index.html")

    # Helpful CSRF error page so 400s show the reason
    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template("errors/csrf.html", reason=e.description), 400

    return app
