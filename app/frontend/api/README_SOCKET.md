## Подключение к сокетам
Подключить к сокетам можно по url вида: `ws[wss]://<host>/ws/`

## Авторизация в сокетах
Авторизая производится посредством передачи валидного jwt в token в url. Пример:

## Как использовать события
Любой запрос будет иметь 1 обязательный параметр:
1. `event` — Название события, по которому необходимо получить ответ 

Любой ответ будет иметь 2 обязательных параметра: 
1. `event` — Название события, с которым связан ответ
2. `data` — Данные события

## Важное
1. Для работы обязательно должен быть создан диалог с ревьюером одним из способов:
    - `/api/dialogs/new-message/`
    - Через админку


```
wss://0.0.0.0:8000/ws/token?=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluQGFkbWluLmFkIiwiZXhwIjoxNjE5MTc3MzIwLCJlbWFpbCI6ImFkbWluQGFkbWluLmFkIiwib3JpZ19pYXQiOjE2MTkwOTA5MjB9.59BpaCPkUXpRy6Su-FoY39vCdOwW3pmLk12pHiNoQ5M
```

## Возможные события
1. `dialogs.load` — событие загружает все диалоги пользователя. Так же в каждом диалоге выводится последнее сообщение
    - Поддерживает `limit`
    - Поддерживает `offset`
    - Пример запроса:
    ```json
    {
       "event": "dialogs.load",
       "limit": 20,
       "offset": 40 
    }  
    ```
   - Пример ответа:
   ```json
   {
      "type": "ws_send",
      "data": [
        {
          "id": 8,  # id диалога
          "last_message": {
            "id": 29,  # id сообщения
            "user": {
              "email": "mat.coniaev2012@yandex.ru",
              "first_name": "a",
              "last_name": "b",
              "github_url": null,
              "avatar": "/static/default_avatar.jpg",
              "thumbnail_avatar": null,
              "email_notifications": false,
              "email_confirmed": false
            },
            "body": "first test",  # Сообщение в html
            "file": null,
            "date_created": "2021-04-22T17:24:02.807658+03:00",
            "date_read": null,
            "dialog": 8,
            "lesson": null
          }
        },
        {
          "id": 2,
          "last_message": {
            "user": {
              "first_name": "",
              "last_name": "",
              "github_url": "",
              "avatar": null,
              "email_notifications": false,
              "email_confirmed": false
            },
            "file": {
              "content": null
            },
            "date_read": null,
            "dialog": null,
            "lesson": null
          }
        }
      ]
    }
   ```
    
2. `dialogs.messages.load` — событие загружает сообщения по необходимому диалогу
    - Поддерживает `limit`
    - Поддерживает `offset`
    - Необходим параметр `dialog_id` в полезной нагрузке запроса
    - Пример запроса:
    ```json
    {
       "event": "dialogs.messages.load",
       "limit": 20,
       "offset": 40,
       "dialog_id": 1
    }  
    ```
     - Пример ответа:
   ```json
   {
      "type": "ws_send",
      "data": [
        {
          "id": 29,
          "user": {
            "email": "mat.coniaev2012@yandex.ru",
            "first_name": "a",
            "last_name": "b",
            "github_url": null,
            "avatar": "/static/default_avatar.jpg",
            "thumbnail_avatar": null,
            "email_notifications": false,
            "email_confirmed": false
          },
          "body": "first test",
          "file": null,
          "date_created": "2021-04-22T17:24:02.807658+03:00",
          "date_read": null,
          "dialog": 8,
          "lesson": null
        }
      ]
    }
   ```
    
3. `dialogs.messages.create` — событие создает сообщение в нужном диалоге. Так же событие дополнительно порождает событие `notifications.dialogs.count`. Так же в этот момент адресату отправляется сообщение на почту
    - Поддерживает присоединение файла в `file_id`
    - Тело сообщения поддерживает md 
    - Необходим параметр `dialog_id` в полезной нагрузке запроса
    - Пример запроса:
    ```json
    {
       "event": "dialogs.messages.create",
       "dialog_id": 1,
       "file_id": 1,
       "body": "yep"
    }  
    ```
    - Пример ответа:
   ```json
    {
      "type": "ws_send",
      "data": {
        "id": 34,
        "user": {
          "email": "mat.coniaev2012@yandex.ru",
          "first_name": "a",
          "last_name": "b",
          "github_url": null,
          "avatar": "/static/default_avatar.jpg",
          "thumbnail_avatar": null,
          "email_notifications": false,
          "email_confirmed": false
        },
        "body": "a",
        "file": {
          "id": 8,
          "date_created": "2021-04-19T17:47:56.538733+03:00",
          "content": "/media/2021/04/1/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA_%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0_2021-04-19_%D0%B2_12.24.53.png"
        },
        "date_created": "2021-04-22T19:23:58.794871+03:00",
        "date_read": null,
        "dialog": 8,
        "lesson": null
      }
    }
   ```
    
4. `dialogs.messages.seen` — событие делает сообщение прочитанным. Так же событие дополнительно порождает событие `notifications.dialogs.count`
    - Необходим параметр `dialog_id` в полезной нагрузке запроса
    - Необходим параметр `message_id` в полезной нагрузке запроса
    - Пример запроса:
    ```json
    {
       "event": "dialogs.messages.seen",
       "dialog_id": 1,
       "message_id": 1
    }  
    ```
    - Пример ответа:
   ```json
    {
      "type": "ws_send",
      "data": {
        "id": 31,
        "user": {
          "email": "admin@admin.ad",
          "first_name": "Ma",
          "last_name": "Ko",
          "github_url": null,
          "avatar": "/static/default_avatar.jpg",
          "thumbnail_avatar": null,
          "email_notifications": false,
          "email_confirmed": false
        },
        "body": "yep!",
        "file": null,
        "date_created": "2021-04-22T19:03:54.685450+03:00",
        "date_read": "2021-04-22T19:07:43.213623+03:00",
        "dialog": 8,
        "lesson": null
      }
    }
   ```
    
5. `notifications.dialogs.count` — событие содержит информацию о том, сколько диалогов с непрочитанными сообщениями есть у пользователя. Имеет смысл вызывать метод при загрузке страницы. Далее, это событие будет приходить когда необходимо.
    - Не требует никаких параметров
    - Пример запроса:
    ```json
    {
       "event": "notifications.dialogs.count"
    }  
    ```
   - Пример ответа:
   ```json
   {
      "type": "ws_send",
      "data": 1,
      "event": "notifications.dialogs.count"
    }
   ```
    

