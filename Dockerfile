FROM python:2.7

ENV PYTHONUNBUFFERED 1

RUN apt-get update 
RUN apt-get install -y binutils libproj-dev gdal-bin

RUN mkdir /leaderboard

WORKDIR /leaderboard

ADD requirements.txt /leaderboard/

RUN pip install -r requirements.txt

ADD . /leaderboard/

CMD gunicorn -b 0.0.0.0:7001 leaderboard.wsgi
