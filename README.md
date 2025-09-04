# Restaurant Order Management System

Система управления заказами для ресторана с функциями реального времени и микросервисной архитектурой.

## Особенности системы

- 🚀 Realtime обновления через WebSocket
- 📊 Статистика заказов в реальном времени
- 🔄 Управление статусами заказов
- 🛡️ Разделение прав доступа (клиенты/персонал)
- 📱 Адаптивный интерфейс
- 🔍 Фильтрация заказов по статусу
- 🏗️ Микросервисная архитектура

## Технологический стек

### Frontend
- React
- TypeScript
- WebSocket для real-time обновлений
- Axios для HTTP запросов
- React Router для навигации

### Backend
- FastAPI (Python)
- MongoDB
- WebSocket для real-time коммуникации
- Docker и Docker Compose для контейнеризации

## Архитектура системы

### Frontend Architecture
```
frontend/
├── src/
│   ├── components/      # React компоненты
│   ├── services/        # API и WebSocket сервисы
│   ├── types/          # TypeScript типы
│   └── pages/          # Страницы приложения
```

### Backend Architecture
```
backend/
├── app/
│   ├── apis/           # API endpoints
│   ├── services/       # Бизнес логика
│   ├── models/         # Модели данных
│   ├── dto/            # Data Transfer Objects
│   ├── websocket/      # WebSocket handlers
│   └── dependencies.py # Dependency injection
```

## Запуск проекта

### Предварительные требования
- Docker и Docker Compose
- Node.js 16+ (для разработки)
- Python 3.8+ (для разработки)

### Шаги по запуску

1. Клонировать репозиторий:
\`\`\`bash
git clone <repository-url>
cd order
\`\`\`

2. Запустить backend сервисы:
\`\`\`bash
docker-compose up -d
\`\`\`

3. Установить зависимости и запустить frontend:
\`\`\`bash
cd frontend
npm install
npm start
\`\`\`

Приложение будет доступно по адресу: http://localhost:3000

## API Endpoints

### Products API
- \`GET /products/\` - Получение списка продуктов
- \`POST /products/\` - Создание нового продукта (для админов)

### Orders API
- \`GET /orders/\` - Получение списков заказов
- \`POST /orders/\` - Создание нового заказа
- \`PATCH /orders/{id}\` - Обновление статуса заказа
- \`GET /orders/statistics/overview\` - Получение статистики по заказам

## WebSocket Events

### Подключение
\`\`\`typescript
ws://localhost:8000/ws/{role}  // role: customers, staff, admin
\`\`\`

### События
- \`ORDER_CREATED\` - Создан новый заказ
- \`ORDER_UPDATED\` - Обновлен статус заказа
- \`STATS_UPDATED\` - Обновлена статистика

## Statuses Flow

Последовательность статусов заказа:
1. NEW (новый) → CONFIRMED (подтвержден)
2. CONFIRMED → PREPARING (готовится)
3. PREPARING → READY (готов)
4. READY → COMPLETED (выполнен)

* CANCELLED (отменен) - доступен из любого статуса кроме COMPLETED

## Разработка

### Backend Development
\`\`\`bash
cd backend
python -m venv .venv
source .venv/bin/activate  # или .venv\\Scripts\\activate на Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
\`\`\`

### Frontend Development
\`\`\`bash
cd frontend
npm install
npm start
\`\`\`

## Логирование

Логи сохраняются в директории \`logs/\`:
- \`app.log\` - общие логи приложения
- \`errors.log\` - логи ошибок

## Docker конфигурация

Проект использует Docker Compose для оркестрации следующих сервисов:
- MongoDB (порт 27017)
- Backend API (порт 8000)

## Безопасность

- WebSocket подключения разделены по ролям
- Валидация данных на бэкенде
- Обработка ошибок на всех уровнях
- Безопасное хранение данных в MongoDB

## Мониторинг

- Healthcheck для API сервиса
- Логирование всех важных событий

## License

MIT License
