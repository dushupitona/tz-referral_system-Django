# Тестовое задание 'Реферальная система' #

> ## Запуск проекта ##
> 1. Склонируйте проект
> 2. Перейдите в директорию проекта
> 3. Запустите команду ``` docker-compose up --build```
> 4. Перейдите по адресу http://localhost:8000

> ## Админка Django ##
> Пользователь создается автоматически:
> - login: admin
> - password: admin

> ## Функционал ##
> ### Вход в профиль: ###
> 1. Введите номер телефона ```79.........```
> 2. Введите код из консоли
> - Если код запрошен повторно (предыдущий запрос был меньше 10 мин назад), то необходимо ввести код из прошлого запроса
> 
> ### Ввести реферальный код: ###
> 1. Введите инвайт код в необходимое поле
> - Если код уже введен - поле станет недоступным

> ## API ##
> ### (В проекте есть коллекция для Postman)  ###
> ### Получить данные профиля  ###
> 1. Получить код аутентификации
> > ***Запрос***
> > - POST по адресу ```127.0.0.1:8000/api/send_code/```
> > - Тело запроса:
> > ```{"phone_number": "79000000000"}```
>
> > ***Ответ:***
> > ```
> > {
> > "response": "CODE SENDED",
> >     "user":
> >         {"phone_number": "79000000000"}
> > }
> > ```
> >
> 2. Ввести код аутентификации
> > ***Запрос***
> > - POST по адресу ```127.0.0.1:8000/api/auth/```
> > - Тело запроса:
> > ```
> > {
> > "phone_number": "79000000000",
> > "auth_code": "7670"
> >  }
> > ```
>
> > ***Ответ***
> > ```
> > {
> > "response": "SUCCESS",
> > "token": "b175eb3ba6b5a72f77c6e34b64bd145c1286ef7c"
> > }
> > ```
> >
> 3. Получить данные профиля
> > ***Запрос***
> > - GET по адресу ```127.0.0.1:8000/api/profile/```
> > - Заголовок:
> > ```
> > Key: Authorization
> > Value: Token b175eb3ba6b5a72f77c6e34b64bd145c1286ef7c
> > ```
>
> > ***Ответ***
> > ```
> > {
> >     "user": "79000000000",
> >     "referral_code": "HEQPR8",
> >     "invite_code": "Инвайт код не введен",
> >     "invited_users": []
> > }
> > ```
> 
> ### Ввести инвайт код  ###
> > ***Запрос***
> > - POST по адресу ```127.0.0.1:8000/api/profile/invite_code/```
> > - Заголовок:
> > ```
> > Key: Authorization
> > Value: Token b175eb3ba6b5a72f77c6e34b64bd145c1286ef7c
> > ```
> > 
> > - Тело запроса:
> > ```
> > {
> >     "referral_code": "866S6N"
> > }
> > ```
>
> > ***Ответ:***
> > ```
> > {
> >   'response': 'SUCCESS'
> > }
> > ```
>
> ### Список всех телефонов (для SUPERUSER)  ###
> > ***Запрос***
> > - GET по адресу ```127.0.0.1:8000/api/profiles/```
> > - Заголовок:
> > ```
> > Key: Authorization
> > Value: Token <необходимо получить токен для "phone_number": "admin">
> > ```
>
> > ***Ответ:***
> > ```
> > [
> >     {
> >         "id": 4,
> >         "phone_number": "+79000000001"
> >     },
> >     {
> >         "id": 5,
> >         "phone_number": "+79000000000"
> >     },
> >     {
> >         "id": 3,
> >         "phone_number": "79000000000"
> >     },
> >     {
> >         "id": 2,
> >         "phone_number": "admin"
> >     }
> > ]
> > ```

> ## Celery workers ##
> > 1. Генератор ключей аутентификации
> > - Воркер по запросу пользователя генерирует ключ и выводит его в консоль с дополнительной задержкой в 2 сек.
>
> > 2. Уборщик мусора
> > - Уборщик с периодичностью в минуту проверяет базы данных на наличие устаревших ключей и неактивных профилей (профили, которые ни разу не вводили код аутентификации) и удаляет их.
