import telebot
from emoji import emojize


def create_start_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    Ukraine = telebot.types.KeyboardButton(emojize("Ukraine :Ukraine:", use_aliases=True))
    Russia = telebot.types.KeyboardButton(emojize("Russia :Russia:", use_aliases=True))
    United_Kingdom = telebot.types.KeyboardButton(emojize("UK:United_Kingdom:", use_aliases=True))
    USA = telebot.types.KeyboardButton(emojize("USA:United_States:", use_aliases=True))

    keyboard.add(Ukraine, Russia)
    keyboard.add(United_Kingdom, USA)

    return keyboard


def ua_stat():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    stat = telebot.types.KeyboardButton(emojize(":Ukraine:Статистика по Вашій країні:Ukraine:", use_aliases=True))
    stat_world = telebot.types.KeyboardButton(
        emojize(":earth_americas:Статистика по світу:earth_americas:", use_aliases=True))
    stat_country = telebot.types.KeyboardButton(emojize("Статистика по обраній країні :bar_chart:", use_aliases=True))
    top10 = telebot.types.KeyboardButton(emojize("TOP-10:Ukraine:"))
    next = telebot.types.KeyboardButton(emojize("далі:right_arrow:"))

    keyboard.add(stat)
    keyboard.add(stat_world)
    keyboard.add(stat_country)
    keyboard.add(top10, next)

    return keyboard


def ru_stat():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    stat = telebot.types.KeyboardButton(emojize(":Russia:Статистика по Вашей стране:Russia:", use_aliases=True))
    stat_world = telebot.types.KeyboardButton(
        emojize(":earth_americas:Статистика по миру:earth_americas:", use_aliases=True))
    stat_country = telebot.types.KeyboardButton(
        emojize("Статистика по выбранной стране :bar_chart:", use_aliases=True))
    top10 = telebot.types.KeyboardButton(emojize("TOP-10:Russia:"))
    next = telebot.types.KeyboardButton(emojize(":right_arrow:дальше"))
    keyboard.add(stat)
    keyboard.add(stat_world)
    keyboard.add(stat_country)
    keyboard.add(top10, next)

    return keyboard


def uk_stat():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    stat = telebot.types.KeyboardButton(
        emojize(":United_Kingdom:Statistics for your country:United_Kingdom:", use_aliases=True))
    stat_world = telebot.types.KeyboardButton(
        emojize(":earth_americas:World Statistics:earth_americas:", use_aliases=True))
    stat_country = telebot.types.KeyboardButton(
        emojize("Statistics for the selected country :bar_chart:", use_aliases=True))
    top10 = telebot.types.KeyboardButton(emojize("TOP-10:United_Kingdom:"))
    next = telebot.types.KeyboardButton(emojize("next:right_arrow:"))
    keyboard.add(stat)
    keyboard.add(stat_world)
    keyboard.add(stat_country)
    keyboard.add(top10, next)

    return keyboard


def us_stat():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    stat = telebot.types.KeyboardButton(
        emojize(":United_States:Statistics for your country:United_States:",
                use_aliases=True))
    stat_world = telebot.types.KeyboardButton(
        emojize(":earth_americas:World Statistics:earth_americas:", use_aliases=True))
    stat_country = telebot.types.KeyboardButton(
        emojize("Statistics for the selected country :bar_chart:", use_aliases=True))
    top10 = telebot.types.KeyboardButton(emojize("TOP-10:United_States:"))
    next = telebot.types.KeyboardButton(emojize(":right_arrow:next"))
    keyboard.add(stat)
    keyboard.add(stat_world)
    keyboard.add(stat_country)
    keyboard.add(top10, next)

    return keyboard


def additional_key_ua():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    mailing = telebot.types.KeyboardButton(emojize("Щоденні сповіщення:alarm_clock:"))
    moz = telebot.types.KeyboardButton(emojize("Корисні поради:bat:"))
    tips = telebot.types.KeyboardButton(emojize("Корисні посилання:up-right_arrow:"))
    back = telebot.types.KeyboardButton(emojize("назад:left_arrow:"))
    keyboard.add(mailing)
    keyboard.add(moz)
    keyboard.add(tips)
    keyboard.add(back)

    return keyboard

def additional_key_ru():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    mailing = telebot.types.KeyboardButton(emojize("Ежедневные оповещения:alarm_clock:"))
    moz = telebot.types.KeyboardButton(emojize("Полезные советы:bat:"))
    tips = telebot.types.KeyboardButton(emojize("Полезные ссылки:up-right_arrow:"))
    back = telebot.types.KeyboardButton(emojize(":left_arrow:назад"))
    keyboard.add(mailing)
    keyboard.add(moz)
    keyboard.add(tips)
    keyboard.add(back)

    return keyboard

def additional_key_uk():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    mailing = telebot.types.KeyboardButton(emojize("Daily notifications:alarm_clock:"))
    moz = telebot.types.KeyboardButton(emojize("Tips:bat:"))
    tips = telebot.types.KeyboardButton(emojize("Useful links:up-right_arrow:"))
    back = telebot.types.KeyboardButton(emojize("back:left_arrow:"))
    keyboard.add(mailing)
    keyboard.add(moz)
    keyboard.add(tips)
    keyboard.add(back)

    return keyboard

def additional_key_us():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    mailing = telebot.types.KeyboardButton(emojize("Daily notifications :alarm_clock:"))
    moz = telebot.types.KeyboardButton(emojize("Tips :bat:"))
    tips = telebot.types.KeyboardButton(emojize("Useful links :up-right_arrow:"))
    back = telebot.types.KeyboardButton(emojize(":left_arrow:back"))
    keyboard.add(mailing)
    keyboard.add(moz)
    keyboard.add(tips)
    keyboard.add(back)

    return keyboard

def mail_keyboard_ua():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    set_up = telebot.types.KeyboardButton(emojize("Підписатись :white_check_mark:", use_aliases=True))
    cancel = telebot.types.KeyboardButton(emojize("Скасувати підписку :cross_mark:"))
    back = telebot.types.KeyboardButton(emojize("назад:left_arrow::left_arrow:"))
    keyboard.add(set_up)
    keyboard.add(cancel)
    keyboard.add(back)

    return keyboard

def mail_keyboard_ru():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    set_up = telebot.types.KeyboardButton(emojize("Подписаться :white_check_mark:", use_aliases=True))
    cancel = telebot.types.KeyboardButton(emojize("Отменить подписку :cross_mark:"))
    back = telebot.types.KeyboardButton(emojize(":left_arrow::left_arrow:назад"))
    keyboard.add(set_up)
    keyboard.add(cancel)
    keyboard.add(back)

    return keyboard

def mail_keyboard_uk():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    set_up = telebot.types.KeyboardButton(emojize("Subscribe:white_check_mark:", use_aliases=True))
    cancel = telebot.types.KeyboardButton(emojize("Unsubscribe:cross_mark:"))
    back = telebot.types.KeyboardButton(emojize("back:left_arrow::left_arrow:"))
    keyboard.add(set_up)
    keyboard.add(cancel)
    keyboard.add(back)

    return keyboard

def mail_keyboard_us():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    set_up = telebot.types.KeyboardButton(emojize("Subscribe :white_check_mark:", use_aliases=True))
    cancel = telebot.types.KeyboardButton(emojize("Unsubscribe :cross_mark:"))
    back = telebot.types.KeyboardButton(emojize(":left_arrow::left_arrow:back"))
    keyboard.add(set_up)
    keyboard.add(cancel)
    keyboard.add(back)

    return keyboard

def tips_ua():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    symptoms = telebot.types.KeyboardButton(emojize("Симптоми :red_circle:", use_aliases=True))
    sick = telebot.types.KeyboardButton(emojize("Я хворий? :skull:"))
    prevention = telebot.types.KeyboardButton(emojize("Профілактика :blue_circle:"))
    wash_hands = telebot.types.KeyboardButton(emojize("Як правильно мити руки? :palms_up_together:"))
    back = telebot.types.KeyboardButton(emojize("назад:left_arrow::left_arrow:"))
    keyboard.add(symptoms, prevention)
    keyboard.add(sick)
    keyboard.add(wash_hands)
    keyboard.add(back)

    return keyboard

def tips_ru():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    symptoms = telebot.types.KeyboardButton(emojize("Симптомы :red_circle:", use_aliases=True))
    sick = telebot.types.KeyboardButton(emojize("Я болен? :skull:"))
    prevention = telebot.types.KeyboardButton(emojize("Профилактика :blue_circle:"))
    wash_hands = telebot.types.KeyboardButton(emojize("Как правильно мыть руки? :palms_up_together:"))
    back = telebot.types.KeyboardButton(emojize(":left_arrow::left_arrow:назад"))
    keyboard.add(symptoms, prevention)
    keyboard.add(sick)
    keyboard.add(wash_hands)
    keyboard.add(back)

    return keyboard

def tips_uk():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    symptoms = telebot.types.KeyboardButton(emojize("Symptoms :red_circle:", use_aliases=True))
    sick = telebot.types.KeyboardButton(emojize("I am sick? :skull:"))
    prevention = telebot.types.KeyboardButton(emojize("Prevention :blue_circle:"))
    wash_hands = telebot.types.KeyboardButton(emojize("How to wash your hands? :palms_up_together:"))
    back = telebot.types.KeyboardButton(emojize("back:left_arrow::left_arrow:"))
    keyboard.add(symptoms, prevention)
    keyboard.add(sick)
    keyboard.add(wash_hands)
    keyboard.add(back)

    return keyboard

def tips_us():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    symptoms = telebot.types.KeyboardButton(emojize("Symptoms :red_circle:", use_aliases=True))
    sick = telebot.types.KeyboardButton(emojize("I am Sick? :skull:"))
    prevention = telebot.types.KeyboardButton(emojize("Prevention :blue_circle:"))
    wash_hands = telebot.types.KeyboardButton(emojize("How to wash your hands? :palms_up_together:"))
    back = telebot.types.KeyboardButton(emojize(":left_arrow::left_arrow:back"))
    keyboard.add(symptoms, prevention)
    keyboard.add(sick)
    keyboard.add(wash_hands)
    keyboard.add(back)

    return keyboard

def urls_ua():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    first_url = telebot.types.KeyboardButton("Міністерство охорони здоров’я України")
    second_url = telebot.types.KeyboardButton("Офіційний інформаційний портал Кабінету Міністрів України")
    third_url = telebot.types.KeyboardButton("Рекомендації ВООЗ для громадськості")
    fourth_url = telebot.types.KeyboardButton("Сторінка Центру громадського здоров’я України")
    back = telebot.types.KeyboardButton(emojize("назад:left_arrow::left_arrow:"))
    keyboard.add(first_url)
    keyboard.add(second_url)
    keyboard.add(third_url)
    keyboard.add(fourth_url)
    keyboard.add(back)

    return keyboard

def urls_ru():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    first_url = telebot.types.KeyboardButton("Всё про коронавирус!")
    second_url = telebot.types.KeyboardButton("Министерство Здравоохранения России")
    third_url = telebot.types.KeyboardButton("Всемирная Организация Здравохранения")
    back = telebot.types.KeyboardButton(emojize(":left_arrow::left_arrow:назад"))
    keyboard.add(first_url)
    keyboard.add(second_url)
    keyboard.add(third_url)
    keyboard.add(back)

    return keyboard

def urls_uk():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    first_url = telebot.types.KeyboardButton("Government Digital Service")
    second_url = telebot.types.KeyboardButton("National Health Service")
    third_url = telebot.types.KeyboardButton("World Health Organization")
    back = telebot.types.KeyboardButton(emojize("back:left_arrow::left_arrow:"))
    keyboard.add(first_url)
    keyboard.add(second_url)
    keyboard.add(third_url)
    keyboard.add(back)

    return keyboard

def urls_us():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    first_url = telebot.types.KeyboardButton("Centers for Disease Control")
    second_url = telebot.types.KeyboardButton("United States Federal Government")
    third_url = telebot.types.KeyboardButton("World Health Organization")
    back = telebot.types.KeyboardButton(emojize(":left_arrow::left_arrow:back"))
    keyboard.add(first_url)
    keyboard.add(second_url)
    keyboard.add(third_url)
    keyboard.add(back)

    return keyboard


ua = "Ukrainian"

ru = "Russian"

by = "Belorussian"

es = "English"

sp = "Spanish"

de = "German"

fr = "French"

it = "Italian"

jp = "Japanese"

lv = "Latvian"

cz = "Czech"

keyboard_remove = telebot.types.ReplyKeyboardRemove()
