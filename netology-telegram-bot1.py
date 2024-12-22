# to-do list - программа для ведения списка дел

import telebot
from random import choice
from datetime import datetime, timedelta
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Токен бота
token = '7769145923:AAEA5JHOeuWcwIvUr-shE6l3lgqmQ4_mero'
bot = telebot.TeleBot(token)

# Случайные задачи
RANDOM_TASKS = [
    'Написать Гвидо письмо',
    'Выучить Python',
    'Записаться на курс в Нетологию',
    'Посмотреть 4 сезон Рик и Морти'
]

# Хранилище задач
todos = {}

# Текст помощи
HELP = '''
Выберете действие с помошью предложенных кнопок в интерфейсе телерам-бота
Показать задачи - вывод задач за определенную дату
Добавить задачу - добавление задач на копределенную дату
Случайная задача - пример работы бота
'''

# Сохранение задач в файл
def save_todos():
    with open('todos.json', 'w', encoding='utf-8') as file:
        json.dump(todos, file, ensure_ascii=False, indent=4)

# Загрузка задач из файла
def load_todos():
    global todos
    try:
        with open('todos.json', 'r', encoding='utf-8') as file:
            todos = json.load(file)
    except FileNotFoundError:
        todos = {}

# Функция добавления задачи
def add_todo(date, task):
    if date in todos:
        todos[date].append(task)
    else:
        todos[date] = [task]
    save_todos()

# Создание основного меню кнопок
def create_main_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Показать задачи", callback_data='show'))
    keyboard.add(InlineKeyboardButton("Добавить задачу", callback_data='add'))
    keyboard.add(InlineKeyboardButton("Случайная задача", callback_data='random'))
    keyboard.add(InlineKeyboardButton("Помощь", callback_data='help'))
    return keyboard

# Создание календаря для выбора даты
def create_calendar(year=None, month=None, action="show"):
    now = datetime.now()
    year = year or now.year
    month = month or now.month
    keyboard = InlineKeyboardMarkup()

    # Название месяца и навигация
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
        # Добавлено разделение callback'ов для показа и добавления задач
        day_buttons.append(InlineKeyboardButton(f"{day}", callback_data=f"select_date_{action}|{year}-{month:02d}-{day:02d}"))

    # Пустые кнопки для заполнения начального пространства
    for _ in range(first_day.weekday()):
        day_buttons.insert(0, InlineKeyboardButton(" ", callback_data="ignore"))

    # Разбить на строки
    while day_buttons:
        keyboard.row(*day_buttons[:7])
        day_buttons = day_buttons[7:]

    return keyboard

# Команда /start
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я бот для управления списком задач. Выберите действие:",
        reply_markup=create_main_menu()
    )

# Обработка Inline кнопок
@bot.callback_query_handler(func=lambda call: True)
def inline_button_callback(call):
    if call.data == 'show':
        bot.send_message(call.message.chat.id, "Выберите дату для отображения задач:", reply_markup=create_calendar(action="show"))
    elif call.data == 'add':
        bot.send_message(call.message.chat.id, "Выберите дату для добавления задачи:", reply_markup=create_calendar(action="add"))
    elif call.data == 'random':
        random_command(call.message)
    elif call.data == 'help':
        bot.send_message(call.message.chat.id, HELP)
    elif call.data.startswith("select_date_add"):
        handle_date_for_task(call)
    elif call.data.startswith("select_date_show"):  # Новый обработчик показа задач
        handle_date_for_show(call)
    elif call.data.startswith("prev_month") or call.data.startswith("next_month"):
        handle_month_navigation(call)

# Новый обработчик выбора даты для показа задач
def handle_date_for_show(call):
    selected_date = call.data.split("|")[1]
    if selected_date in todos:
        tasks = f"Задачи на {selected_date}:\n" + '\n'.join([f"{i+1}. {task}" for i, task in enumerate(todos[selected_date])])
    else:
        tasks = f"На дату {selected_date} задач нет."
    bot.send_message(call.message.chat.id, tasks)

# Обработка выбора даты для добавления задачи
def handle_date_for_task(call):
    selected_date = call.data.split("|")[1]
    bot.send_message(call.message.chat.id, f"Вы выбрали дату {selected_date}. Введите задачу:")
    bot.register_next_step_handler_by_chat_id(call.message.chat.id, lambda msg: process_add_task(msg, selected_date))

# Обработка добавления задачи
def process_add_task(message, date):
    task = message.text.strip()
    add_todo(date, task)
    bot.send_message(message.chat.id, f'Задача "{task}" добавлена на дату {date}')

# Обработка навигации календаря
def handle_month_navigation(call):
    _, year, month = call.data.split("|")
    year, month = int(year), int(month)
    if call.data.startswith("prev_month"):
        if month == 1:
            year -= 1
            month = 12
        else:
            month -= 1
    elif call.data.startswith("next_month"):
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=create_calendar(year, month))

# Команда /random
@bot.message_handler(commands=['random'])
def random_command(message):
    task = choice(RANDOM_TASKS)
    today = datetime.now().strftime('%Y-%m-%d')
    add_todo(today, task)
    bot.send_message(message.chat.id, f'Задача "{task}" добавлена на сегодня ({today})')

# Загрузка задач при старте
load_todos()

# Запуск бота
bot.polling(none_stop=True)