# To-Do Telegram Bot

Этот проект представляет собой Telegram-бота для управления списком задач. Бот позволяет пользователю добавлять задачи на выбранные даты, просматривать задачи на определенную дату или за месяц, а также добавлять случайные задачи. Задачи сохраняются в формате JSON, что позволяет боту сохранять данные между сессиями.
За основу проекта был взят курс [Основы Python: создаём телеграм-бота](https://netology.ru/) от Нетологии.
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
```
### 2. Загрузка задач в JSON
Когда бот запускается, он загружает сохраненные задачи из файла todos.json. Если файл отсутствует, то задачи не загружаются и создается новый пустой словарь.

**Функция:** `load_todos()`

**Описание:** Загружает задачи из файла при старте бота.

Пример кода:
```python
def load_todos():
    global todos
    try:
        with open('todos.json', 'r', encoding='utf-8') as file:
            todos = json.load(file)
    except FileNotFoundError:
        todos = {}
```
### 3. Добавление задачи
**Функция:** add_todo(date, task)

**Описание:** Добавляет задачу на указанную дату. Если задачи на эту дату уже существуют, она добавляется в список для этой даты. В противном случае создается новый список задач.
Пример кода:
```python
def add_todo(date, task):
    if date in todos:
        todos[date].append(task)
    else:
        todos[date] = [task]
    save_todos()
```
### 4. Интерактивный календарь
Бот использует календарь, который позволяет пользователю выбрать дату для добавления задачи или просмотра задач. Для навигации по месяцам можно перемещаться вперед или назад.

**Функция:** create_calendar(year, month, action)

**Описание:** Генерирует интерактивный календарь с кнопками для дней месяца и навигационными кнопками для выбора месяца.
Пример кода:
```python
def create_calendar(year=None, month=None, action="show"):
    now = datetime.now()
    year = year or now.year
    month = month or now.month
    keyboard = InlineKeyboardMarkup()
    
    # Навигация по месяцам
    keyboard.row(
        InlineKeyboardButton("<", callback_data=f"prev_month|{year}|{month}"),
        InlineKeyboardButton(f"{year}-{month:02d}", callback_data="ignore"),
        InlineKeyboardButton(">", callback_data=f"next_month|{year}|{month}")
    )
    
    # Дни недели
    days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    keyboard.row(*[InlineKeyboardButton(day, callback_data="ignore") for day in days])
    
    # Дни месяца
    first_day = datetime(year, month, 1)
    last_day = (first_day + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    day_buttons = []
    for day in range(1, last_day.day + 1):
        day_buttons.append(InlineKeyboardButton(f"{day}", callback_data=f"select_date_{action}|{year}-{month:02d}-{day:02d}"))
    
    # Пустые кнопки для заполения пространства
    for _ in range(first_day.weekday()):
        day_buttons.insert(0, InlineKeyboardButton(" ", callback_data="ignore"))
    
    while day_buttons:
        keyboard.row(*day_buttons[:7])
        day_buttons = day_buttons[7:]
    
    return keyboard
```
### 5. Обработка команд и кнопок

** Команда**  /start: 
Отправляет приветственное сообщение и главное меню с кнопками для выбора действия.
** Обработка Inline кнопок:**  
В зависимости от выбранной кнопки, бот вызывает соответствующие функции, такие как показ задач, добавление задачи или выбор даты.

**Пример обработки команды:** 
```python
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я бот для управления списком задач. Выберите действие:",
        reply_markup=create_main_menu()
    )
```    

________________________________________
### Логгирование и ошибки
Для логгирования ошибок можно использовать стандартную библиотеку logging. Вы можете добавить в программу базовую настройку логгирования, чтобы отслеживать события бота.

Пример настройки логирования:
```python

import logging
logging.basicConfig(level=logging.INFO)

# Пример записи логов
logging.info('Задача была успешно добавлена.')
```
________________________________________

### Как запустить бота
**1.	Установка зависимостей:** Убедитесь, что у вас установлены все необходимые библиотеки:
```bash
pip install pyTelegramBotAPI
```
**2.	Настройка токена:** Замените токен бота в коде на ваш собственный. Вы можете получить токен, создав бота через BotFather.
**3.	Запуск: Запустите файл с кодом:**
```bash
python bot.py
```
**4.	Использование:**

***o	Нажмите на кнопку "Показать задачи" для отображения задач на определенную дату.***

***o	Используйте "Добавить задачу" для ввода задач.***

***o	Воспользуйтесь "Случайной задачей", чтобы добавить случайную задачу.***
________________________________________
###Заключение
Этот проект демонстрирует создание функционального Telegram-бота для управления задачами. Бот предлагает удобный интерфейс для добавления, удаления и отображения задач с помощью inline-кнопок и календаря.
