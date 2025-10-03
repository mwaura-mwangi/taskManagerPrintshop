from io import BytesIO
import pandas as pd
from flask import send_file
from .models import Job

def weekly_jobs_xlsx():
    jobs = Job.query.order_by(Job.created_at.desc()).limit(500).all()
    data = [{
        "ID": j.id, "Title": j.title, "Status": j.status,
        "Owner": j.owner_id, "Updated": j.updated_at
    } for j in jobs]
    df = pd.DataFrame(data)
    bio = BytesIO()
    with pd.ExcelWriter(bio, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Jobs")
    bio.seek(0)
    return send_file(bio, as_attachment=True, download_name="weekly_jobs.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
