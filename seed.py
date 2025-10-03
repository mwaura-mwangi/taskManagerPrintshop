import os
from pathlib import Path
from dotenv import load_dotenv

# Always load the .env file from your project root
ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env", override=True)

from app import create_app
from app.extensions import db
from app.models import User, Role, Job
from passlib.hash import pbkdf2_sha256 as hasher

app = create_app()
with app.app_context():
    db.create_all()

    # Create roles if missing
    for r in ["admin", "staff", "user"]:
        if not Role.query.filter_by(name=r).first():
            db.session.add(Role(name=r, description=f"{r} role"))
    db.session.commit()

    # Create admin user if missing
    admin = User.query.filter_by(email="admin@example.com").first()
    if not admin:
        admin = User(email="admin@example.com",
                     password = hasher.hash("admin123"),
                     active=True)
        admin.roles = [Role.query.filter_by(name="admin").first()]
        db.session.add(admin)
        db.session.commit()
        print("Created admin@example.com / admin123")

    # Seed some sample jobs if none exist
    if not Job.query.first():
        for i in range(1, 6):
            db.session.add(Job(title=f"Sample Job {i}",
                               status="Not Started",
                               owner_id=admin.id))
        db.session.commit()
        print("Seeded sample jobs")
