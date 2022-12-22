from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lang.message import lang

def register_btn(user_lang):
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton(lang.get("register_btn").get(user_lang))
    )

def olimpiada_btn(user_lang):
    text = lang.get("menu").get(user_lang)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    a = []
    for i in text:
        a.append(
        KeyboardButton(i))
    return markup.add(*a)
    