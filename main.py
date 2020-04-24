import reques as reques
from models import Stat, Users, Country, init_db
from function_Stat import *
from config import token_1, LOGGER_CONFIG
from keyboards import *

import time
import threading
import logging
import emoji
import datetime
import telebot

log = logging.getLogger("MainLog")
fh = logging.FileHandler(LOGGER_CONFIG["file"])
fh.setLevel(LOGGER_CONFIG["level"])
fh.setFormatter(LOGGER_CONFIG["formatter"])
log.addHandler(fh)
log.setLevel(LOGGER_CONFIG["level"])


def set_up_bot():
    bot = telebot.TeleBot(token_1)
    return bot


def send_stat_user(id, country_name):
    bot = set_up_bot()
    if country_name == "Світ":
        stat = search("world")
        bot.send_message(id,
                         "<b>У всьому світі:</b>\nЗагальна кількість випадків: <b>{0}</b>\nІз них кількість смертей: <b>{1}</b>\nОдужало: <b>{2}</b>\nДата оновлення: <b>{3}</b>\n(оновлюється кожні півгодини)\n".format(
                             C(stat[1]), C(stat[2]), C(stat[3]), stat[6]), parse_mode="html")
        return False
    elif country_name == "Мир":
        stat = search("world")
        bot.send_message(id,
                         "<b>Во всём мире:</b>\nОбщее количество случаев: <b>{0}</b>\nИз них количество смертей: <b>{1}</b>\nВыздоровели: <b>{2}</b>\nДата обновление: <b>{3}</b>\n(обновляется каждые полчаса)\n".format(
                             C(stat[1]), C(stat[2]), C(stat[3]), stat[6]), parse_mode="html")
        return False

    ind = "ua"
    try:
        ind = "en"
        stat = search(translate_country(country_name, es))
    except:
        try:
            ind = "ua"
            stat = search(translate_country(country_name, ua))
        except:
            try:
                ind = "ru"
                stat = search(translate_country(country_name, ru))
            except:
                bot.send_message(id, emojize(
                    "Упс...:pleading_face:\nНе знайшов такої країни.\nПеревір правильність написання назви країни та спробуй ще раз.\n(Почати спочатку - /start)"))
                return False

    stat_date = list(stat[6])
    for i in range(7):
        stat_date.pop()
    stat[6] = "".join(stat_date)

    if country_name == "world":
        if ind == "en":
            bot.send_message(id,
                             "<b>Worldwide:</b>\nTotal number of cases: <b>{0}</b>\nThe number of deaths: <b>{1}</b>\nRecovered: <b>{2}</b>\nDate of update: <b>{3}</b>\n(updated every half hour)\n".format(
                                 C(stat[1]), C(stat[2]), C(stat[3]), stat[6]), parse_mode="html")
    elif ind == "ua":
        bot.send_message(id,
                         "Країна: <b>{0}</b>\nЗагальна кількість випадків: <b>{1}</b>\nІз них кількість смертей: <b>{2}</b>\nОдужало: <b>{3}</b>\nДата оновлення: <b>{4}</b>\n(оновлюється кожні півгодини)\n".format(
                             stat[0], C(stat[1]), C(stat[2]), C(stat[3]), stat[6]), parse_mode="html")
    elif ind == "ru":
        bot.send_message(id,
                         "Страна: <b>{0}</b>\nОбщее количество случаев: <b>{1}</b>\nИз них количество смертей: <b>{2}</b>\nВыздоровели: <b>{3}</b>\nДата обновление: <b>{4}</b>\n(обновляется каждые полчаса)\n".format(
                             stat[0], C(stat[1]), C(stat[2]), C(stat[3]), stat[6]), parse_mode="html")
    elif ind == "en":
        bot.send_message(id,
                         "Country: <b>{0}</b>\nTotal number of cases: <b>{1}</b>\nThe number of deaths: <b>{2}</b>\nRecovered: <b>{3}</b>\nDate of update: <b>{4}</b>\n(updated every half hour)\n".format(
                             stat[0], C(stat[1]), C(stat[2]), C(stat[3]), stat[6]), parse_mode="html")


def checktime():
    b = datetime.datetime.now()
    today = datetime.datetime(b.year, b.month, b.day)
    bot = set_up_bot()

    if (b - today).seconds >= 28800 and (b - today).seconds <= 30600:
        log.debug("Start MAIL")
        users = Users.select()
        for user in users:
            if user.ua:
                try:
                    bot.send_message(user.user_id, "Доброго ранку.\nСтатистика на {0}:\n".format(
                        datetime.date(b.year, b.month, b.day)))
                    send_stat_user(user.user_id, "Україна")
                    send_stat_user(user.user_id, "Світ")
                except:
                    log.info("MAIL ERROR for user_id - %s" % (user.user_id))

            elif user.ru:
                try:
                    send_stat_user(user.user_id, "Россия")
                    send_stat_user(user.user_id, "Мир")
                except:
                    log.info("MAIL ERROR for user_id - %s" % (user.user_id))
            elif user.uk:
                try:
                    send_stat_user(user.user_id, "UK")
                    send_stat_user(user.user_id, "world")
                except:
                    log.info("MAIL ERROR for user_id - %s" % (user.user_id))
            elif user.uk:
                try:
                    send_stat_user(user.user_id, "USA")
                    send_stat_user(user.user_id, "world")
                except:
                    log.info("MAIL ERROR for user_id - %s" % (user.user_id))


def check_update():
    checktime()
    stat = search("world")
    try:
        reques.worldstat()
        if reques.worldstat()["total_cases"] != stat[1]:
            init_db()
    except:
        print("Статистика не прийшла. ИСПРАВИТЬ НА ЛОГГИРОВАНИЕ")
    time.sleep(1800)
    check_update()


def bot():
    bot = set_up_bot()

    def text_has_emoji(text):
        for character in text:
            if character in emoji.UNICODE_EMOJI:
                return True
        return False

    def check_user(message):
        try:
            user = Users.get(Users.user_id == message.chat.id)
            return True
        except:
            return False

    def del_user(message):
        try:
            user = Users.get(Users.user_id == message.chat.id)
            user.delete_instance()
            return True
        except:
            return False

    def add_user(message, ua, ru, uk, us):
        try:
            user = Users.create(user_id=message.chat.id, ua=ua, ru=ru, uk=uk, us=us)
            return True
        except:
            return False

    def send_stat(message, country_name):

        if country_name == "Світ":
            stat = search("world")

            stat_date = list(stat[6])
            for i in range(7):
                stat_date.pop()
            stat[6] = "".join(stat_date)

            bot.send_message(message.chat.id,
                             "<b>У всьому світі:</b>\nЗагальна кількість випадків: <b>{0}</b>\nІз них кількість смертей: <b>{1}</b>\nОдужало: <b>{2}</b>\nДата оновлення: <b>{3}</b>\n(оновлюється кожні півгодини)\n".format(
                                 C(stat[1]), C(stat[2]), C(stat[3]), stat[6]), parse_mode="html")
            return False
        elif country_name == "Мир":
            stat = search("world")

            stat_date = list(stat[6])
            for i in range(7):
                stat_date.pop()
            stat[6] = "".join(stat_date)

            bot.send_message(message.chat.id,
                             "<b>Во всём мире:</b>\nОбщее количество случаев: <b>{0}</b>\nИз них количество смертей: <b>{1}</b>\nВыздоровели: <b>{2}</b>\nДата обновление: <b>{3}</b>\n(обновляется каждые полчаса)\n".format(
                                 C(stat[1]), C(stat[2]), C(stat[3]), stat[6]), parse_mode="html")
            return False

        ind = "ua"
        try:
            ind = "en"
            stat = search(translate_country(country_name, es))
        except:
            try:
                ind = "ua"
                stat = search(translate_country(country_name, ua))
            except:
                try:
                    ind = "ru"
                    stat = search(translate_country(country_name, ru))
                except:
                    bot.send_message(message.chat.id, emojize(
                        "Whoops...:pleading_face:\nDon't find country or command.\nTry again.\n(start over - /start)"))
                    log.debug("Don't find country or command, message - %s (don't forget check translate)" % (
                            message.text))
                    return False


        if not stat:
            bot.send_message(message.chat.id, emojize(
                "Whoops ...: pleading face:\ Sorry, no data from this country. \n (Start over - /start)"))
            log.debug("Doesn't find data for country - %s" % (message.text))
            return False

        stat_date = list(stat[6])
        for i in range(7):
            stat_date.pop()
        stat[6] = "".join(stat_date)

        if country_name == "world":
            if ind == "en":
                bot.send_message(message.chat.id,
                                 "<b>Worldwide:</b>\nTotal number of cases: <b>{0}</b>\nThe number of deaths: <b>{1}</b>\nRecovered: <b>{2}</b>\nDate of update: <b>{3}</b>\n(updated every half hour)\n".format(
                                     C(stat[1]), C(stat[2]), C(stat[3]), stat[6]), parse_mode="html")
        elif ind == "ua":
            bot.send_message(message.chat.id,
                             "Країна: <b>{0}</b>\nЗагальна кількість випадків: <b>{1}</b>\nІз них кількість смертей: <b>{2}</b>\nОдужало: <b>{3}</b>\nДата оновлення: <b>{4}</b>\n(оновлюється кожні півгодини)\n".format(
                                 stat[0], C(stat[1]), C(stat[2]), C(stat[3]), stat[6]), parse_mode="html")
        elif ind == "ru":
            bot.send_message(message.chat.id,
                             "Страна: <b>{0}</b>\nОбщее количество случаев: <b>{1}</b>\nИз них количество смертей: <b>{2}</b>\nВыздоровели: <b>{3}</b>\nДата обновление: <b>{4}</b>\n(обновляется каждые полчаса)\n".format(
                                 stat[0], C(stat[1]), C(stat[2]), C(stat[3]), stat[6]), parse_mode="html")
        elif ind == "en":
            bot.send_message(message.chat.id,
                             "Country: <b>{0}</b>\nTotal number of cases: <b>{1}</b>\nThe number of deaths: <b>{2}</b>\nRecovered: <b>{3}</b>\nDate of update: <b>{4}</b>\n(updated every half hour)\n".format(
                                 stat[0], C(stat[1]), C(stat[2]), C(stat[3]), stat[6]), parse_mode="html")

    def send_top(message, ind):
        top10_country, top10_cases = top_10()
        if not top10_country:
            log.info("Cannot take top 10 - %s")

        if ind == "ua":
            for i in range(len(top10_country)):
                top10_country[i] = translate_country_en(top10_country[i], ua)
            bot.send_message(message.chat.id, "ТОП-10 країн за кількістю виявлених випадків:")
            bot.send_message(message.chat.id,
                             "<b>1.</b>{0} - {1}\n<b>2.</b>{2} - {3}\n<b>3.</b>{4} - {5}\n4.{6} - {7}\n5.{8} - {9}\n6.{10} - {11}\n7.{12} - {13}\n8.{14} - {15}\n9.{16} - {17}\n10.{18} - {19}".format(
                                 top10_country[0], C(top10_cases[0]), top10_country[1], C(top10_cases[1]),
                                 top10_country[2],
                                 C(top10_cases[2]), top10_country[3], C(top10_cases[3]), top10_country[4],
                                 C(top10_cases[4]),
                                 top10_country[5], C(top10_cases[5]), top10_country[6], C(top10_cases[6]),
                                 top10_country[7],
                                 C(top10_cases[7]), top10_country[8], C(top10_cases[8]), top10_country[9],
                                 C(top10_cases[9])),
                             parse_mode="html")

        if ind == "ru":
            for i in range(len(top10_country)):
                top10_country[i] = translate_country_en(top10_country[i], ru)
            bot.send_message(message.chat.id, "ТОП-10 стран по количеству выявленных случаев:")
            bot.send_message(message.chat.id,
                             "<b>1.</b>{0} - {1}\n<b>2.</b>{2} - {3}\n<b>3.</b>{4} - {5}\n4.{6} - {7}\n5.{8} - {9}\n6.{10} - {11}\n7.{12} - {13}\n8.{14} - {15}\n9.{16} - {17}\n10.{18} - {19}".format(
                                 top10_country[0], C(top10_cases[0]), top10_country[1], C(top10_cases[1]),
                                 top10_country[2],
                                 C(top10_cases[2]), top10_country[3], C(top10_cases[3]), top10_country[4],
                                 C(top10_cases[4]),
                                 top10_country[5], C(top10_cases[5]), top10_country[6], C(top10_cases[6]),
                                 top10_country[7],
                                 C(top10_cases[7]), top10_country[8], C(top10_cases[8]), top10_country[9],
                                 C(top10_cases[9])),
                             parse_mode="html")

        if ind == "en":
            bot.send_message(message.chat.id, "TOP 10 countries by the number of cases identified:")
            bot.send_message(message.chat.id,
                             "<b>1.</b>{0} - {1}\n<b>2.</b>{2} - {3}\n<b>3.</b>{4} - {5}\n4.{6} - {7}\n5.{8} - {9}\n6.{10} - {11}\n7.{12} - {13}\n8.{14} - {15}\n9.{16} - {17}\n10.{18} - {19}".format(
                                 top10_country[0], C(top10_cases[0]), top10_country[1], C(top10_cases[1]),
                                 top10_country[2],
                                 C(top10_cases[2]), top10_country[3], C(top10_cases[3]), top10_country[4],
                                 C(top10_cases[4]),
                                 top10_country[5], C(top10_cases[5]), top10_country[6], C(top10_cases[6]),
                                 top10_country[7],
                                 C(top10_cases[7]), top10_country[8], C(top10_cases[8]), top10_country[9],
                                 C(top10_cases[9])),
                             parse_mode="html")

    @bot.message_handler(commands=['start'])
    def start(message):
        keyboard = create_start_keyboard()
        bot.send_message(message.chat.id, "<b>Welcome - {0.first_name}</b>".format(message.from_user),
                         parse_mode="html",
                         reply_markup=keyboard)

        bot.send_message(message.chat.id, "Choose your country:")

    @bot.message_handler(
        content_types=['video', "audio", "document", "photo", "sticker", " video", "video_note", "voice", "location",
                       "contact"])
    def other_send(message):
        bot.send_sticker(message.chat.id,
                         "CAACAgIAAxkBAAJGSl6U9Fp--kpof1zujySvfdTyYe64AALJAQACVp29CnXYcMSIGS6NGAQ")
        bot.send_message(message.chat.id, "please send me a text only.")

    @bot.message_handler(content_types=['text'])
    def determine_country(message):

        # Ссылки UA
        if message.text == "Корисні посилання↗":
            bot.send_message(message.chat.id, "Обери про що бажаєшь дізнатись: ", reply_markup=urls_ua())
        elif message.text == "Міністерство охорони здоров’я України":
            bot.send_message(message.chat.id, "https://moz.gov.ua")
        elif message.text == "Офіційний інформаційний портал Кабінету Міністрів України":
            bot.send_message(message.chat.id, "https://covid19.gov.ua")
        elif message.text == "Рекомендації ВООЗ для громадськості":
            bot.send_message(message.chat.id, "https://www.who.int/emergencies/diseases/novel-coronavirus-2019")
        elif message.text == "Сторінка Центру громадського здоров’я України":
            bot.send_message(message.chat.id, "https://www.phc.org.ua")

        # Ссылки RU
        elif message.text == "Полезные ссылки↗":
            bot.send_message(message.chat.id, "Выбери, что тебе интересно: ", reply_markup=urls_ru())
        elif message.text == "Всё про коронавирус!":
            bot.send_message(message.chat.id, "https://стопкоронавирус.рф")
        elif message.text == "Министерство Здравоохранения России":
            bot.send_message(message.chat.id, "https://www.rosminzdrav.ru")
        elif message.text == "Всемирная Организация Здравохранения":
            bot.send_message(message.chat.id, "https://www.who.int/ru/emergencies/diseases/novel-coronavirus-2019")

        # Ссылки UK
        elif message.text == "Useful links↗":
            bot.send_message(message.chat.id, "Choose what interests you: ", reply_markup=urls_uk())
        elif message.text == "Government Digital Service":
            bot.send_message(message.chat.id, "https://www.gov.uk/coronavirus")
        elif message.text == "National Health Service":
            bot.send_message(message.chat.id, "https://www.nhs.uk/conditions/coronavirus-covid-19/")
        elif message.text == "World Health Organization":
            bot.send_message(message.chat.id, "https://www.who.int/home")

        # Ссылки USA
        elif message.text == "Useful links ↗":
            bot.send_message(message.chat.id, "Choose what interests you: ", reply_markup=urls_us())
        elif message.text == "Centers for Disease Control":
            bot.send_message(message.chat.id, "www.cdc.gov/coronavirus/")
        elif message.text == "United States Federal Government":
            bot.send_message(message.chat.id, "https://www.usa.gov/coronavirus")
        elif message.text == "World Health Organization":
            bot.send_message(message.chat.id, "https://www.who.int/home")



        # Советы UA
        elif message.text == "Корисні поради🦇":
            bot.send_message(message.chat.id, "Обери про що бажаєшь дізнатись: ", reply_markup=tips_ua())
        elif message.text == "Симптоми 🔴":
            bot.send_message(message.chat.id,
                             "До найбільш поширених симптомів <b>COVID-19 </b> відносяться:\n\n   🔶  <b> підвищення температури тіла </b> \n\n   🔶  <b> втомлюваність </b>\n\n   🔶  <b> сухий кашель </b>\n\nУ низки пацієнтів можуть відзначатися:\n\n        🔸  <b> різні болі </b>\n\n        🔸  <b> закладеність носа </b>\n\n        🔸  <b> нежить </b>\n\n        🔸  <b> фарингіт </b>\n\n        🔸  <b> діарея </b>\n\nЯк правило, ці симптоми розвиваються поступово і носять слабо виражений характер.\nУ деяких інфікованих осіб не виникає будь-яких симптомів або поганого самопочуття.\nУ більшості людей (близько 80%) хвороба закінчується одужанням, при цьому специфічних лікувальних заходів не потрібно.",
                             parse_mode="html",
                             reply_to_message_id=message.message_id)
        elif message.text == "Я хворий? 💀":
            bot.send_message(message.chat.id,
                             "<b>Маю симптоми COVID-19. Що робити?</b>\n\n1.Залишайтеся вдома.\n\n2.Подзвоніть своєму сімейному лікарю.\n\n3.Опишіть йому симптоми, історію подорожей.\n\nРозкажіть про те, чи були ви в контакті з людьми, які потенційно можуть бути інфіковані.\nРозкажіть про результати опитування, а також уточніть, на які саме запитання Ви дали стверджувальну відповідь.\nВиконуйте інструкції свого лікаря.\n\nУ невідкладних станах — температура вище 38, яка не збивається,та ускладнене дихання — терміново викликайте “швидку” за номером <b>103</b>.\n\nУ разі виникнення запитань — звертайтеся за телефонами:\n\n    ▪  Урядова гаряча лінія:<b>15-45</b>\n    ▪  Гаряча лінія МОЗ:<b>0 800 505 201</b>\n    ▪  Гаряча лінія ЦГЗ: <b>0 800 505 840</b>",
                             parse_mode="html",
                             reply_to_message_id=message.message_id)
        elif message.text == "Профілактика 🔵":
            bot.send_message(message.chat.id,
                             "<b>Як уберегтися? Рекомендації щодо профілактики COVID-19:</b>\n\n   🔹   мити руки з милом понад 20 секунд\n\n   🔹   не торкатися руками очей, носа, рота\n\n   🔹   чхати і кашляти —  у згин ліктя або прикриваючи рот і ніс серветками\n\n   🔹   регулярно провітрювати приміщення;дезінфікувати поверхні\n\n   🔹   дотримуватися дистанції у 1,5 метри з людьми\n\n   🔹   уникати рукостискань, поцілунків, обіймів",
                             parse_mode="html",
                             reply_to_message_id=message.message_id)
        elif message.text == "Як правильно мити руки? 🤲":
            bot.send_video(message.from_user.id,
                           "BAACAgIAAxkBAAPBXpTzBq5LE7jlk_y-B6Zf_gU2e74AApQHAALAwKhI5NuZ4NEadOwYBA",
                           reply_to_message_id=message.message_id)
        # Советы RU
        elif message.text == "Полезные советы🦇":
            bot.send_message(message.chat.id, "Выбери, что тебе интересно: ", reply_markup=tips_ru())
        elif message.text == "Симптомы 🔴":
            bot.send_message(message.chat.id,
                             "К наиболее распространенных симптомам <b> COVID-19 </b> относятся: \n\n   🔹   <b> повышение температуры тела </b>\n\n   🔹   <b> утомляемость </b>\n\n   🔹   <b> сухой кашель </b>\n\nУ ряда пациентов могут отмечаться:\n\n        🔸  <b> различные боли </b>\n\n        🔸  <b> заложенность носа </b>\n\n        🔸  <b> насморк </b>\n\n        🔸  <b> фарингит </b>\n\n        🔸  <b> диарея</b>\n\nКак правило, эти симптомы развиваются постепенно и носят слабо выраженный характер. \nУ некоторых инфицированных лиц не возникает каких-либо симптомов или плохого самочувствия. \nУ большинства людей (около 80%) болезнь заканчивается выздоровлением, при этом специфических лечебных мероприятий не требуется.",
                             parse_mode="html",
                             reply_to_message_id=message.message_id)
        elif message.text == "Я болен? 💀":
            bot.send_message(message.chat.id,
                             "<b> У меня симптомы COVID-19. Что делать? </b> \n\n1.Оставайся дома. \n\n2.Позвонить своему семейному врачу. \n\n3.Опишите ему симптомы, историю путешествий.\n\nРозкажите о том, были ли вы в контакте с людьми, которые могут быть инфицированы. \nРозкажите о результатах опроса, а также уточните, на какие именно вопросы Вы дали утвердительный ответ. \nВыполняйте инструкции врача.\n\nВ неотложных ситуациях - температура выше 38, не сбивается, и затруднено дыхания - срочно вызывайте скорую по телефону <b> 112 </b>. \n\nВ случае возникновения вопросов - обращайтесь по телефону:\n\n ▪ Единая горячая линия: <b> 8-800-2000-112 </b>",
                             parse_mode="html",
                             reply_to_message_id=message.message_id)
        elif message.text == "Профилактика 🔵":
            bot.send_message(message.chat.id,
                             "<b> Как не заразиться? Рекомендации по профилактике COVID-19 </b>\n\n   🔹   мыть руки с мылом более 20 секунд \n\n   🔹   не касаться руками глаз, носа, рта \n\n   🔹   чихать и кашлять - в сгиб локтя или прикрывая рот и нос салфетками \n\n   🔹   регулярно проветривать помещения; дезинфицировать поверхности \n\n   🔹   соблюдать дистанцию в 1,5 метра с людьми \n\n   🔹   избегать рукопожатий, поцелуев, объятий ",
                             parse_mode="html",
                             reply_to_message_id=message.message_id)
        elif message.text == "Как правильно мыть руки? 🤲":
            bot.send_video(message.from_user.id,
                           "BAACAgIAAxkBAAPBXpTzBq5LE7jlk_y-B6Zf_gU2e74AApQHAALAwKhI5NuZ4NEadOwYBA",
                           reply_to_message_id=message.message_id)

        # Советы UK и USA
        elif message.text == "Tips🦇":
            bot.send_message(message.chat.id, "Choose what interests you: ", reply_markup=tips_uk())
        elif message.text == "Tips 🦇":
            bot.send_message(message.chat.id, "Choose what interests you: ", reply_markup=tips_us())
        elif message.text == "Symptoms 🔴":
            bot.send_message(message.chat.id,
                             "The most common <b> COVID-19 </b> symptoms include: \n\n   🔹   <b> fever </b> \n\n   🔹   <b> fatigue </b> \n\n   🔹   <b> dry cough </b> \n\nA number of patients may experience: \n\n        🔸  <b> various pains </b> \n\n        🔸  <b> nasal congestion </b> \n\n        🔸  <b> runny nose </b> \n\n        🔸  <b> pharyngitis </b> \n\n        🔸  <b> diarrhea </b> \n\nAs a rule, these symptoms develop gradually and are mild. \n Some people who are infected do not experience any symptoms or feel unwell. \nIn most people (about 80%), the disease ends in recovery, and no specific treatment is required.",
                             parse_mode="html",
                             reply_to_message_id=message.message_id)
        elif message.text == "I am sick? 💀":
            bot.send_message(message.chat.id,
                             "<b> I have symptoms of COVID-19. What to do? </b> \n\n1.Stay at home. \n\n2.Call your family doctor. \n\n3.Dell him the symptoms, travel history. \n\nTell about whether you have been in contact with people who may be infected. \nTell about the results of the survey, and also specify which questions you gave in the affirmative. \nFollow the instructions of the doctor. \n\nIn urgent situations - the temperature is above 38, does not stray, and breathing is difficult - urgently call an ambulance by phone <b> 112 </b>. \n\n If you have questions, please call: \n\n ▪ Single hotline: <b> 8-800-2000-112 </b>",
                             parse_mode="html",
                             reply_to_message_id=message.message_id)
        elif message.text == "I am Sick? 💀":
            bot.send_message(message.chat.id,
                             "<b> I have symptoms of COVID-19. What to do? </b> \n\n1.Stay at home. \n\n2.Call your family doctor. \n\n3.Dell him the symptoms, travel history. \n\nTell about whether you have been in contact with people who may be infected. \nTell about the results of the survey, and also specify which questions you gave in the affirmative. \nFollow the instructions of the doctor. \n\nIn urgent situations - the temperature is above 38, does not stray, and breathing is difficult - urgently call an ambulance by phone <b> 112 </b>. \n\n If you have questions, please call: \n\n ▪ Helpline: <b> 1-844-872-4681 </b>",
                             parse_mode="html",
                             reply_to_message_id=message.message_id)

        elif message.text == "Prevention 🔵":
            bot.send_message(message.chat.id,
                             "<b> How not to get infected? COVID-19 Prevention Recommendations </b> \n\n   🔹   wash your hands with soap for more than 20 seconds \n\n   🔹   do not touch your eyes, nose, mouth with your hands \n\n   🔹   sneeze and cough - bend your elbow or cover your mouth and nose with napkins \n\n   🔹   regularly air the premises; disinfect surfaces \n\n   🔹   keep a distance of 1.5 meters with people \n\n   🔹   avoid handshakes, kisses, hugs",
                             parse_mode="html",
                             reply_to_message_id=message.message_id)
        elif message.text == "How to wash your hands? 🤲":
            bot.send_video(message.from_user.id,
                           "BAACAgIAAxkBAAPBXpTzBq5LE7jlk_y-B6Zf_gU2e74AApQHAALAwKhI5NuZ4NEadOwYBA",
                           reply_to_message_id=message.message_id)

        # Напоминалка UK
        elif message.text == "Daily notifications⏰":
            if check_user(message):
                bot.send_message(message.chat.id, "You already have a subscription", reply_markup=mail_keyboard_uk())
            else:
                bot.send_message(message.chat.id,
                                 "You have the option to subscribe to daily notifications. \n Every day in the morning you will receive up-to-date statistics \ nby your country and world. \n If you wish, you can unsubscribe at any time by \n clicking on the “unsubscribe” button.",
                                 reply_markup=mail_keyboard_uk())
                bot.send_message(message.chat.id, "\nTo start receiving messages - click “subscribe”.")


        elif message.text == "Subscribe✅":
            if not check_user(message):
                if add_user(message, False, False, True, False):
                    bot.send_message(message.chat.id, "Subscription issued.")
            else:
                bot.send_message(message.chat.id, "You already have a subscription.")
        elif message.text == "Unsubscribe❌":
            if check_user(message):
                if del_user(message):
                    bot.send_message(message.chat.id, "Unsubscribed.")
                else:
                    bot.send_message(message.chat.id, "Failed to cancel. \nTry again.")
            else:
                bot.send_message(message.chat.id, "To cancel a subscription, you first need to subscribe.")

        elif message.text == "back⬅⬅":
            bot.send_message(message.chat.id, "Choose what interests you: ", reply_markup=additional_key_uk())

        # Напоминалка USA
        elif message.text == "Daily notifications ⏰":
            if check_user(message):
                bot.send_message(message.chat.id, "You already have a subscription", reply_markup=mail_keyboard_us())
            else:
                bot.send_message(message.chat.id,
                                 "You have the option to subscribe to daily notifications. \n Every day in the morning you will receive up-to-date statistics \ nby your country and world. \n If you wish, you can unsubscribe at any time by \n clicking on the “unsubscribe” button.",
                                 reply_markup=mail_keyboard_us())
                bot.send_message(message.chat.id, "\nTo start receiving messages - click “subscribe”.")


        elif message.text == "Subscribe ✅":
            if not check_user(message):
                if add_user(message, False, False, True, False):
                    bot.send_message(message.chat.id, "Subscription issued.")
            else:
                bot.send_message(message.chat.id, "You already have a subscription.")
        elif message.text == "Unsubscribe ❌":
            if check_user(message):
                if del_user(message):
                    bot.send_message(message.chat.id, "Unsubscribed.")
                else:
                    bot.send_message(message.chat.id, "Failed to cancel. \nTry again.")
            else:
                bot.send_message(message.chat.id, "To cancel a subscription, you first need to subscribe.")

        elif message.text == "⬅⬅back":
            bot.send_message(message.chat.id, "Choose what interests you: ", reply_markup=additional_key_us())


        # Напоминалка Россия
        elif message.text == "Ежедневные оповещения⏰":
            if check_user(message):
                bot.send_message(message.chat.id, "Вы уже имеете подписку", reply_markup=mail_keyboard_ru())
            else:
                bot.send_message(message.chat.id,
                                 "У вас есть возможность подписаться на ежедневные уведомления. \nКаждый день утром вы будете получать актуальную статистику \nпо своей страны и миру. \nПо желанию, Вы можете в любой момент отменить подписку, \nнажав на кнопку - “отменить подписку”.",
                                 reply_markup=mail_keyboard_ru())
                bot.send_message(message.chat.id, "\nЧтобы начать получать сообщения - нажмите “подписаться”.")


        elif message.text == "Подписаться ✅":
            if not check_user(message):
                if add_user(message, False, True, False, False):
                    bot.send_message(message.chat.id, "Подписка оформлена.")
            else:
                bot.send_message(message.chat.id, "Вы уже имеете подписку")
        elif message.text == "Отменить подписку ❌":
            if check_user(message):
                if del_user(message):
                    bot.send_message(message.chat.id, "Подписку отменено")
                else:
                    bot.send_message(message.chat.id, "Не удалось отменить. \nПопробуйте еще раз.")
            else:
                bot.send_message(message.chat.id, "Чтобы отменить подписку сначала нужно подписаться.")

        elif message.text == "⬅⬅назад":
            bot.send_message(message.chat.id, "Выбери, что тебе интересно:  ", reply_markup=additional_key_ru())

        # Напоминалка Украина
        elif message.text == "Щоденні сповіщення⏰":
            if check_user(message):
                bot.send_message(message.chat.id, "Ви вже маєте підписку", reply_markup=mail_keyboard_ua())
            else:
                bot.send_message(message.chat.id,
                                 "У вас є можливість підписатись на щоденні сповіщення.\nКожного дня вранці ви будете отримувати актуальну статистику\nщодо своєї країни та світу.\nЗа бажанням, Ви можете у будь-який момент скасувати підписку,\nнатиснувши кнопку – “скасувати підписку”.",
                                 reply_markup=mail_keyboard_ua())
                bot.send_message(message.chat.id, "\nЩоб почати отримувати повідомлення -  натисність “підписатись”.")


        elif message.text == "Підписатись ✅":
            if not check_user(message):
                if add_user(message, True, False, False, False):
                    bot.send_message(message.chat.id, "Підписка оформлена.")
            else:
                bot.send_message(message.chat.id, "Ви вже маєте підписку")
        elif message.text == "Скасувати підписку ❌":
            if check_user(message):
                if del_user(message):
                    bot.send_message(message.chat.id, "Підписку скасовано")
                else:
                    bot.send_message(message.chat.id, "Не вдалося скасувати.\nСпробуй ще раз.")
            else:
                bot.send_message(message.chat.id, "Щоб скасувати підписку спочатку потрібно підписатись.")

        elif message.text == "назад⬅⬅":
            bot.send_message(message.chat.id, "Обери про що бажаєшь дізнатись: ", reply_markup=additional_key_ua())

        # Переход ко второму меню
        elif message.text == "далі➡":
            bot.send_sticker(message.chat.id,
                             "CAACAgIAAxkBAAI-l16J15VPAAEzw-sjZFKJD2AHRPxrNgACwgEAAladvQqZeEiAQjhtkBgE")
            bot.send_message(message.chat.id, "Обери про що бажаєшь дізнатись: ", reply_markup=additional_key_ua())
        elif message.text == "➡дальше":
            bot.send_sticker(message.chat.id,
                             "CAACAgIAAxkBAAI-l16J15VPAAEzw-sjZFKJD2AHRPxrNgACwgEAAladvQqZeEiAQjhtkBgE")
            bot.send_message(message.chat.id, "Выбери, что тебе интересно: ", reply_markup=additional_key_ru())
        elif message.text == "next➡":
            bot.send_sticker(message.chat.id,
                             "CAACAgIAAxkBAAI-l16J15VPAAEzw-sjZFKJD2AHRPxrNgACwgEAAladvQqZeEiAQjhtkBgE")
            bot.send_message(message.chat.id, "Choose what interests you: ", reply_markup=additional_key_uk())
        elif message.text == "➡next":
            bot.send_sticker(message.chat.id,
                             "CAACAgIAAxkBAAI-l16J15VPAAEzw-sjZFKJD2AHRPxrNgACwgEAAladvQqZeEiAQjhtkBgE")

            bot.send_message(message.chat.id, "Choose what interests you: ", reply_markup=additional_key_us())


        # Назад к главному меню по каждой стране
        elif message.text == "назад⬅":
            bot.send_message(message.chat.id, "Обери про що бажаєшь дізнатись: ", reply_markup=ua_stat())

        elif message.text == "⬅назад":
            bot.send_message(message.chat.id, "Выбери, что тебе интересно: ", reply_markup=ru_stat())

        elif message.text == "back⬅":
            bot.send_message(message.chat.id, "Choose what interests you: ", reply_markup=uk_stat())

        elif message.text == "⬅back":
            bot.send_message(message.chat.id, "Choose what interests you: ", reply_markup=us_stat())


        # Статистика по вашей стране
        elif message.text == "🇺🇦Статистика по Вашій країні🇺🇦":
            send_stat(message, "Україна")
        elif message.text == "🇷🇺Статистика по Вашей стране🇷🇺":
            send_stat(message, "Россия")
        elif message.text == "🇬🇧Statistics for your country🇬🇧":
            send_stat(message, "UK")
        elif message.text == "🇺🇸Statistics for your country🇺🇸":
            send_stat(message, "USA")

        # Статистика по миру
        elif message.text == "🌎Статистика по світу🌎":
            send_stat(message, "Світ")
        elif message.text == "🌎Статистика по миру🌎":
            send_stat(message, "Мир")
        elif message.text == "🌎World Statistics🌎":
            send_stat(message, "world")

        # ТОП-10 по всему миру
        elif message.text == "TOP-10🇺🇦":
            send_top(message, "ua")
        elif message.text == "TOP-10🇷🇺":
            send_top(message, "ru")
        elif message.text == "TOP-10🇬🇧" or message.text == "TOP-10🇺🇸":
            send_top(message, "en")

        # Статистика по выбранной стране
        elif message.text == "Статистика по обраній країні 📊":
            bot.send_message(message.chat.id, "Введіть назву країни:")
        elif message.text == "Статистика по выбранной стране 📊":
            bot.send_message(message.chat.id, "Введите название страны:")
        elif message.text == "Statistics for the selected country 📊":
            bot.send_message(message.chat.id, "Enter country name:")

        # Старт в зависимости от начальной страны
        elif message.text == "Ukraine 🇺🇦":
            bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAI-k16J1tQeXffFgA40X6eMLWksrGkrAALYAQACVp29CpjUfylnzkA5GAQ")
            bot.send_message(message.chat.id, "Обери про що бажаєшь дізнатись: ", reply_markup=ua_stat())

        elif message.text == "Russia 🇷🇺":
            bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAI-k16J1tQeXffFgA40X6eMLWksrGkrAALYAQACVp29CpjUfylnzkA5GAQ")

            bot.send_message(message.chat.id, "Выбери, что тебе интересно: ", reply_markup=ru_stat())

        elif message.text == "UK🇬🇧":
            bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAI-k16J1tQeXffFgA40X6eMLWksrGkrAALYAQACVp29CpjUfylnzkA5GAQ")

            bot.send_message(message.chat.id, "Choose what interests you: ", reply_markup=uk_stat())

        elif message.text == "USA🇺🇸":
            bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAI-k16J1tQeXffFgA40X6eMLWksrGkrAALYAQACVp29CpjUfylnzkA5GAQ")

            bot.send_message(message.chat.id, "Choose what interests you: ", reply_markup=us_stat())
        # Если ни одна команда не подошла, автоматически создается поиск по стране(введенному сообщению)
        else:
            if text_has_emoji(message.text):
                bot.send_message(message.chat.id,
                                 "Your message should not contain emoticons.\nТвоє повідомлення не повинно містити смайли.")
                return False

            if message.text == message.text.upper():
                send_stat(message, message.text)
            else:
                message.text = message.text.strip().title()
                if message.text == "South Korea":
                    send_stat(message, "S. Korea")
                elif message.text == "United Kingdom":
                    send_stat(message, "UK")
                else:
                    send_stat(message, message.text)

    bot.polling(none_stop=True)


t1 = threading.Thread(target=check_update)
t2 = threading.Thread(target=bot)
init_db()
t1.start()
t2.start()
