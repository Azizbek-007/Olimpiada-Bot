from aiogram import types
from loader import dp, bot_id, admins
from aiogram.dispatcher.storage import FSMContext
from states import StateCreateOlimpiada, StateSendMessage, StateChannelAdd, StateRank
from keyboards.inline import admin_btn, cancel_btn, olimpiada_set_btn, olimpiada_list_btn, delete_channel_btn
from utils.db_api import db, DBS
import re
import asyncio

@dp.message_handler(commands=['admin'], user_id=admins)
async def admin_hello(msg: types.Message):
    await msg.answer("Admin sazlamaları.", reply_markup=admin_btn)

@dp.callback_query_handler(text="cancel", state="*")
async def bot_cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer("Cancel")
    
@dp.callback_query_handler(text="ExportRegistedUsers")
async def exportRegistedUsers(call: types.CallbackQuery):
    try:
        DBS.get_registed_users(DBS)
        await call.answer()
        await call.message.answer_document(open('./registedUsers.xlsx', 'rb'))
    except: await call.answer("Maglumat tabilmadi", True)

@dp.callback_query_handler(text="createOlimpiada")
async def create_olimpiada_func(call: types.CallbackQuery):
    await call.answer()
    await StateCreateOlimpiada.name.set()
    await call.message.answer("Olimpiada atın kiritiń.", reply_markup=cancel_btn)

@dp.message_handler(state=StateCreateOlimpiada.name)
async def set_olimpiada_name(msg:  types.Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await StateCreateOlimpiada.answer.set()
    await msg.answer("Olimpiada juwapların kiritiń.", reply_markup=cancel_btn)


@dp.message_handler(state=StateCreateOlimpiada.answer)
async def set_olimpiada_answer(msg:  types.Message, state: FSMContext):
    await state.update_data(answer=msg.text)
    await StateCreateOlimpiada.start.set()
    await msg.answer("Olimpiada baslanıw waqtın kiritiń.\njıl-ay-kún saat-minut\nÚlgi: 2022-12-20 12:00", reply_markup=cancel_btn)

@dp.message_handler(state=StateCreateOlimpiada.start)
async def set_olimpiada_start_date(msg: types.Message, state: FSMContext):
    regex = "^\d{4}-[0-1][0-2]-[0-3]\d\s([0-1][0-9]|2[0-3]):[0-5]{2}"
    if re.search(regex, msg.text):
        await state.update_data(start_date=msg.text)
        await StateCreateOlimpiada.end.set()
        await msg.answer("Olimpiada tamamlaniw waqtin kiritin':", reply_markup=cancel_btn)
    else: await msg.answer("Waqitti qa'te kiritin'iz!\njıl-ay-kún saat-minut\nÚlgi: 2022-12-20 12:00")

@dp.message_handler(state=StateCreateOlimpiada.end)
async def set_olimpiada_start_date(msg: types.Message, state: FSMContext):
    regex = "^\d{4}-[0-1][0-2]-[0-3]\d\s([0-1][0-9]|2[0-3]):[0-5]{2}"
    if re.search(regex, msg.text):
        await state.update_data(end_date=msg.text)
        data = await state.get_data()
        await msg.answer(
                f"<b>Olimpiada ati:</b> {data['name']}\n\n"
                f"<b>Juwaplar:</b> {data['answer']}\n\n"
                f"<b>baslaniw waqti:</b> {data['start_date']}\n\n"
                f"<b>juwmaqlaniw waqti:</b> {data['end_date']}",
                reply_markup=olimpiada_set_btn
                )
    else: await msg.answer("Waqitti qa'te kiritin'iz!\njıl-ay-kún saat-minut\nÚlgi: 2022-12-20 12:00")

@dp.callback_query_handler(text="startOlimpiada", state="*")
async def start_Set_Olimpiada(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    DBS._set_olimpiada(DBS, name=data['name'], answer=data['answer'], start=data['start_date'], end=data['end_date'])
    await call.message.delete()
    await call.message.answer("Olimpiada qosildi")
    await state.finish()

@dp.callback_query_handler(lambda call: 'delete=' in call.data)
async def _delete_Olimpiada(call: types.CallbackQuery, state: FSMContext):
    _id = str(call.data).split('=')[1]
    DBS.delete_olimpiada(DBS, olimpiada_id=_id)
    OlimpList = DBS.get_olimpiada(DBS)
    await call.answer("deleted")
    await call.message.edit_text("Olimpiada list", reply_markup=olimpiada_list_btn(OlimpList))

@dp.callback_query_handler(text="deleteOlimpiada")
async def delete_a_olimpiada(call: types.CallbackQuery):
    await call.answer("hi")
    OlimpList = DBS.get_olimpiada(DBS)
    await call.message.answer("Olimpiada list", reply_markup=olimpiada_list_btn(OlimpList))

@dp.callback_query_handler(text="sendMessage")
async def bot_all_sen_message(call: types.CallbackQuery):
    await StateSendMessage.promis.set()
    await call.message.answer("send me a message", reply_markup=cancel_btn)

@dp.message_handler(state=StateSendMessage.promis ,content_types=types.ContentTypes.ANY)
async def promis_send_all_message(msg: types.Message, state: FSMContext):
    await state.finish()
    s, y = 0, 0
    for x in DBS.user_list(DBS):
        try:
            await msg.copy_to(x[0])
            s += 1 
            await asyncio.sleep(.7)
        except:
            y += 1
    await msg.answer(f"Jiberildi: {s} users\nJiberilmedi: {y} users")

@dp.callback_query_handler(text='GetRank')
async def xsl_down_send_promis(call: types.CallbackQuery):
    await StateRank.promis.set()
    await call.message.answer("Olimpiada kodin jiberin':", reply_markup=cancel_btn)

@dp.message_handler(regexp="^[0-9]+$", state=StateRank.promis)
async def xsl_dowload_func(msg: types.Message, state: FSMContext):
    try:
        if DBS.get_xls(DBS, msg.text) == False: 
            await msg.reply("Olimpiada tabilmadi")
        else: await msg.answer_document(open('./rank.xlsx', 'rb'))
    except Exception as e:
        await msg.answer(e)
    await state.finish()


@dp.callback_query_handler(text="addChannel")
async def bot_add_channel_procces(call: types.CallbackQuery):
    await StateChannelAdd.promis.set()
    await call.message.answer("Kanaldan forward qilip xabr jiberin....", reply_markup=cancel_btn)

@dp.message_handler(state=StateChannelAdd.promis, content_types=types.ContentTypes.ANY)
async def bot_is_forward(msg: types.Message, state: FSMContext):
    try:
        print('ok')
        channel = msg.forward_from_chat
        if channel.type == "channel":
            get = await dp.bot.get_chat_member(channel.id, bot_id)
            if get.status == 'administrator':
                create_link = await dp.bot.create_chat_invite_link(channel.id)
                link = create_link.invite_link
                DBS._set_new_channel(DBS, channel.id, link)
                await msg.answer("Kanal qosildi")
            else: await msg.answer("Bot kanalg'a admin bolmag'an")
        else: await msg.answer("Botqa tek kanal qosa alasiz")
    except: await msg.answer("Kanaldan forward qilip xabr jiberin....")
    await state.finish()

@dp.callback_query_handler(text="deleteChannel")
async def deleteChannel(call: types.CallbackQuery):
    await call.message.answer("Kanallar", reply_markup=delete_channel_btn())

@dp.callback_query_handler(lambda call: call.data.startswith("ChannelDelete="))
async def delete_channel_pr(call: types.CallbackQuery):
    channel_id = str(call.data).split('=')[1]
    await call.answer(channel_id)
    DBS._delete_channel(DBS, channel_id)
    await call.message.edit_text("Kanallar", reply_markup=delete_channel_btn())