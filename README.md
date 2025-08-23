# Alpina Bot Constructor

Django-приложение для создания и управления ботами на основе GPT API и Telegram.

## Возможности

- Создание и управление ботами через административный интерфейс
- Настройка сценариев взаимодействия с пользователями
- Интеграция с OpenAI GPT для генерации ответов
- Интеграция с Telegram для обмена сообщениями
- REST API для управления ботами, сценариями и шагами

## Технологии

- Python 3.8+
- Django 3.2
- Django REST Framework
- OpenAI API
- Telegram Bot API

## Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/andreika2095/alpina-bot-constructor.git
cd alpina-bot-constructor
2. Создание виртуального окружения
bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
3. Установка зависимостей
bash
pip install -r requirements.txt
4. Настройка переменных окружения
Создайте файл .env в корне проекта:

ini
DEBUG=True
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key-here
DATABASE_URL=sqlite:///db.sqlite3
Для генерации секретного ключа выполните:

bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
5. Применение миграций
bash
python manage.py migrate
6. Создание суперпользователя
bash
python manage.py createsuperuser
7. Загрузка тестовых данных (опционально)
bash
python manage.py create_test_data
8. Запуск сервера
bash
python manage.py runserver
После этого приложение будет доступно по адресу: http://localhost:8000

Использование
Административный интерфейс
Доступен по адресу: http://localhost:8000/admin

Здесь вы можете:

Создавать и управлять ботами

Настраивать сценарии и шаги

Просматривать сессии пользователей

REST API
Доступны следующие endpoints:

GET /api/bots/ - список ботов

POST /api/bots/ - создание бота

GET /api/bots/{id}/ - детали бота

PUT /api/bots/{id}/ - обновление бота

DELETE /api/bots/{id}/ - удаление бота

GET /api/scenarios/ - список сценариев

POST /api/scenarios/ - создание сценария

GET /api/scenarios/{id}/ - детали сценария

PUT /api/scenarios/{id}/ - обновление сценария

DELETE /api/scenarios/{id}/ - удаление сценария

GET /api/steps/ - список шагов

POST /api/steps/ - создание шага

GET /api/steps/{id}/ - детали шага

PUT /api/steps/{id}/ - обновление шага

DELETE /api/steps/{id}/ - удаление шага

Интеграция с Telegram
Создайте бота через @BotFather и получите токен.

Добавьте бота в административном интерфейсе, указав полученный токен.

Установите вебхук для бота (замените YOUR_DOMAIN на ваш домен и BOT_ID на ID бота в системе):

bash
python manage.py set_webhook --bot-id BOT_ID
Для локальной разработки можно использовать ngrok для создания публичного URL.

Интеграция с OpenAI GPT
Получите API ключ на OpenAI Platform.

Укажите его в переменной окружения OPENAI_API_KEY.

Разработка
Структура проекта
text
alpina-bot-constructor/
├── bot_constructor/          # Настройки Django проекта
├── bots/                     # Приложение для управления ботами
│   ├── management/commands/  # Пользовательские команды
│   ├── migrations/           # Миграции базы данных
│   ├── models.py             # Модели данных
│   ├── serializers.py        # Сериализаторы для API
│   ├── services.py           # Логика работы с GPT API
│   ├── signals.py            # Сигналы Django
│   ├── telegram_handler.py   # Обработчик Telegram сообщений
│   ├── urls.py               # Маршруты API
│   └── views.py              # Представления API
├── .env.example              # Пример файла с переменными окружения
├── .gitignore               # Файлы, игнорируемые Git
├── requirements.in          # Список зависимостей (входной файл)
├── requirements.txt         # Зафиксированные зависимости
└── manage.py               # Утилита управления Django
Добавление новых функциональностей
Модели: редактируйте bots/models.py

API: добавляйте endpoints в bots/urls.py, представления в bots/views.py и сериализаторы в bots/serializers.py

Логика работы с внешними API: добавляйте в bots/services.py

Обработчики для мессенджеров: добавляйте в bots/telegram_handler.py или создавайте новые файлы

Тестирование
Для запуска тестов выполните:

bash
python manage.py test
Вклад в проект
Форкните репозиторий

Создайте ветку для новой функциональности (git checkout -b feature/amazing-feature)

Закоммитьте изменения (git commit -m 'Add some amazing feature')

Запушьте ветку (git push origin feature/amazing-feature)

Откройте Pull Request