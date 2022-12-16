from telebot import TeleBot, types
from package.weather import get_weather
from package.currency import get_main_currencies
from package.rational_calculator import calculation as rat_calc
from package.complex_calculator import calculation as com_calc
import logging

level = logging.DEBUG
logger = logging.getLogger("log")
form = "%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s"
logger.setLevel(level)
fh = logging.FileHandler(filename=f"log.txt", encoding="UTF-8")
fh.setFormatter(logging.Formatter(form))
fh.setLevel(level)
logger.addHandler(fh)
logger.debug(f"Logger was initialized")

TOKEN = '5535429972:AAF6gALeYPninEfitow4PPoStDBtL6LkFjU'
bot = TeleBot(TOKEN)


# Создать бот-калькулятор для работы с рациональными и комплексными числами, организовать кнопочное меню, добавить
# систему логирования

@bot.message_handler(command=["start"])
def start(message):
    logger.debug(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Погода"),
        types.KeyboardButton("Курс валют"),
        types.KeyboardButton("Калькулятор")
    )
    logger.debug("{0.first_name}".format(message.from_user))
    bot.send_message(message.chat.id, "Привет, {0.first_name}!".format(message.from_user), reply_markup=markup)
    markup = types.ReplyKeyboardRemove()


@bot.message_handler(content_types=['text'])
def bot_message(message):
    logger.debug(f"Chat ID - {message.chat.id}")
    logger.debug("First Name - {0.first_name}".format(message.from_user))
    if message.text == "Погода":
        loc_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        loc_markup.add(types.KeyboardButton(text="Отправить местоположение", request_location=True))
        bot.send_message(message.chat.id, "Нажми на кнопку и передай мне свое местоположение",
                         reply_markup=loc_markup)
    elif message.text == "Курс валют":
        bot.send_message(message.chat.id, get_main_currencies())
    elif message.text == "Калькулятор":
        cm = types.InlineKeyboardMarkup()
        cm.row(
            types.InlineKeyboardButton(text='Комплексные числа', callback_data="ComplexCalculator"),
            types.InlineKeyboardButton(text='Рациональные числа', callback_data="RationalCalculator")
               )
        bot.send_message(message.chat.id, "Какие числа будем считать?", reply_markup=cm)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(
            types.KeyboardButton("Погода"),
            types.KeyboardButton("Курс валют"),
            types.KeyboardButton("Калькулятор")
        )
        bot.send_message(message.chat.id, "Мои функции \n Погода - отправляет погоду по текущей геолокации \nКурс "
                                          "валют - отправляет курсы ЦБ РФ по трем основным валютам \nКалькулятор",
                         reply_markup=markup)


@bot.message_handler(content_types=["location"])
def location(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Погода"),
        types.KeyboardButton("Курс валют"),
        types.KeyboardButton("Калькулятор")
    )
    if message.location is not None:
        logger.debug(f"lat - {message.location.latitude}, lon - {message.location.longitude}")
        bot.send_message(message.chat.id, get_weather(message.location.latitude, message.location.longitude),
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Ошибка при получении геолокации")


@bot.callback_query_handler(func=lambda call:True)
def callback_func(query):
    data = query.data
    if data == "RationalCalculator":
        msg = bot.send_message(query.message.chat.id, "Введите выражение, которое необходимо посчитать \nВ формате "
                                                      "число-пробел-знак-пробел-число (x + y)")
        bot.register_next_step_handler(msg, rational_calc)
    elif data == "ComplexCalculator":
        msg = bot.send_message(query.message.chat.id, "Введите выражение, которое необходимо посчитать \nВ формате "
                                                      "число$знак$число (1 + 7j $ + $ 3 - 2j)")
        bot.register_next_step_handler(msg, complex_calc)


def rational_calc(message):
    value = message.text
    value = value.split()
    if (" " in value) and (len(value) == 2):
        try:
            value1, value2 = float(value[0]), float(value[2])
            result = rat_calc(value1, value[1], value2)
            if result % 1 == 0:
                result = int(result)
            bot.send_message(message.chat.id, str(result))
        except TypeError:
            logger.warning("Ошибка типов!")
            logger.debug(f"{value}")
            bot.send_message(message.chat.id, "Возникла ошибка при рассчетах! Проверьте корректность вводимых данных")
    else:
        logger.warning("Ошибка ввода!")
        logger.debug(f"{value}")
        bot.send_message(message.chat.id, "Ошибка ввода! Проверь корректность вводимых данных!")


def complex_calc(message):
    value = message.text
    if (" " in value) and ("$" in value):
        value = value.replace(" ", "")
        value = value.split("$")
        if len(value) == 3:
            try:
                value1, value2 = complex(value[0]), complex(value[2])
                bot.send_message(message.chat.id, str(com_calc(value1, value[1], value2)))
            except ValueError:
                logger.warning("Ошибка типов!")
                logger.debug(f"{value}")
                bot.send_message(message.chat.id,
                                 "Возникла ошибка при рассчетах! Проверьте корректность вводимых данных")
            else:
                bot.send_message(message.chat.id, "Ошибка ввода! Проверь корректность вводимых данных!")
                logger.warning("Ошибка ввода!")
                logger.debug(f"{value}")
    else:
        logger.warning("Ошибка ввода!")
        logger.debug(f"{value}")
        bot.send_message(message.chat.id, "Ошибка ввода! Проверь корректность вводимых данных!")


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.polling(none_stop=True, interval=0)
