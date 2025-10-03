from pathlib import Path
from .extensions import db
from .models import Job, JobFile
from .utils.pdf_tools import pdf_to_png_preview
from .utils.imaging import add_crop_marks, tile_business_cards
from celery_worker import celery

@celery.task(name="app.tasks.preflight")
def preflight(job_id: int):
    job = Job.query.get(job_id)
    source = JobFile.query.filter_by(job_id=job.id, kind="source").first()
    if source and source.path.lower().endswith(".pdf"):
        pdf_to_png_preview(Path(source.path), Path(source.path).parent / "preview")
    job.status = "Tile"
    db.session.commit()
    return True

@celery.task(name="app.tasks.tile_and_marks")
def tile_and_marks(job_id: int, cols=3, rows=3):
    src = JobFile.query.filter_by(job_id=job_id, kind="source").first()
    out = Path(src.path).parent / "output" / "sheet.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    tile_business_cards(Path(src.path), out, cols=cols, rows=rows)
    add_crop_marks(out, out)
    job = Job.query.get(job_id)
    job.status = "Print"
    db.session.commit()
    return str(out)
