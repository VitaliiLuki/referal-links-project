[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)

Проект для хранения реферальных ссылок пользователей.

## Запуск проекта через docker-compose

### Склонировать репозиторий на локальную машину:

```
git clone https://github.com/VitaliiLuki/referal-links-project

```
### Перейти в директорию с проектом

```
cd referal-links-project/
```

### Перейти в директорию infra и создать .env файл в директории infra/.env

```
cd infra/
```

```
touch .env
```

### Вписать переменные для БД Postgres и Secret_key django:

>DB_ENGINE=<django.db.backends.postgresql>

>DB_NAME=<имя базы данных postgres>

>DB_USER=<пользователь бд>

>DB_PASSWORD=<пароль>

>DB_HOST=<db_postgres>

>DB_PORT=<5432>

>SECRET_KEY=<секретный ключ проекта django>


### Выполнить развертывание контейнеров

```
docker-compose up -d
```

## API

 ### Документация API.
 
```http
   GET /redoc/
```

#### Запрос на получение кода авторизации.

```http
  POST /api/send_auth_code
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `phone_number` | `string` | **Required** |


#### Запрос на получение токена.

```http
  POST /api/check_phone_code
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `phone_number` | `string` | **Required** |
| `auth_code` | `string` | **Required** |

#### Запрос профиля пользователя.

```http
  GET api/users/me/
```
* Для авторизироанных пользователей

#### Запрос на активацию инвайт-кода другого пользователя.

```http
  GET api/users/me/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `invite_code` | `string` | **Required** |

* Для авторизироанных пользователей

#### Запрос списка пользователей.

```http
  GET api/users/
```

#### Запрос информации о конкретном пользователе.

```http
  GET api/users/<user_id>
```

