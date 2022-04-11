# API для Yatube
## Проект 9-го спринта (блок API)

### Описание
API для платформы Yatube. Version 1.

### Установка
Клонировать репозиторий и перейти в него в командной строке:

```git clone https://github.com/tanja-ovc/api_final_yatube.git```

Убедиться, что находитесь в директории _api_final_yatube_.

Cоздать и активировать виртуальное окружение:

```python3 -m venv env```

```source env/bin/activate```

При необходимости обновить pip:

```python3 -m pip install --upgrade pip```

Установить зависимости из файла requirements.txt:

```pip install -r requirements.txt```

Выполнить миграции:

```python3 manage.py migrate```

Запустить проект:

```python3 manage.py runserver```

### Примеры запросов к API
Просмотр списка постов сайта (доступно всем):


```GET``` ```http://127.0.0.1:8000/api/v1/posts/```

Создание нового поста (доступно аутентифицированным пользователям):

```POST``` ```http://127.0.0.1:8000/api/v1/posts/```

Просмотр отдельного поста (доступно всем):

```GET``` ```http://127.0.0.1:8000/api/v1/posts/1/```

Изменение/удаление отдельного поста (доступно только автору поста):

```PATCH/PUT/DELETE``` ```http://127.0.0.1:8000/api/v1/posts/1/```

Просмотр списка комментариев к отдельному посту (доступно всем):

```GET``` ```http://127.0.0.1:8000/api/v1/posts/1/comments/```

...

Просмотр подписок текущего пользователя (доступно аутентифицированным пользователям):

```GET``` ```http://127.0.0.1:8000/api/v1/follow/```

Подписка (доступно аутентифицированным пользователям): 

```POST``` ```http://127.0.0.1:8000/api/v1/follow/```


### Автор
_Таня Овчинникова_
