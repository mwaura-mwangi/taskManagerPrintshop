from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from passlib.hash import pbkdf2_sha256 as hasher
from ..extensions import db
from ..models import User
from ..forms import LoginForm, RegisterForm

bp = Blueprint("users", __name__, url_prefix="/auth")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("jobs.list_jobs"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Invalid email or password.", "danger")
            return render_template("auth/login.html", form=form)

        try:
            ok = hasher.verify(form.password.data, user.password)
        except Exception:
            ok = False

        if not ok:
            flash("Invalid email or password.", "danger")
            return render_template("auth/login.html", form=form)

        if not user.active:
            flash("Account is disabled. Contact admin.", "warning")
            return render_template("auth/login.html", form=form)

        login_user(user, remember=form.remember.data)
        flash("Signed in.", "success")
        next_url = request.args.get("next") or url_for("jobs.list_jobs")
        return redirect(next_url)

    return render_template("auth/login.html", form=form)


@bp.post("/logout")
@login_required
def logout():
    logout_user()
    flash("Signed out.", "success")
    return redirect(url_for("users.login"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            email = form.email.data.lower().strip()
            if User.query.filter_by(email=email).first():
                flash("Email already registered.", "warning")
                return render_template("auth/register.html", form=form)

            user = User(
                email=email,
                password=hasher.hash(form.password.data),  # PBKDF2-SHA256
                active=True,
            )
            db.session.add(user)
            db.session.commit()
            flash("Account created. You can now sign in.", "success")
            return redirect(url_for("users.login"))
        except Exception as e:
            current_app.logger.exception("Registration failed")
            flash(f"Registration error: {e}", "danger")
            db.session.rollback()

    return render_template("auth/register.html", form=form)
