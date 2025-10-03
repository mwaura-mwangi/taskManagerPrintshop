from pathlib import Path
import fitz  # PyMuPDF

def pdf_to_png_preview(pdf_path: Path, out_dir: Path, dpi=144):
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(pdf_path))
    images = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=dpi)
        out = out_dir / f"page-{i+1:03}.png"
        pix.save(str(out))
        images.append(out)
    return images
