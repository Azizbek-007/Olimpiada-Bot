from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lang.message import lang
def register_btn():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("Ro‘yxatdan o‘tish")
    )

def olimpiada_btn(user_lang):
    text = lang.get("menu").get(user_lang)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    a = []
    for i in text:
        a.append(
        KeyboardButton(i))
    return markup.add(*a)
    