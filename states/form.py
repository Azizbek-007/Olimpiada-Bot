from aiogram.dispatcher.filters.state import StatesGroup, State

class StateRegister(StatesGroup):
    fullname = State()

class StateCreateOlimpiada(StatesGroup):
    name = State()
    answer = State()
    start = State()
    end = State()

class StateSendMessage(StatesGroup):
    promis = State()

class StateChannelAdd(StatesGroup):
    promis = State()

class StateRank(StatesGroup):
    promis = State()