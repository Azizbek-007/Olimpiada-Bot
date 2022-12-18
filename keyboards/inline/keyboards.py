from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from lang.message import lang
from utils.db_api import DBS

lang_btn = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text="Qaraqalpaq tili", callback_data="lang=qq"),
    InlineKeyboardButton(text="Русский", callback_data="lang=ru")
    ).add(
    InlineKeyboardButton(text="Edit IFO", callback_data="EDITIFO")
    )

admin_btn = InlineKeyboardMarkup().add(
    InlineKeyboardButton("Create Olimpiada", callback_data="createOlimpiada"),
    InlineKeyboardButton("Delete Olimpiada", callback_data="deleteOlimpiada"),
    ).add(
        InlineKeyboardButton("Add Channel", callback_data="addChannel"),
         InlineKeyboardButton("Delete Channel", callback_data="deleteChannel")
    ).add(
        InlineKeyboardButton("Send Message", callback_data="sendMessage")
    ).add(
        InlineKeyboardButton("Get Rank", callback_data="GetRank")
    )
cancel_btn = InlineKeyboardMarkup().add(
    InlineKeyboardButton("cancel", callback_data="cancel")
    )

olimpiada_set_btn = InlineKeyboardMarkup().add(
    InlineKeyboardButton("✅ Baslaw", callback_data="startOlimpiada")
    ).add(
    InlineKeyboardButton("🗑 Biykar etiw", callback_data="cancel")
    )

def olimpiada_list_btn(OlimpList): 
    markup = InlineKeyboardMarkup()
    for x in OlimpList:
        markup.add(InlineKeyboardButton(x[1], callback_data=x[0]), InlineKeyboardButton("🗑 Delete", callback_data=f'delete={x[0]}'))
    return markup

def channels_btn():
    markup = InlineKeyboardMarkup()
    i = 1
    for x in DBS._get_channels(DBS):
        markup.add(InlineKeyboardButton(f"{i}-kanal", url=x[1]))
        i +=1
    markup.add(InlineKeyboardButton("✅ Ag'za boldim", callback_data="channelCheck"))
    return markup
