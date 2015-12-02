FROM python:2.7
ENV PYTHONUNBUFFERED 1
WORKDIR /leaderboard
EXPOSE 80
EXPOSE 7001
RUN apt-get update && apt-get install -y binutils libproj-dev gdal-bin nginx && apt-get -y clean
COPY ./nginx/leaderboard /etc/nginx/sites-enabled/default
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf 
COPY ./requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir --disable-pip-version-check
COPY . /leaderboard
RUN mkdir /leaderboard/leaderboard/served/ && mkdir /leaderboard/leaderboard/served/static/ && python manage.py collectstatic -c --noinput
