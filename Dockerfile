FROM python:3.8.6-buster

WORKDIR /usr/src/msk_app

ADD ./requirements.txt ./
RUN pip install -r ./requirements.txt

COPY . /usr/src/msk_app/

CMD ["uwsgi", "app.ini"]
