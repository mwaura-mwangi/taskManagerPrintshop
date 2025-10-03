# app/views/jobs.py
from pathlib import Path
import mimetypes

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from ..extensions import db
from ..models import Job, JobFile, Note
from ..forms import JobForm
from ..print_utils import print_with_cups  # or: from ..print_utils import print_with_lp

bp = Blueprint("jobs", __name__, url_prefix="/jobs")  # define FIRST


@bp.get("/")
@login_required
def list_jobs():
    status = (request.args.get("status") or "").strip() or None
    q = Job.query
    if status:
        q = q.filter_by(status=status)
    jobs = q.order_by(Job.updated_at.desc()).limit(100).all()
    return render_template("jobs/list.html", jobs=jobs, status=status)


@bp.get("/<int:job_id>")
@login_required
def detail(job_id):
    job = Job.query.get_or_404(job_id)
    files = JobFile.query.filter_by(job_id=job.id).all()
    notes = Note.query.filter_by(job_id=job.id).order_by(Note.created_at.desc()).all()
    return render_template("jobs/detail.html", job=job, files=files, notes=notes)


def _get_source_file(job_id: int):
    return (
        JobFile.query.filter_by(job_id=job_id, kind="source")
        .order_by(JobFile.id.asc())
        .first()
    )


def _send_to_printer(job: Job) -> bool:
    src = _get_source_file(job.id)
    if not src:
        flash("No source file found for this job.", "warning")
        return False

    # Prefer env-configured name; fall back to CUPS-PDF-Printer (your system’s name)
    printer = current_app.config.get("PRINTER_NAME") or "CUPS-PDF-Printer"

    # Common CUPS options; tweak as needed
    options = {
        "fit-to-page": "true",
        "media": "A4",
        # "sides": "two-sided-long-edge",
        # "landscape": "true",
        # "copies": "2",
    }

    try:
        cups_job_id = print_with_cups(src.path, printer=printer, options=options)
        flash(f"Queued for printing on '{printer}' (CUPS job #{cups_job_id}).", "success")
        current_app.logger.info("Print queued: job_id=%s file=%s printer=%s cups_job=%s",
                                job.id, src.path, printer, cups_job_id)
        return True
    except Exception as e:
        current_app.logger.exception("Printing failed for job_id=%s file=%s", job.id, src.path)
        flash(f"Printing failed: {e}", "danger")
        return False


@bp.post("/<int:job_id>/advance")
@login_required
def advance(job_id):
    job = Job.query.get_or_404(job_id)
    flow = ["Not Started", "Design", "Tile", "Print", "Complete", "Notify"]
    try:
        nxt = flow[flow.index(job.status) + 1]
    except (ValueError, IndexError):
        flash("Cannot advance further.", "warning")
        return redirect(url_for("jobs.detail", job_id=job.id))

    job.status = nxt
    db.session.commit()

    # Auto-print when entering the Print stage
    if nxt == "Print":
        _send_to_printer(job)

    flash(f"Advanced to {nxt}", "success")
    return redirect(url_for("jobs.detail", job_id=job.id))


@bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    form = JobForm()
    if form.validate_on_submit():
        job = Job(
            title=form.title.data.strip(),
            status="Design",
            priority=form.priority.data,
            due_date=form.due_date.data,
            owner_id=current_user.id,
        )
        db.session.add(job)
        db.session.commit()

        # File upload
        f = form.file.data
        if f and f.filename:
            filename = secure_filename(f.filename)
            ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

            cfg_allowed = current_app.config.get("ALLOWED_EXT", set()) or set()
            allowed = {e.strip().lower() for e in cfg_allowed if e and e.strip()}
            if allowed and ext not in allowed:
                flash(f"File type .{ext} not allowed. Allowed: {', '.join(sorted(allowed))}", "danger")
                return redirect(url_for("jobs.detail", job_id=job.id))

            storage = Path(current_app.config["FILE_STORAGE_DIR"]) / f"jobs/{job.id}/source"
            storage.mkdir(parents=True, exist_ok=True)
            path = storage / filename
            f.save(path)

            mimetype = f.mimetype or (mimetypes.guess_type(str(path))[0] or "application/octet-stream")
            db.session.add(JobFile(job_id=job.id, kind="source", path=str(path), mimetype=mimetype))
            db.session.commit()
            flash("Source file uploaded.", "success")

        # NEW: create initial note if provided
        if form.note.data and form.note.data.strip():
            note = Note(job_id=job.id, author_id=current_user.id, body=form.note.data.strip())
            db.session.add(note)
            db.session.commit()
            flash("Initial note saved.", "success")

        flash("Job created.", "success")
        return redirect(url_for("jobs.detail", job_id=job.id))

    if request.method == "POST" and form.errors:
        errs = "; ".join([f"{k}: {', '.join(v)}" for k, v in form.errors.items()])
        flash(f"Please fix: {errs}", "danger")

    return render_template("jobs/create.html", form=form)


@bp.post("/<int:job_id>/print")
@login_required
def print_job(job_id: int):
    job = Job.query.get_or_404(job_id)
    _send_to_printer(job)
    return redirect(url_for("jobs.detail", job_id=job.id))
