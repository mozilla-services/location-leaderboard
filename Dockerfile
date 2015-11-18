FROM python:2.7
ENV PYTHONUNBUFFERED 1
WORKDIR /leaderboard
EXPOSE 7001
ENTRYPOINT gunicorn -b 0.0.0.0:7001 leaderboard.wsgi
COPY . /leaderboard
RUN apt-get update && apt-get install -y binutils libproj-dev gdal-bin && apt-get -y clean 
RUN pip install -r requirements.txt --no-cache-dir --disable-pip-version-check
