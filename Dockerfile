FROM python:3.8.3-alpine3.11

WORKDIR /usr/src/d_app

COPY . /usr/src/d_app/

RUN apk add python3-dev build-base linux-headers pcre-dev musl-dev postgresql-dev jpeg-dev zlib-dev \
    && pip install -r requirements.txt \
    && mkdir data

CMD ["uwsgi", "app.ini"]
