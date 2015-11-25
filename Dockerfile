FROM python:2.7
ENV PYTHONUNBUFFERED 1
WORKDIR /leaderboard
EXPOSE 7001
RUN apt-get update && apt-get install -y binutils libproj-dev gdal-bin && apt-get -y clean 
COPY ./requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir --disable-pip-version-check
COPY . /leaderboard
