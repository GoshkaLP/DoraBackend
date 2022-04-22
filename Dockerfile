FROM python:3.8.3-alpine3.11

WORKDIR /usr/src/app

COPY ./ ./

RUN apk add python3-dev build-base linux-headers pcre-dev musl-dev postgresql-dev jpeg-dev zlib-dev \
    && pip install -r requirements.txt

CMD ["uwsgi", "app.ini"]