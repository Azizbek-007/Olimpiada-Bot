from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from lang.message import lang
from utils.db_api import DBS

def ifo_btn(user_lang):
    text = lang.get("lang_btn").get(user_lang)
    return InlineKeyboardMarkup().add(
    InlineKeyboardButton(text="Qaraqalpaq tili", callback_data="lang=qq"),
    InlineKeyboardButton(text="Русский", callback_data="lang=ru")
    ).add(InlineKeyboardButton(text=text[2], callback_data="EDITIFO"))
    
lang_btn = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text="Qaraqalpaq tili", callback_data="lang=qq"),
    InlineKeyboardButton(text="Русский", callback_data="lang=ru")
    )

admin_btn = InlineKeyboardMarkup().add(
    InlineKeyboardButton("Olimpiada jaratıw", callback_data="createOlimpiada"),
    InlineKeyboardButton("Olimpiadanı óshiriw", callback_data="deleteOlimpiada"),
    ).add(
        InlineKeyboardButton("Kanal usınıs etiw", callback_data="addChannel"),
         InlineKeyboardButton("Kanaldı óshiriw", callback_data="deleteChannel")
    ).add(
        InlineKeyboardButton("Paydalanıwshılarǵa xabar jiberiw", callback_data="sendMessage")
    ).add(
        InlineKeyboardButton("Nátiyjelerdi alıw", callback_data="GetRank"),
        InlineKeyboardButton("Dizimnen o'tkenlerdi aliw", callback_data="ExportRegistedUsers")
    )

cancel_btn = InlineKeyboardMarkup().add(
    InlineKeyboardButton("Biykarlaw", callback_data="cancel")
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

def delete_channel_btn():
    markup = InlineKeyboardMarkup()
    i = 1
    for x in DBS._get_channels(DBS):
        markup.add(InlineKeyboardButton(f"{i}-kanal", url=x[1]), InlineKeyboardButton("🗑", callback_data=f"ChannelDelete={x[0]}"))
        i +=1
    return markup