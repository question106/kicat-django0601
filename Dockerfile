FROM python:3.9-alpine3.19
LABEL maintainer="kjobslink.com"

ENV PYTHONUNBUFFERED=1

# Copy requirements first for better caching
COPY requirements.txt /requirements.txt

# Install dependencies
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home app && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R app:app /vol && \
    chmod -R 755 /vol

# Copy application code
COPY ./app /app

WORKDIR /app

# Set PATH
ENV PATH="/py/bin:$PATH"

# Change to app user
USER app

EXPOSE 8000

# Production command with Gunicorn
# Run collectstatic, migrations, then start server
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn --bind 0.0.0.0:8000 app.wsgi:application"]



