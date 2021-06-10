# Course-Platform

## Materials
[Surge.sh demo](https://ytyt.surge.sh/)
[Figma](https://www.figma.com/file/ufNp4pKYlap6G7AEH2rRl6/YtYt)
[Swagger Hub](https://ytyt.ru/swagger/)

## Frontend
Based on [Nuxt.js](https://nuxtjs.org).

```bash
# install dependencies
$ yarn install

# serve with hot reload at localhost:3000
$ yarn dev

# build for production and launch server
$ yarn build
$ yarn start

# generate static project
$ yarn generate
```


# Магические команды в редакторе
Редактор в django-admin поддерживает магические команды по аналогии с Jupyter Notebook.
Команды после рендеринга будут удалены, а лишние пробелмы убраны. 

## Быстрый старт
Пользоваться командами просто — достаточно указать их в начале файла

```md
%default_language=python

%brython_snippets=true

# Это наш первый урок
...

```

## Правила объявления команд
1. Каждая команда должна быть отделена одной строкой:
    - Правильно:
    ```md
    %default_language=python

    %brython_snippets=true
    
    ...
    ```
    
    - Неправильно:
    ```md
    %default_language=python
    %brython_snippets=true

    ...
    ```

    - Неправильно:
    ```md
    %default_language=python
    ...
    ```

2. Каждая команда должна начинаться с префикса `%`:
    - Правильно:
    ```md
    %default_language=python

    ...
    ```
    
    - Неправильно:
    ```md
    &default_language=python

    ...
    ```


## Список команд команды 

| Команда              | Описание                                                                                 | Параметры      |
| -------------------- |------------------------------------------------------------------------------------------|:--------------:|
| default_language     | Устанавливает значение языка блока с кодом по умолчанию. Включается, если не указан ЯП   |  Любая строка  | 
| brython_snippets     | Все блоки кода из Jupyter Notebook будут переведены в исполняемые на фронте сниппеты     |  true         |


##  Дополнение


### Условия исполнения команд
Каждая из команд сначала берется из урока и переносится на каждый фрагмент урока. 
Существует возможность настроить магические команды в рамках одного фрагмента, которые будут обработаны индивидуально


### Объявление исполняемого brython-сниппета
Объявить исполняемый сниппет можно как из файла `.ipynb`, так и из редактора непосредственно

Обычный код, который не будет инициализирован как сниппет:
````md

```python
print('hello world')
```

````

Код, который будет инициализирован как сниппет:
````md

```brython-snippet
print('hello world')
```

````

Далее, во время рендеринга будут обнаружены все сниппеты и выведены на в необходимом шаблоне