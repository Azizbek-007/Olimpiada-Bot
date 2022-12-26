from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data import config

admins = [1750889783, 663946357, 1872428199, 1748582267]
token = str(config.BOT_TOKEN)
bot_id = token.split(':')[0]
bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
