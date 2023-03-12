#Ass We Can          # Талисман кода



import telebot
from telebot import types

bot = telebot.TeleBot('6262757409:AAHsjhCslfRa6kV1q-sZsE4gFgLPrfEAgME') # Определенние переменных
answer = ''



@bot.message_handler(commands=["start"]) # Функция по обработке команды /start
def start(message, res=False):
    
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("1")
    markup.add(item1)
    item2=types.KeyboardButton("2")
    markup.add(item2)

    bot.send_message(message.chat.id, "Привет!", reply_markup=markup)


@bot.message_handler(content_types=["text"]) # Функция по обработке кнопок
def handle_text(message):
    global answer

    if message.text.strip() == '1':
        answer = "1"
        bot.send_message(message.chat.id, answer)
    
    elif message.text.strip() == '2':
        answer = "2"
        bot.send_message(message.chat.id, answer)

    else:
        answer = "Я тебя не понимаю! Ты дебил?! Используй кнопки и команды!"
        bot.send_message(message.chat.id, answer)



bot.polling(none_stop=True, interval=0) # Запуск бота