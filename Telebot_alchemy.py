import telebot
from telebot import types
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import Session
from telebot.types import InputMediaPhoto

# Создаем объект бота
bot = telebot.TeleBot(token="6167075694:AAHP9vXY-4ROK8KZ3frEL9xr5S14no7w3dA")
# Создаем подключение к базе данных
engine = create_engine("sqlite:///venera_carpets_v_2.0.db")
# Объявляем переменную, нужна для пагинации ковров(прокрутки)
offset = 0
# Глобальная переменная форма, необходима для формирования запроса в БД
global shape


@bot.message_handler(commands=['start'])
def start(message):
    """Обработчик команды 'start' """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Выбрать форму")
    markup.add(btn1)
    bot.send_message(message.from_user.id, text="Приветствуем Вас в онлайн-магазине 'Ковры и коврики'! Мы находимся "
                                                "https://yandex.ru/maps/-/CCUKEEt~hD "
                     .format(message.from_user), reply_markup=markup)


@bot.message_handler(commands=['info'])
def info(message):
    """Обработчик команды 'info' """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Выбрать форму ковра")
    markup.add(btn1)
    bot.send_message(message.from_user.id, text="Ждем Вас в магазине ковров Персия! Мы находимся "
                                                "https://yandex.ru/maps/-/CCUKEEt~hD "
                     .format(message.from_user), reply_markup=markup)


@bot.message_handler(commands=['catalog'])
def catalog(message):
    """Обработчик команды 'catalog' """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Задаем кнопки для пагинации(прокрутки) ковров
    btn1 = types.KeyboardButton("Прямоугольник")
    btn2 = types.KeyboardButton("Овал")
    btn3 = types.KeyboardButton("Круг")
    markup.add(btn1, btn2, btn3)
    # Бот принимает на вход следующее сообщение, форму ковра
    mesg = bot.send_message(message.from_user.id, f"Какая форма ковра Вас интересует?", reply_markup=markup)
    bot.register_next_step_handler(mesg, choice_country)


def choice_country(message):
    global shape
    shape = message.text
    # Проверка полученного сообщения, для фильтрации правильной формы ковра, чтобы исключить поломку бота при отправке
    # неправильной формы пользователем текстом
    if shape == "Прямоугольник" or shape == "Овал" or shape == "Круг":
        markup = types.InlineKeyboardMarkup()
        # Задаем кнопки для пагинации(прокрутки) ковров
        btn1 = types.InlineKeyboardButton(text="Турция", callback_data="Турция")
        btn2 = types.InlineKeyboardButton(text="Иран", callback_data="Иран")
        btn3 = types.InlineKeyboardButton(text="Россия", callback_data="Россия")
        markup.add(btn1, btn2, btn3)
        photo1 = "https://avatars.mds.yandex.net/get-altay/5482460/2a0000018109c13a114686b58438fe852626/XXXL"
        caption = f"Выбрана форма {shape}, выберите страну"
        bot.send_photo(photo=photo1, caption=caption, chat_id=message.from_user.id, reply_markup=markup)
        return shape
    else:
        bot.send_message(message.from_user.id, f"Неверно выбрана форма ковра. Какая форма ковра Вас интересует?")
        catalog(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """Обработчик Inline кнопок"""
    req = call.data.split("_")
    # Прокидываем глобальные переменные, shape - форма, offset - нужна для пагинации, carpet_caption - текстовое
    # описание ковра, carpet_photo - URL ссылка на фото ковра, взятая из базы данных
    global shape
    global offset
    global country
    global shape
    global carpet_caption
    global carpet_photo
    # После выбора страны пользователем, переопределяем параметр country, прописываем запросы в базу
    if req[0] == "Турция":
        country = "Турция"
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text="Скрыть", callback_data="Удалить")
        btn2 = types.InlineKeyboardButton(text="Вперед -- >", callback_data="Вперед")
        markup.add(btn1, btn2)
        url = "https://avatars.mds.yandex.net/get-altay/5482460/2a0000018109c13a114686b58438fe852626/XXXL"
        caption = f"Выбрана форма {shape}, страна Турция, нажмите вперед"
        media = InputMediaPhoto(media=url, caption=caption)
        bot.edit_message_media(media=media, reply_markup=markup, chat_id=call.message.chat.id,
                               message_id=call.message.message_id)
    elif req[0] == "Россия":
        country = "Россия"
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text="Изменить", callback_data="Удалить")
        btn2 = types.InlineKeyboardButton(text="Вперед -- >", callback_data="Вперед")
        markup.add(btn1, btn2)
        url = "https://avatars.mds.yandex.net/get-altay/5482460/2a0000018109c13a114686b58438fe852626/XXXL"
        caption = f"Выбрана форма {shape}, страна Россия, нажмите вперед"
        media = InputMediaPhoto(media=url, caption=caption)
        bot.edit_message_media(media=media, reply_markup=markup, chat_id=call.message.chat.id,
                               message_id=call.message.message_id)
    elif req[0] == "Иран":
        country = "Иран"
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text="Скрыть", callback_data="Удалить")
        btn2 = types.InlineKeyboardButton(text="Вперед -- >", callback_data="Вперед")
        markup.add(btn1, btn2)
        url = "https://avatars.mds.yandex.net/get-altay/5482460/2a0000018109c13a114686b58438fe852626/XXXL"
        caption = f"Выбрана форма {shape}, страна Иран, нажмите вперед"
        media = InputMediaPhoto(media=url, caption=caption)
        bot.edit_message_media(media=media, reply_markup=markup, chat_id=call.message.chat.id,
                               message_id=call.message.message_id)
    # По командам 'Вперед' и 'Назад' вызываем функцию запроса из базы данных сведений о ковре
    elif req[0] == "Вперед":
        offset = offset + 1
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text="< -- Назад", callback_data="Назад")
        btn2 = types.InlineKeyboardButton(text="Скрыть", callback_data="Удалить")
        btn3 = types.InlineKeyboardButton(text="Вперед -- >", callback_data="Вперед")
        btn4 = types.InlineKeyboardButton(text="Изменить", callback_data="Сменить")
        btn5 = types.InlineKeyboardButton(text="Связаться с нами", callback_data="Уточнить")
        markup.add(btn1, btn2, btn3, btn4, btn5)
        # Вызываем функцию get_media для запроса сведений из базы данных, передаем функции аргументами текущий параметр
        # пагинации, страну и форму ковра
        carpet_photo = get_media(offset, country, shape)[0]
        carpet_caption = get_media(offset, country, shape)[1]
        media = InputMediaPhoto(media=get_media(offset, country, shape)[0],
                                caption=get_media(offset, country, shape)[1])
        bot.edit_message_media(media=media, reply_markup=markup, chat_id=call.message.chat.id,
                               message_id=call.message.message_id)
    elif req[0] == "Назад":
        if offset >= 2:
            offset = offset - 1
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(text="< -- Назад", callback_data="Назад")
            btn2 = types.InlineKeyboardButton(text="Скрыть", callback_data="Удалить")
            btn3 = types.InlineKeyboardButton(text="Вперед -- >", callback_data="Вперед")
            btn4 = types.InlineKeyboardButton(text="Изменить", callback_data="Сменить")
            btn5 = types.InlineKeyboardButton(text="Связаться с нами", callback_data="Уточнить")
            markup.add(btn1, btn2, btn3, btn4, btn5)
            # Вызываем функцию get_media для запроса сведений из базы данных, передаем функции аргументами текущий
            # параметр пагинации, страну и форму ковра
            carpet_photo = get_media(offset, country, shape)[0]
            carpet_caption = get_media(offset, country, shape)[1]
            media = InputMediaPhoto(media=get_media(offset, country, shape)[0],
                                    caption=get_media(offset, country, shape)[1])
            bot.edit_message_media(media=media, reply_markup=markup, chat_id=call.message.chat.id,
                                   message_id=call.message.message_id)
        else:
            pass
    # Обработчики кнопок уточнения данных о ковре, изменения страну или сброса сообщения
    elif req[0] == "Уточнить":
        bot.send_message(chat_id=call.message.chat.id,
                         text="Мы уточним наличие наличие, цену и в ближайшее время свяжемся с Вами!")
        bot.send_photo(chat_id=1665218818, photo=carpet_photo,
                       caption=f"Новый заказ на ковер!\nЗаказчик {call.message.message_id} \n{carpet_caption}")
    elif req[0] == "Сменить":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # Задаем кнопки для пагинации(прокрутки) ковров
        btn1 = types.KeyboardButton("Прямоугольник")
        btn2 = types.KeyboardButton("Овал")
        btn3 = types.KeyboardButton("Круг")
        markup.add(btn1, btn2, btn3)
        mesg = bot.send_message(chat_id=call.message.chat.id, text=f"Какая форма Вас интересует?", reply_markup=markup)
        bot.register_next_step_handler(mesg, choice_country)
    elif req[0] == "Удалить":
        offset = 0
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # Задаем кнопки для пагинации(прокрутки) ковров
        btn1 = types.KeyboardButton("Прямоугольник")
        btn2 = types.KeyboardButton("Овал")
        btn3 = types.KeyboardButton("Круг")
        markup.add(btn1, btn2, btn3)
        mesg = bot.send_message(chat_id=call.message.chat.id, text=f"Какая форма Вас интересует?", reply_markup=markup)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.register_next_step_handler(mesg, choice_country)


@bot.message_handler(content_types=['text'])
def open_catalog(message):
    """Обработчик текстового сообщения и Reply кнопок"""
    if message.text == "Выбрать форму ковра":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # Задаем кнопки для пагинации(прокрутки) ковров
        btn1 = types.KeyboardButton("Прямоугольник")
        btn2 = types.KeyboardButton("Овал")
        btn3 = types.KeyboardButton("Круг")
        markup.add(btn1, btn2, btn3)
        mesg = bot.send_message(message.from_user.id, f"Какая форма ковра Вас интересует?", reply_markup=markup)
        bot.register_next_step_handler(mesg, choice_country)
    elif message.text == "Как нас найти":
        bot.send_message(message.from_user.id, text="https://yandex.ru/maps/-/CCUKEEt~hD")
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Выбрать форму ковра")
        btn2 = types.KeyboardButton("Как нас найти")
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, text="Для просмотра каталога выберите форму", reply_markup=markup)


def get_media(offset, country, shape):
    """Функция ищет ковер в базе данных по выбранной стране и возвращает URL фотографии и текстовое описание текущего
    ковра """
    offset = offset + 1
    stmt_id = text(
        f"SELECT DISTINCT carpet_id FROM carpets WHERE country = '{country}' AND shape = '{shape}' LIMIT 1 "
        f"OFFSET {offset}")
    with Session(engine) as session:
        result_id = session.execute(stmt_id)
        id_list = list()
        for row in result_id:
            id_list.append(row[0])
        try:
            carpet_id = id_list[0]
        except IndexError:
            url = "https://avatars.mds.yandex.net/get-altay/5482460/2a0000018109c13a114686b58438fe852626/XXXL"
            caption = "С таким запросом товаров в данный момент нет"
        stmt = text(f"SELECT name, price, country, composition, density, height_pile, (SELECT t_image "
                    f"FROM t_images WHERE carpet_id = {carpet_id} LIMIT 1) FROM carpets "
                    f"WHERE carpet_id = {carpet_id} ")
        result = session.execute(stmt)
        stmt_sizes = text(f"SELECT c_size FROM c_sizes WHERE carpet_id = {carpet_id}")
        result_sizes = session.execute(stmt_sizes)
        size_list = list()
        for size in result_sizes:
            size_list.append(size[0])
        sizes_list_str = ', '.join(size_list)
        if len(sizes_list_str) == 0:
            sizes_list_str = 'Ожидается получение'
        for row in result:
            # row[2] - цена, пока отключена
            url = f"{row[6]}"
            if row[6] is None:
                url = "https://venera-carpet.ru/img/productOval.png"
            caption = f"{row[0]} \nСтрана: {row[2]}\nCостав: {row[3]} \nРазмеры: {sizes_list_str}" \
                      f"\nПлотность: {row[4]} узлов/м2 \nВысота ворса: {row[5]} мм "
        session.commit()
    return url, caption


bot.polling(none_stop=True, interval=0)
