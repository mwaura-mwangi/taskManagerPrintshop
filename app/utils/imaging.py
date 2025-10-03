from PIL import Image, ImageDraw
from pathlib import Path

def add_crop_marks(img_path: Path, out_path: Path, margin=30, mark_len=20, width=2):
    img = Image.open(img_path).convert("RGB")
    w, h = img.size
    canvas = Image.new("RGB", (w + 2*margin, h + 2*margin), "white")
    canvas.paste(img, (margin, margin))
    d = ImageDraw.Draw(canvas)
    # corners
    d.line([(margin, margin - mark_len), (margin, margin + mark_len)], fill="black", width=width)
    d.line([(margin - mark_len, margin), (margin + mark_len, margin)], fill="black", width=width)
    d.line([(w+margin, margin - mark_len), (w+margin, margin + mark_len)], fill="black", width=width)
    d.line([(w+margin - mark_len, margin), (w+margin + mark_len, margin)], fill="black", width=width)
    d.line([(margin, h+margin - mark_len), (margin, h+margin + mark_len)], fill="black", width=width)
    d.line([(margin - mark_len, h+margin), (margin + mark_len, h+margin)], fill="black", width=width)
    d.line([(w+margin, h+margin - mark_len), (w+margin, h+margin + mark_len)], fill="black", width=width)
    d.line([(w+margin - mark_len, h+margin), (w+margin + mark_len, h+margin)], fill="black", width=width)
    canvas.save(out_path)
    return out_path

def tile_business_cards(img_path: Path, out_path: Path, cols=3, rows=3, gap=10):
    card = Image.open(img_path).convert("RGB")
    cw, ch = card.size
    W = cols*cw + (cols-1)*gap
    H = rows*ch + (rows-1)*gap
    sheet = Image.new("RGB", (W, H), "white")
    for r in range(rows):
        for c in range(cols):
            x = c*(cw+gap); y = r*(ch+gap)
            sheet.paste(card, (x, y))
    sheet.save(out_path)
    return out_path

def nudge(img_path: Path, out_path: Path, dx=0, dy=0):
    img = Image.open(img_path)
    W, H = img.size
    canvas = Image.new(img.mode, (W, H), "white")
    canvas.paste(img, (dx, dy))
    canvas.save(out_path)
    return out_path
