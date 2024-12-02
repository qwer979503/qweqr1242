import telebot
import random
BOT_TOKEN = '7936298846:AAEGaWPXba40OXRICJTtLo6DgAoQcug_Jbo'  # Замените на ваш токен
bot = telebot.TeleBot(BOT_TOKEN)
game_state = {}  # Словарь для хранения состояния игры для отдельных пользователей


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Как я могу помочь? /help")


@bot.message_handler(commands=["help"])
def help_command(message):
    help_text = """ 
    /start - Запустить бота
    /help - Получить помощь
    /info - Информация о боте
    /joke - Получить случайную шутку
    /quote - Получить случайную цитату
    /game - Играть в игру на угадывание числа
    /button - Протестировать взаимодействие с кнопкой
    """
    bot.send_message(message.chat.id, help_text)



@bot.message_handler(commands=["info"])
def info(message):
    bot.reply_to(message,
                 "Я ваш телеграм-ассистент. Могу предоставить информацию, помочь с командами и отвечать на вопросы. Могу сбивать истребители , а  по впоросам @Ton_401 пишитея поплачь")


@bot.message_handler(commands=["joke"])
def joke(message):
    jokes = [
        "Почему программисты предпочитают темный режим? Потому что свет привлекает ошибки!",
        "Как называют кошку, которая умеет программировать? Мяу-граммер!",
        "Якубов леха сбивает истребители , мораль басни такова"
    ]
    bot.reply_to(message, random.choice(jokes))


@bot.message_handler(commands=["quote"])
def quote(message):
    quotes = [
        "Сложность всегда является выбором, возможность всегда - обязанностью.",
        "Программирование - это не только наука, но и искусство."
    ]
    bot.reply_to(message, random.choice(quotes))


@bot.message_handler(commands=["game"])
def game(message):
    game_state[message.chat.id] = {'number': random.randint(1, 10), 'guesses_left': 3}
    bot.reply_to(message, "Я загадал число от 1 до 10. У вас 3 попытки. Какой ваш вариант?")


@bot.message_handler(func=lambda message: message.text.isdigit() and message.chat.id in game_state)
def guess_number(message):
    chat_id = message.chat.id
    guess = int(message.text)
    state = game_state[chat_id]
    if guess == state['number']:
        bot.reply_to(message, "Правильно! Вы выиграли!")
        del game_state[chat_id]  # удаляем состояние игры, если пользователь выиграл
    elif state['guesses_left'] > 1:
        state['guesses_left'] -= 1
        bot.reply_to(message, f"Неправильно. У вас осталось {state['guesses_left']} попыток.")
    else:
        bot.reply_to(message, f"Неправильно. Загаданное число было {state['number']}. Вы проиграли!")
        del game_state[chat_id]





@bot.message_handler(commands=["button"])
def button_game(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("Нажми на кнопку!", "Информация о пользователе")
    bot.send_message(message.chat.id, "Нажмите кнопку!", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Нажми на кнопку!")
def button_response(message):
    bot.reply_to(message, f"Спасибо за нажатие кнопки, {message.from_user.first_name}!")


@bot.message_handler(func=lambda message: message.text == "Информация о пользователе")
def user_info(message):
    user_info_text = (
        f"Ваше имя: {message.from_user.first_name}\\n"
        f"Ваша фамилия: {message.from_user.last_name}\\n"
        f"Ваш ID: {message.from_user.id}\\n"
        f"Ваш ник: {message.from_user.username if message.from_user.username else 'Не задан'}"
    )
    bot.reply_to(message, user_info_text)

@bot.message_handler(func=lambda message: message.text.lower() == "пока")
def goodbye(message):
    bot.reply_to(message, f"Пока, {message.from_user.first_name}!")

@bot.message_handler(func=lambda message: True)
def default_message(message):
    command = message.text.lower()

    if command in ["привет", "hi", "hello"]:
        bot.reply_to(message, f"Привет, {message.from_user.first_name}!")
    elif "как дела" in command:
        bot.reply_to(message, "У меня все отлично, спасибо! А у вас как дела?")
    elif "что нового" in command:
        bot.reply_to(message, "Всегда рад помочь! Что вас интересует?")
    elif "плачь" in command:
        bot.reply_to(message, "Мне пофиг я абсолют")
    elif "самолёт" in command:
        bot.reply_to(message, "Я сбил истребитель")
    elif "ссылка" in command:
        bot.send_message(message.chat.id,
                         "[Вот ваша ссылка: на гоблины](https://t.me/GoblinMine_bot/start?startapp=1259503170)",
                         parse_mode='Markdown')


# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
