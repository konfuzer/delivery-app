# ✅ Описание #

Проект Delivery App — это веб-приложение на основе Django и Django REST Framework, предназначенное для управления доставками.
Приложение позволяет:

Создавать, редактировать и удалять доставки
Отслеживать статистику по доставкам с фильтрацией по дате, типу доставки и типу груза
Просматривать данные о доставках через интерфейс админки и отчетной страницы

# 🧩 Возможности #
CRUD доставок - Полный доступ к управлению доставками через API и админку

Админка - Интерфейс с поддержкой всех моделей

Отчёты - Страница /reports/ показывает таблицу с полной информацией о доставках

Фильтры - Возможность фильтровать по дате, типу доставки и типу груза

График - Линейная диаграмма: количество доставок + среднее расстояние

Сортировка - Кликабельные заголовки таблицы для сортировки по возрастанию/убыванию

# 🛠 Технологии #
Django – основной бэкенд

DRF (Django REST Framework) – для работы с API

PostgreSQL – база данных

Chart.js – графики на странице отчетов

HTML/CSS/JS – клиентская часть без использования фреймворков

Docker – контейнеризация

Nginx – статические файлы и проксирование

JWT – авторизация

# 🚀 Установка и запуск #

- Клонируйте репозиторий 
```
git clone https://github.com/konfuzer/delivery-app.git
```
- Перейдите в папку с проектом, установите виртуальное окружение и зависимости
```
cd delivery-app/

python -m venv venv
source venv/Scraipts/activate (если используете bash)

pip install -r backend/requirements.txt
```

- Подготовьте .env файл:
Пример:

```
SECRET_KEY='your_key'
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
POSTGRES_DB=postgres_db
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=postgres_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

- Включите docker и запустите проект:

```
docker-compose up -d --build
```

- Примените миграции, создайти суперпользователя и соберите статику:

```
docker exec -it delivery-app-backend-1 python manage.py makemogrations
docker exec -it delivery-app-backend-1 python manage.py migrate

docker exec -it delivery-app-backend-1 python manage.py createsuperuser

docker exec -it delivery-app-backend-1 python manage.py collectstatic
```

Теперь проект доступен по адресу: 127.0.0.1/reports

Также можно загрузить тестовые данные:

```
docker exec -it delivery-app-backend-1 python deliveries/fill_test_data.py
```

Помимо данных, загрузятся три тестовых пользователя:
- testuser | testpass123 (superuser)
- Иван | 12345 
- sergey | sergey123

# 🔐 Авторизация #

Используется JWT-токен:

- Получение токена : POST /api/token/
- Обновление токена : POST /api/token/refresh/
Пример запроса:

```
curl -X POST http://localhost:8000/api/token/ \
-d "username=admin" \
-d "password=admin"
```

# 🌐 Доступные URL #
GET /reports/
- Страница отчёта с таблицей и графиком

GET /admin/
- Админка Django

GET /api/transports/
- API: список моделей транспорта

GET /api/packagings/
- API: список типов упаковки

GET /api/services/
- API: услуги доставки

GET /api/statuses/
- API: статусы доставки

GET /api/cargos/
- API: типы груза

GET /api/deliveries/
- API: список доставок

GET /api/reports/data/
- API: данные для отчёта

# 📊 Отчетная страница (/reports/) #
*Компоненты:*

Фильтры :
- По дате (start_date, end_date)
- По типу доставки (service)
- По типу груза (cargo)

Таблица :
- Итого | Дата | Модель ТС | Упаковка | Услуга | Статус | Груз | Расстояние (км) | Создал

График :

- Линия количества доставок
- Линия среднего расстояния

Все данные загружаются через /api/reports/data/ 

# 🎨 Админка #

- Полностью настроена
- Поддерживает все модели: TransportModel, PackagingType, DeliveryService, DeliveryStatus, CargoType, Delivery

# 📈 Графики #

*Работают на Chart.js:*

Тип графика : линейный (line)

Линии :
- Количество доставок
- Среднее расстояние

# 🔍 Сортировка #
*Все столбцы таблицы поддерживают клик для сортировки:*

- По возрастанию/убыванию
- Визуальные стрелочки на активном заголовке

# 📦 Фильтрация #

- По дате (start_date, end_date)
- По типу доставки (service)
- По типу груза (cargo)

# 🧪 Проверка работоспособности #

```
curl http://localhost:8000/api/reports/data/
```

Должен вернуть JSON с данными:

```
{
  "chart": {
    "labels": ["10.05.2025", ...],
    "total_count": [12, 14, ...],
    "avg_distance": [100.5, 120.0, ...]
  },
  "table": [
    {
      "id": 1,
      "delivery_date": "2025-05-10",
      "transport_model": "REX",
      "packaging": "Целофан",
      "service": "Хрупкий груз",
      "status": "В ожидании",
      "cargo_type": "Особые товары",
      "distance_km": 41.13,
      "created_by": "testuser"
    },
    ...
  ]
}
```

# 📦 Docker #

*Запущен через docker-compose.yml:*

- backend: Django + Gunicorn
- db: PostgreSQL
- nginx: раздача статики