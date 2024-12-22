# To-Do Telegram Bot

Этот проект представляет собой Telegram-бота для управления списком задач. Бот позволяет пользователю добавлять задачи на выбранные даты, просматривать задачи на определенную дату или за месяц, а также добавлять случайные задачи. Задачи сохраняются в формате JSON, что позволяет боту сохранять данные между сессиями.

## Возможности бота

- **Показать задачи за определенную дату** — пользователь может выбрать дату и увидеть все задачи, назначенные на этот день.
- **Добавить задачу на выбранную дату** — бот предложит выбрать дату и ввести задачу, которую нужно добавить в список задач на эту дату.
- **Случайная задача** — бот предложит случайную задачу из предустановленного списка.
- **Интерактивный календарь** — календарь позволяет легко выбирать даты для добавления задач или их просмотра.
- **Сохранение задач в JSON-файл** — задачи сохраняются в файл `todos.json`, чтобы данные не терялись при перезапуске бота.

## Структура проекта

- `telebot` — библиотека для работы с Telegram API.
- `random` — используется для генерации случайных задач.
- `datetime` — используется для работы с датами и временем.
- `json` — для работы с JSON-файлами, в которых сохраняются задачи.
- `InlineKeyboardMarkup` и `InlineKeyboardButton` — для создания интерактивных кнопок в Telegram.

## Как работает бот

### 1. Сохранение задач в JSON

Задачи сохраняются в файле `todos.json` в формате JSON. Каждая задача привязана к определенной дате, которая используется как ключ в словаре.

**Функция:** `save_todos()`  
**Описание:** Сохраняет словарь с задачами в JSON-файл для долговременного хранения.

Пример кода:
```python
def save_todos():
    with open('todos.json', 'w', encoding='utf-8') as file:
        json.dump(todos, file, ensure_ascii=False, indent=4)
```python
### 2. Загрузка задач из JSON
