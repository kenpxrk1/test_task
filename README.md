# Тестовое задание для VK - Ботоферма

### Требования: 

Написать Restful-сервис на Python с использованием FastAPI в качестве веб-фреймворка, SQLAlcheymy в качестве ORM,
который бы создавал нового пользователя в ботоферме, выдавал список всех существующих пользователей, а также блокировал
пользователя для его использования в рамках E2E-теста.


## Стек:

![FastAPI](https://img.shields.io/badge/FastAPI-0.110.2-cyan?style=flat&logo=FastAPI&logoColor=cyan)
![Python](https://img.shields.io/badge/Python-3.10-brightgreen?style=flat&logo=Python&logoColor=brightgreen)
![SqlAlchemy](https://img.shields.io/badge/SqlAlchemy-2.0.20-brightgreen?style=flat&logo=python&logoColor=brightgreen)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15.5-blue?style=flat&logo=postgresql&logoColor=blue)
![Docker](https://img.shields.io/badge/Docker_compose-grey?style=flat&logo=docker&logoColor=blue)

## Зависимости: 

- docker 

- docker-compose


## Инструкция по установке и запуску приложения: 

Клонируйте репозиторий:
```sh
$ git clone https://github.com/kenpxrk1/quiz-task-api
```

Запустите приложение из корневой папки с помощью docker-compose:

```sh
$ docker-compose docker_compose_app up 
```

```sh
$ docker-compose docker_compose_tests up 
```


### После установки и запуска, приложение станет доступно по адресу: 

`http://127.0.0.1:9999/docs`

