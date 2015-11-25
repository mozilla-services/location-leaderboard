FROM python:2.7
ENV PYTHONUNBUFFERED 1
EXPOSE 7001
WORKDIR /leaderboard
COPY . /leaderboard
RUN apt-get update && apt-get install -y binutils libproj-dev gdal-bin && apt-get -y clean 
RUN pip install -r requirements.txt --no-cache-dir --disable-pip-version-check
