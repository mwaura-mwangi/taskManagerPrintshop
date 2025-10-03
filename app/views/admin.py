from flask import Blueprint, render_template
from flask_login import login_required
from ..models import User, Job, AuditLog

bp = Blueprint("admin", __name__, url_prefix="/admin")

@bp.get("/")
@login_required
def dashboard():
    users = User.query.count()
    jobs = Job.query.count()
    audits = AuditLog.query.count()
    return render_template("admin/dashboard.html", users=users, jobs=jobs, audits=audits)
