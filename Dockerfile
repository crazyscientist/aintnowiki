FROM python:3
ENV PYTHONUNBUFFERED=1
ENV MEDIA_ROOT=/data/media/
ENV STATIC_ROOT=/data/static/
COPY ./ /code

RUN adduser -q anw; \
    mkdir -p /data; \
    chown anw /data; \
    chmod 770 /data; \
    pip install -r /code/requirements.txt gunicorn psycopg2-binary; \
    cd /code; \
    python setup.py install; \
    manage.py collectstatic --noinput
USER anw
