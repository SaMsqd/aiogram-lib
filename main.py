from aiogram import Dispatcher, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from aiogram.fsm.state import StatesGroup, State

from frames import *


class TestStates(StatesGroup):
    city = State()
    price = State()
    district = State()
    test = State()


async def buttons_generator(**kwargs):
    """ В зависимости от города возвращаю разные данные"""
    data = await kwargs.get('state').get_data()
    res = {}
    if data['city'] == 'Москва':
        res['buttons'] = ['Московский район 1', 'Московский район 2', 'Московский район 3']
    if data['city'] == 'Питер':
        res['buttons'] = ['Питерский район 1', 'Питерский район 2', 'Питерский район 3']
    if data['city'] == 'Ростов':
        res['buttons'] = ['Ростовский район 1', 'Ростовский район 2', 'Ростовский район 3']

    return res | {'move_forward': True, 'move_back': True}


async def print_state(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer(text='последний frame')
    print(await state.get_data())


fr = [
    FrameModel(text='Выберите свой город', buttons=['Москва', 'Питер', 'Ростов']),
    FrameModel(text='Выберите цену', buttons=['30.000-40.000', '40.000-50.000', '50.000-60.000']),
    FrameModel(text='Выберите район', buttons_generator=buttons_generator),
    FrameModel(text='Ещё какая-то тестовая тема', buttons=['1', '2', '3'], custom_handler=print_state),
]

fm = FrameManager(TestStates(), frames=fr, is_start_route=True)
dp = Dispatcher()
dp.include_router(fm.router)
print('бот запущен')
dp.run_polling(Bot('7640053974:AAGIJKrJGDz0FazV-_-nv7aIB_JEP5_bM4s'))
