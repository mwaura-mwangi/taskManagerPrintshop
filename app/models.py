from datetime import datetime
from flask_login import UserMixin

from .extensions import db

# Association table for many-to-many User <-> Role
roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id")),
)


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    last_login_at = db.Column(db.DateTime)
    confirmed_at = db.Column(db.DateTime)

    # Roles m2m
    roles = db.relationship("Role", secondary=roles_users, backref="users")


class Template(db.Model):
    __tablename__ = "templates"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    preset = db.Column(db.JSON, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class Job(db.Model):
    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default="Not Started")  # Design/Tile/Print/Complete/Notify
    priority = db.Column(db.String(20), default="normal")
    due_date = db.Column(db.Date)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class JobFile(db.Model):
    __tablename__ = "job_files"
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), index=True)
    kind = db.Column(db.String(20))  # source, preview, output
    path = db.Column(db.String(500), nullable=False)
    mimetype = db.Column(db.String(120))
    meta = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Note(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), index=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AuditLog(db.Model):
    __tablename__ = "audit_logs"
    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    action = db.Column(db.String(80))
    entity = db.Column(db.String(80))
    entity_id = db.Column(db.Integer)
    extra = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
