from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Filter, StateFilter
from aiogram.types import CallbackQuery


class MyFilter(Filter):
    def __init__(self, states: StatesGroup, all_filters):
        pass

    def __call__(self, *args, **kwargs):
        return True


class TestStates(StatesGroup):
    city = State()
    district = State()
    price = State()


class Frame:
    def __init__(self, buttons, filters, text):
        pass


class FrameManager:
    dp: Dispatcher = Dispatcher()
    def __init__(self, bot: Bot, states: StatesGroup, context: FSMContext):
        # Реализовать паттерн state
        self.bot = bot
        self.current_state = []     # стек. Тут отлов первого и последнего стейта
        self.states = {state: {'buttons': None, 'text': None}   # Проверить нужны ли фильтры
                       for state in states.__all_states_names__}
        self.context = context

    @dp.callback_query()
    def handle_event(self, callback_query: CallbackQuery, state: FSMContext):
        pass

    @dp.callback_query(F.data == 'next')
    async def next(self, callback_query: CallbackQuery, state: FSMContext):
        self.current_state # увеличить стек
        await self.generate_frame()

    @dp.callback_query(F.data == 'prev')
    async def prev(self, callback_query: CallbackQuery, state: FSMContext):
        self.current_state # уменьшить стек
        await self.generate_frame()

    async def generate_frame(self):
        self.current_state[-1]
        # дальнейшая отправка сообщения

