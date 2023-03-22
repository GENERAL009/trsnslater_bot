from telebot import TeleBot
from telebot.types import Message
from googletrans import Translator
from telebot.types import ReplyKeyboardRemove

from configs import *
from keyboard import *
from queries import *
# from queries import insert_translate_history, select_history

bot = TeleBot(token=TOKEN, parse_mode='HTML')


@bot.message_handler(commands=['start', 'history', 'about_dev'])
def command_start(message: Message):
    user_id = message.from_user.id
    if message.text == '/start':
        full_name = message.from_user.full_name
        print(f'someones name: {full_name}')
        print(f'someonse user id: {user_id}')
        bot.send_message(user_id, f"""Welcome to our telegram bot respected <i>{full_name}</i> 😎""")
        # bot.send_message(CHANEL_id, f"""Welcome to our telegram bot respected <i>{full_name}</i> 😎""")
        bot.send_sticker(user_id, 'CAACAgIAAxkBAAEGEYdjRwT-apkdpItqhhMW0g8xqpmg4wACNhYAAnJroEul2k1dhz9kKSoE')
        ask_first_language(message)
    elif message.text == '/history':
        show_history(message)
    elif message.text == '/about_dev':
        bot.send_message(user_id, f"""This bot created by t.me/Sa1ntGENERAL""")
        ask_first_language(message)


def show_history(message: Message):
    user_id = message.from_user.id
    full_name1 = message.from_user.full_name
    translates = select_history(user_id)
    # print(translates)

    for tr in translates[:-6:-1]:
        bot.send_message(user_id, f"""
<b>From language:</b> {tr[0]}
<b>To language:</b> {tr[1]}
<b>Original text:</b> {tr[2]}
<b>Translated text:</b> {tr[3]}
""")
#     for tr1 in translates[:-6:-1]:
#         bot.send_message(CHANEL_id, f"""Thats <i>{full_name1}<i> stories
# <b>From language:</b> {tr1[0]}
# <b>To language:</b> {tr1[1]}
# <b>Original text:</b> {tr1[2]}
# <b>Translated text:</b> {tr1[3]}
# """)

    ask_first_language(message)


def ask_first_language(message: Message):
    user_id = message.from_user.id
    msg = bot.send_message(user_id,
                           f"""Please choose <b>from which</b> language do you want to translate ?""",
                           reply_markup=generate_languages())

    bot.register_next_step_handler(msg, ask_second_language)


def ask_second_language(message: Message):
    if message.text in ['/start', '/history', '/about_dev']:
        command_start(message)
    else:
        user_id = message.from_user.id
        first_language = message.text
        # print(first_language)
        msg = bot.send_message(user_id,
                               f"""Please choose <b>to which</b> language do you want to translate ?""",
                               reply_markup=generate_languages())
        bot.register_next_step_handler(msg, ask_text, first_language)


def ask_text(message: Message, first_language):
    if message.text in ['/start', '/history', '/about_dev']:
        command_start(message)
    else:
        user_id = message.from_user.id
        # print(first_language)
        second_language = message.text
        # print(second_language)
        msg = bot.send_message(user_id,
                               f"""Please write your <b>text or words</b>: """,
                               reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, translate, first_language, second_language)


def translate(message: Message, first_language, second_language):
    if message.text in ['/start', '/history', '/about_dev']:
        command_start(message)
    else:
        user_id = message.from_user.id
        original_text = message.text
        translator = Translator()
        # English 🇬🇧  # ['English', '🇬🇧']
        translated_text = translator.translate(src=first_language.split(' ')[0],
                                               dest=second_language.split(' ')[0],
                                               text=original_text).text
        result = len(original_text.split())

        # print("There are " + str(result) + " words.")
        bot.send_message(user_id, translated_text)
        bot.send_message(user_id, f"✅There are only ✅ (" + str(result) + ") ✅words.✅")

        insert_translate_history(telegram_id=user_id,
                                 src=first_language,
                                 dest=second_language,
                                 org_text=original_text,
                                 tr_text=translated_text)

        ask_first_language(message)


bot.polling(none_stop=True)





