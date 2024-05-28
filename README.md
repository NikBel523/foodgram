## Бэкенд Foodgram

Представляет REST-сервис бэкенда для формирования рецептов. Включает регистрацию пользователей, простой профайл и безопасность доступа на основе стандартного токена. Позволяет идентифицированным пользователем:

- создавать и редактировать рецепты, привязанные к тегам;
- добавлять и удалять чужие рецепты в избранное;
- формировать из рецептов список покупок и скачивать его;
- подписываться на других пользователей.

Теги и ингредиенты добавляются и изменяются только пользователями с правами администратора. 

### Билд проекта

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
