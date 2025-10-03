FROM python:3.12-slim

# WeasyPrint deps (cairo/pango), build tools for Pillow, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    libpango-1.0-0 libcairo2 libpangoft2-1.0-0 libffi8 libxml2 libxslt1.1 \
    libjpeg62-turbo zlib1g libtiff5 libwebp7 ghostscript imagemagick poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV FLASK_ENV=production
CMD ["gunicorn","-w","3","-b","0.0.0.0:8000","wsgi:app"]
