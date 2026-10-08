FROM python:3.12-slim

# Don't write .pyc files into the image, and don't buffer stdout/stderr,
# so logs show up immediately in `docker logs`.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencies first: this layer is only rebuilt when requirements.txt changes.
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Only the application package, not the whole repo (no .env, .venv, tests, db files).
COPY ./app ./app

# Don't run the server as root.
RUN useradd --create-home --uid 1000 appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]