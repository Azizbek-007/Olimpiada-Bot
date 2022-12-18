from aiogram import Dispatcher

from loader import dp
from .isJoined import IsJoined, Is_Joined


if __name__ == "filters":
    dp.filters_factory.bind(IsJoined)
    dp.filters_factory.bind(Is_Joined)
    pass
