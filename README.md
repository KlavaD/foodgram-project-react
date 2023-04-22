![test](https://github.com/KlavaD/foodgram-project-react/actions/workflows/foodgram-project-react_workflow.yml/badge.svg)
# Мой дипломный проект — сайт Foodgram, «Продуктовый помощник». 
## На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

http://klavayamdb.sytes.net/admin/ 

Проект создавала я - 
* ### Клавдия Дунаева


**Вот, что было сделано в ходе работы над проектом:**
* настроено взаимодействие Python-приложения с внешними API-сервисами;
* создан собственный API-сервис на базе проекта Django;
* создан Telegram-бот;
* подключено SPA к бэкенду на Django через API;
* созданы образы и запущены контейнеры Docker;
* созданы, развёрнуты и запущены на сервере мультиконтейнерные приложения;
* закреплены на практике основы DevOps, включая CI&CD.

**Инструменты и стек:**

Python, JSON, YAML, Django, React, Telegram, API, Docker, Nginx, PostgreSQL, Gunicorn, Postman

**Как запустить проект:**

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/KlavaD/foodgram-project-react.git
```

**Описание команд для запуска приложения в контейнерах**

Создайте файл .env с переменными окружения:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=< имя базы данных>
POSTGRES_USER=<логин для подключения к базе данных>
POSTGRES_PASSWORD=<пароль для подключения к БД (установите свой)>
DB_HOST=< название сервиса (контейнера)>
DB_PORT=5432 # порт для подключения к БД 
```
Запустите контейнер из папки infra/
```
docker-compose up -d --build
```

Выполните следующие команды:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```
Сделать импорт из csv файлов:

```
docker-compose exec web python manage.py adddata
```


## Примеры запросов: ##
Регистрация нового пользователя:
>**POST** http://127.0.0.1/api/users/

Для получения токена отправьте логин и код, который пришел вам на электронную почту:
>**POST** http://127.0.0.1/api/auth/token/login/

```
{
"password": "string",
"email": "string"
}
```

Получение списка рецептов:
>**GET** .../api/recipes/

Создание рецепта (только зарегистрированный пользователь):
>**POST** .../api/recipes/
> 
```
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```

Получение списка покупок:
>**GET** .../api/recipes/download_shopping_cart/

Получение списка тэгов:
>**GET** .../api/tags/

Просмотр подписок:
>**GET** .../api/v1/titles/{title_id}/reviews/

Подписаться на пользователя:
>**POST** .../api/users/{id}/subscribe/

Остальные запросы можно посмотреть в документации для Foodgram:
> .../api/docs/

