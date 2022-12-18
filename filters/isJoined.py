from aiogram import types
from loader import dp
from aiogram.dispatcher.filters import BoundFilter
from utils.db_api import DBS
class IsJoined(BoundFilter):

    async def check(self, message: types.Message) -> bool:
        for x in DBS._get_channels(DBS):
           get = await dp.bot.get_chat_member(x[0], message.from_id)
           if get.status == "left": return True
        
        
       
class Is_Joined(BoundFilter):

    async def check(self, call: types.CallbackQuery) -> bool:
        for x in DBS._get_channels(DBS):
           get = await dp.bot.get_chat_member(x[0], call.from_user.id)
           if get.status == "left": return True