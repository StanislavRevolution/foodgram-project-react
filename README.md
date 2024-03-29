# Проект "Продуктовый помощник"

Описание проекта
----------
Проект создан в рамках учебного курса Яндекс.Практикум.

Cайт Foodgram («Продуктовый помощник») создан для начинающих кулинаров и изысканныю гурманов. В сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Проект разворачивается в Docker контейнерах: backend-приложение API, postgresql-база данных, nginx-сервер и frontend-контейнер (используется только для сборки файлов и после запуска останавливается).

[Ссылка на размещенный проект на сервере Yandex.Cloud](http://yapiproject2.ddns.net)

Системные требования
----------
* Python 3.7+
* Docker
* Works on Linux, Windows, macOS, BSD

Стек технологий
----------
* Python 3.7
* Django 2.2.16
* Rest API
* PostgreSQL
* Nginx
* gunicorn
* Docker
* DockerHub
* JS

Установка проекта из репозитория (Linux и macOS)
----------

1. Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone git@github.com:StanislavRevolution/foodgram-project-react.git
```
2. Cоздать и открыть файл ```.env``` с переменными окружения:
```bash 
cd infra
touch .env
```
3. Заполнить ```.env``` файл с переменными окружения по примеру:
```bash 
echo DB_ENGINE=django.db.backends.postgresql >> .env
echo DB_NAME=postgres >> .env
echo POSTGRES_PASSWORD=postgres >> .env
echo POSTGRES_USER=postgres >> .env
echo DB_HOST=db >> .env
echo DB_PORT=5432 >> .env
```
4. Установка и запуск приложения в контейнерах (контейнер backend загружактся из DockerHub):
```bash 
docker-compose up -d
```

5. Запуск миграций, сбор статики и заполнение БД:
```bash 
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --no-input 
docker-compose exec web python manage.py recipes/management/commands/loaddemodata
```

### Логин и пароль от админки
- Login: admin
- Password: admin
### Автор
* Орловский Станислав