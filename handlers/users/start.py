from builtins import float
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.storage import FSMContext
from keyboards.default import register_btn
from loader import dp
from states import StateRegister
from utils.db_api import db, DBS
from keyboards.inline import lang_btn, channels_btn, ifo_btn
from keyboards.default import olimpiada_btn
from lang.message import lang
from filters import IsJoined, Is_Joined


@dp.callback_query_handler(Is_Joined(), text='channelCheck', state='*')
async def check_joined(call: types.CallbackQuery):
    UserLang = DBS.user_lang(DBS, call.from_user.id)
    await call.answer(lang.get("no_join").get(UserLang))

@dp.callback_query_handler(text='channelCheck', state='*')
async def check_joined(call: types.CallbackQuery):
    await call.message.delete()
    UserLang = DBS.user_lang(DBS, call.from_user.id)
    if UserLang:
        await call.message.answer(
                "menu",
                reply_markup=olimpiada_btn(UserLang))
    else: 
        await call.message.answer(
                "Выберите язык, который вам удобен:",
                reply_markup=lang_btn)

@dp.message_handler(IsJoined(), content_types=types.ContentTypes.ANY, state='*')
async def check_channel_join(msg: types.Message):
    DBS.register_user(DBS, user=msg.from_id, username=msg.from_user.username,
        first_name=msg.from_user.first_name, last_name=msg.from_user.last_name)
    UserLang = DBS.user_lang(DBS, msg.from_id)
    if UserLang:
        await msg.answer(lang.get("join").get(UserLang), reply_markup=channels_btn())
    else:
        await msg.answer(
                "Выберите язык, который вам удобен:",
                reply_markup=lang_btn)

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    DBS.register_user(DBS, user=message.from_id, username=message.from_user.username,
        first_name=message.from_user.first_name, last_name=message.from_user.last_name)
    UserLang = DBS.user_lang(DBS, message.from_id)
    if UserLang:
        await message.answer(
                "menu",
                reply_markup=olimpiada_btn(UserLang))
    else: 
        await message.answer(
                "Выберите язык, который вам удобен:",
                reply_markup=lang_btn)

@dp.message_handler(lambda msg: msg.text == lang.get("menu").get(DBS.user_lang(DBS, msg.from_id))[0])
async def olimpiada_list(msg: types.Message):
    UserLang = DBS.user_lang(DBS, msg.from_id)
    try:
        _list = DBS.get_olimpiada(DBS)
        text, i = "", 1
        for x in _list:
            print(x)
            text += lang.get("olimpiada_list_text").get(UserLang).format(x[1], x[3], x[5], x[4], x[6], x[0])
            i +=1
        await msg.reply(text)
    
    except: 
        await msg.reply(lang.get("no_olimpiada").get(UserLang))

@dp.message_handler(lambda msg: msg.text == lang.get("menu").get(DBS.user_lang(DBS, msg.from_id))[1])
async def lang_setting(msg: types.Message):
    UserLang = DBS.user_lang(DBS, msg.from_id)
    await msg.answer(lang.get("select_lang").get(UserLang), reply_markup=ifo_btn(UserLang))
    

@dp.message_handler(lambda msg: DBS.user_lang(DBS, msg.from_id) == False)
async def _set_lang(msg: types.Message):
     await msg.reply(
                "Выберите язык, который вам удобен:",
                reply_markup=lang_btn)

@dp.message_handler(lambda msg: msg.text == lang.get("register_btn").get(DBS.user_lang(DBS, msg.from_id)))
async def user_register(msg: types.Message):
    UserLang = DBS.user_lang(DBS, msg.from_id)
    await msg.answer(lang.get("register_exsample").get(UserLang))
    await StateRegister.next()

@dp.message_handler(lambda msg: DBS.user_fullname(DBS, msg.from_id) == False)
async def _set_lang(msg: types.Message):
    UserLang = DBS.user_lang(DBS, msg.from_id)
    await msg.answer(
                lang.get("register").get(UserLang),
                reply_markup=register_btn())

@dp.callback_query_handler(text="EDITIFO")
async def update_user_ifo(call: types.CallbackQuery):
    await StateRegister.next()
    UserLang = DBS.user_lang(DBS, call.from_user.id)
    await call.message.answer(lang.get("register_example").get(UserLang))

@dp.callback_query_handler(lambda callback: 'lang=' in callback.data)
async def SetUserLang(callback: types.CallbackQuery):
    UserLang = str(callback.data).split("=")[1]
    DBS.set_user_lang(DBS, user_id=callback.from_user.id, lang=UserLang)
    await callback.message.delete()
    await callback.message.answer("menu", reply_markup=olimpiada_btn(UserLang))


@dp.message_handler(state=StateRegister.fullname)
async def set_fullname(msg: types.Message, state: FSMContext):
    UserLang = DBS.user_lang(DBS, msg.from_id)
    if len(msg.text.split(' ')) == 2:
        DBS.set_user_fullname(DBS, msg.from_id, msg.text)
        await msg.answer(lang.get("insterted_fullname").get(UserLang).format(msg.text), reply_markup=olimpiada_btn(UserLang))
        await state.finish()
    else: await msg.reply(lang.get("register_example").get(UserLang))


@dp.message_handler(regexp="[0-9]+[*][a-z]+$")
async def me_send_answers(msg: types.Message):
    check_date = DBS._start_user_olimpiada(DBS)
    UserLang = DBS.user_lang(DBS, msg.from_id)
    if check_date == []: 
        await msg.reply(lang.get("not_started").get(UserLang))
    else:
        text, check, i, t = msg.text.split('*'), "", 0, 0
        if DBS._check_rank(DBS, msg.from_id, text[0]) == False:
            await msg.reply(lang.get("isset_olipada").get(UserLang))
        else:
            try:     
                Olimpiada = DBS.ByOlimpiada(DBS, text[0])
                print(Olimpiada)
                for x in Olimpiada[0][2]:
                    try:
                        if str(text[1][i]).upper() == str(x).upper():
                            i +=1
                            t +=1
                            check += f"{i}) ✅\t\t"
                        else: 
                            i +=1
                            check += f"{i}) ❌\t\t"
                    except Exception as e:
                        i +=1
                        check += f"{i}) ❌\t\t"
                    if i % 3 == 0: 
                        check +="\n" 
                    
                procent = round(((t * 100)/i), 2)
                DBS._set_rank(DBS, msg.from_id, Olimpiada[0][0], procent)
                await msg.answer(f"{check}\n<b>{Olimpiada[0][1]}</b>\nprocent: <b>{procent}%</b>")    
            except: await msg.reply(lang.get("no_olimpiada").get(UserLang))
