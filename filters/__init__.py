from aiogram import Dispatcher

from loader import dp
from .isJoined import IsJoined


if __name__ == "filters":
    dp.filters_factory.bind(IsJoined)
    pass
