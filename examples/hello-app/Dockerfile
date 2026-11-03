# Pin the base image version so every build uses the same Python.
# "slim" is a smaller Debian image: faster to pull and fewer packages to patch.
FROM python:3.13-slim

# Do not write .pyc files; send output straight to "docker logs" without buffering
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Create an unprivileged user; the app does not need root
RUN useradd --create-home --uid 1000 appuser

# Copy the code last: it changes most often, so earlier layers stay cached.
# In a real project, copy requirements.txt and run "pip install" before this line.
COPY app.py .

USER appuser

# Documentation only; you still need "-p 8000:8000" when running the container
EXPOSE 8000

# Exec form (JSON array): python runs as PID 1 and receives SIGTERM from "docker stop".
# Shell form (CMD python app.py) would run it under /bin/sh, which does not forward signals.
# PID 1 ignores SIGTERM unless the app handles it, so app.py installs a handler.
CMD ["python", "app.py"]
