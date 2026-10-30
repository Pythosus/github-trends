# GitHub Trends
ETL-пайплайн для анализа трендовых репозиториев GitHub и выявления популярных технологий. Собирает данные, обрабатывает их и раз в неделю формирует статистику по языкам, фреймворкам и инструментам.

## Описание

Проект решает задачу мониторинга IT-трендов:
- **Сбор (Extract)** — получение данных о трендовых репозиториях через GitHub REST API
- **Обработка (Transform)** — очистка, нормализация, извлечение технологий из `topics` и `readme`
- **Загрузка (Load)** — сохранение сырых данных в S3 и витрины в PostgreSQL
- **Оркестрация** — ежедневный и еженедельный запуск через Apache Airflow

**Стек:**
| Компонент | Технология |
|-----------|------------|
| Язык | Python 3.10+ |
| Оркестрация | Apache Airflow |
| Хранилище | PostgreSQL 15, S3 (MinIO) |
| Контейнеризация | Docker, Docker Compose |

## Структура проекта

```
.
├── dags/
│   └── main_etl_dag.py             # DAG Airflow
├── src/
│   ├── config.py                   # Подключение к S3 и PostreSQL
|   ├── get_trends.py               # Парсинг trending и сбор данных из GitHub API
│   ├── get_trends.py               # Очистка + поиск ключевых технологий
│   └── token.py                    # Токен GitHub
├── init_base/
│   └── create_tables.sql           # Инициализация схемы БД
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/Pythosus/github-trends.git
cd github-trends
```

### 2. Настройка GitHub-токена

> **Обязательный шаг!** Без токена API GitHub ограничивает запросы до 60 в час.

Скопируйте шаблон и впишите свой [Personal Access Token](https://github.com/settings/tokens):

```bash
cd src
cp token.example.py token.py
```

Отредактируйте `token.py`:

```python
token = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

> Файл `token.py` уже добавлен в `.gitignore` и **не попадёт** в репозиторий.

### 3. Запуск сервисов

```bash
docker-compose up -d --build
```

Будут подняты:
- **Airflow** (webserver + scheduler) — `http://localhost:8080`
- **PostgreSQL** — `localhost:5432`
- **MinIO (S3)** — `http://localhost:9001`

### 4. Подключение к Airflow

1. Откройте `http://localhost:8080`
2. Логин / пароль: `admin` / `admin`
3. Unpause DAG `main_data_trends_dag`

## Граф задач main_data_trends_dag

![Airflow DAG Graph main_data_trends_dag](images/graph.png)

Пайплайн состоит из 3 задач:

| Задача | Описание |
|--------|----------|
| `extract_info` | Запрос к GitHub API, получение JSON с трендовыми репо |
| `transform_info` | Очистка, извлечение ключевых технологий из readme |
| `load_trends` | Сохранение данных в БД |

Расписание: `@daily` (каждый день в 00:00 UTC).

## Схема базы данных

![Database Schema](images/bd.png)

Основные таблицы:

- **`repositories`** — информация о репозиториях
- **`keywords`** — справочник технологий по репозиториям
- **`top_tech`** — итоговый справочник данных

> SQL-скрипт инициализации находится в `init_base/create.sql` и выполняется автоматически при старте PostgreSQL.


## Конфигурация

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `GITHUB_TOKEN` | Personal Access Token | — (обязательно) |
| `POSTGRES_USER` | Пользователь БД | `postgre` |
| `POSTGRES_PASSWORD` | Пароль БД | `postgre` |
| `S3_ENDPOINT` | Endpoint MinIO | `http://minio:9000` |
| `S3_BUCKET` | Имя бакета | `bufer` |
