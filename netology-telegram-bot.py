# to-do list - программа для ведения списка дел

# тз

import telebot
token = '7769145923:AAEA5JHOeuWcwIvUr-shE6l3lgqmQ4_mero'
bot = telebot.TeleBot(token)

my_name = 'Дима'


@bot.message_handler(content_types=["text"])
def echo(message):
    if my_name in message.text:
        text = 'Ба! Знакомые все лица'
    else:
        text = message.text
    bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)