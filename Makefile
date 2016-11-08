build:
	docker build -t app:build .

up: build
	docker run --net=host -i -t app:build python manage.py runserver 0:7001

test: build
	docker run --net=host -i -t app:build python manage.py test
