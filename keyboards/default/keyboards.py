from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def register_btn():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("Ro‘yxatdan o‘tish")
    )

def olimpiada_btn():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("Olimpiadalar dizimi"),
        KeyboardButton("Til nastroykası")
    )