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
1. `dialogs.load` — событие загружает все диалоги пользователя
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
       "body": "#Hello"
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
   - Структура ответа:
   ```json
   {
       "event": "dialogs.messages.seen",
       "user": 
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
   {"type": "ws_send", "data": 1, "event": "notifications.dialogs.count"}
   ```
    

