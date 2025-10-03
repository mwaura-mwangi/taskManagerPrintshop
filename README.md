
# PrintShop – Job & Print Management System

PrintShop is a Flask-based web application that manages design/print jobs from creation to completion.  
It allows you to track job progress, upload files, attach notes, and send files to a printer (local CUPS / PDF output).

---

## Features
- User authentication (login & registration with hashed passwords)
- Role-based accounts (Users & Admins)
- Job lifecycle tracking:
  - Not Started → Design → Tile → Print → Complete → Notify
- File uploads with storage per job
- Notes & comments per job
- Printing integration:
  - Local printing via **CUPS** (Linux)
  - Virtual PDF printer for testing
- Flash messages & clean UI with HTML templates
- CSRF protection & secure forms

---

## Project Structure
```

printshop/
│
├── app/
│   ├── **init**.py        # Flask app factory & blueprints
│   ├── config.py          # Config (Dev/Prod, DB, Mail, Cache, Printer)
│   ├── extensions.py      # SQLAlchemy, LoginManager, etc.
│   ├── models.py          # User, Role, Job, JobFile, Note, AuditLog
│   ├── forms.py           # WTForms (Login, Register, JobForm)
│   ├── print_utils.py     # Print helpers (CUPS or lp)
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── jobs/
│   │   │   ├── list.html
│   │   │   ├── detail.html
│   │   │   └── create.html
│   └── views/
│       ├── users.py
│       ├── jobs.py
│       └── admin.py
│
├── migrations/            # Flask-Migrate (Alembic) migrations
├── storage/               # Uploaded job files
├── seed.py                # Database seeder (admin + sample jobs)
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation

````

---

## Installation

### 1. Clone & setup environment
```bash
git clone https://github.com/yourname/printshop.git
cd printshop
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
````

### 2. Setup Postgres

```bash
sudo -u postgres psql
CREATE USER printshop_user WITH PASSWORD "...";
CREATE DATABASE printshop OWNER printshop_user;
GRANT ALL PRIVILEGES ON DATABASE printshop TO printshop_user;
```

### 3. Configure environment

Create `.env`:

```env
FLASK_ENV=development
SECRET_KEY=your-secret
SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://printshop_user:xxxx@localhost:5432/printshop
SECURITY_PASSWORD_SALT=mysalt
PRINTER_NAME=PDF
FILE_STORAGE_DIR=./storage
ALLOWED_EXT=pdf,png,jpg,jpeg,tif,tiff,ai,eps
```

### 4. Initialize database

```bash
flask --app app:create_app db init
flask --app app:create_app db migrate -m "init"
flask --app app:create_app db upgrade
python seed.py
```

### 5. Run server

```bash
flask --app app:create_app run --port 5000 --debug
```

App will be live at:
 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Printing Setup

### Local (Linux CUPS)

```bash
sudo apt install cups python3-cups
sudo systemctl enable --now cups
lpstat -p -d    # list printers
```

Example print:

```bash
lp -d PDF /usr/share/cups/data/testprint
```

### Virtual PDF printer

* Add **CUPS-PDF** as a virtual printer for testing.
* Output will be saved in your `~/PDF` directory.

---

## Users

* Admin account seeded:

  * Email: `admin@example.com`
  * Password: `admin123`

You can register new users via `/auth/register`.

---

## Tech Stack

* **Backend:** Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF
* **Database:** PostgreSQL (SQLite fallback for dev)
* **Auth:** Flask-Login + Passlib (pbkdf2)
* **Frontend:** Jinja2 templates + CSS
* **Printing:** pycups / lp (Linux CUPS)

---

## Roadmap

* [ ] File previews in browser
* [ ] Background print queue (Celery + Redis)
* [ ] Admin dashboard with job stats
* [ ] Cloud-friendly print export (PDF downloads)

---

## License

MIT License.
Feel free to use, improve, and share.
