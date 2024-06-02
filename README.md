## Бэкенд Foodgram

Представляет REST-сервис бэкенда для формирования рецептов. Включает регистрацию пользователей, простой профайл и безопасность доступа на основе стандартного токена. Позволяет идентифицированным пользователем:

- создавать и редактировать рецепты, привязанные к тегам;
- добавлять и удалять чужие рецепты в избранное;
- формировать из рецептов список покупок и скачивать его;
- подписываться на других пользователей.

Теги и ингредиенты добавляются и изменяются только пользователями с правами администратора. 

### Деплой Foodgram

Деплой на сервер происходит в несколько этапов.

1. В отдельную дерикторию необходимо поместить docker-compose.production.yml и .env. С примером заполнения .env можно ознакомится в .env.example.

2. Настроить внешний Nginx. 

    ` sudo nano /etc/nginx/sites-enabled/default`

    Добавить туда доменное имя и указать порты.

3. В выбранной дериктории запускаеся файл docker-compose.production.yml:

    `sudo docker compose -f docker-compose.production.yml up`

4. Сбор статистики и проведение миграций происходят автоматически на этапе сборки контейнера backend.

5. После запуска приложения, можно воспользоваться командами создания первоначальных объектов внутри контейнера backend.

    `sudo docker compose -f docker-compose.production.yml exec backend python manage.py auto_create_superuser` создаст суперюзера c атрибутами указанными в .env

    `sudo docker compose -f docker-compose.production.yml exec backend python manage.py create_basic_tags` создаст первые теги для рецептов (Завтрак, Обед, Ужин)

    `sudo docker compose -f docker-compose.production.yml exec backend python manage.py load_ingredients` загружает обширную коллекцию ингредиентов в базу даных



### Развертывание бэкенда локально

1. Взятие исходников из репозитория:

    `git clone git@github.com:NikBel523/foodgram.git` или

    `git clone https://github.com/NikBel523/foodgram.git`.

2. Перехдим в корень проекта:

    `cd foodgram`.

3. Создаём виртуальное окружение:

      **Важно!** Должен быть установлен Python 3.9.
      `python -m venv venv` для Windows
      `python3 -m venv venv` для Linux или MacOS

4. Активируем созданное виртуальное окружение:

    Windows: `source venv/Scripts/activate`;

    Linux: `source env/bin/activate`.

5. Опциально обновляем pip:

    `python -m pip install --upgrade pip`.

6. Ставим зависимости:

    `cd ./backend/foodgram_project/`;

    `pip install -r requirements.txt`.

7. Накатываем миграции:

    `python manage.py migrate`.

8. Добавляем супер-пользователя.

    - с данными ручным вводом `python manage.py createsuperuser`
    - с автоматическими или данными из .env `python manage.py auto_create_superuser`

9. Стартуем сервис:

    `python manage.py runserver`.

### Swagger для Api

После запуска сервиса доступен на: [Swagger](http://127.0.0.1:8080/redoc/).


## Стек технологий backend
- Python
- Django
- Django REST Framework
- PostgreSQL
- Nginx
- gunicorn
- Docker

Автор: [Беляков Никита](https://github.com/NikBel523)