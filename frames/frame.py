from collections.abc import Callable

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Filter, StateFilter
from aiogram.types import CallbackQuery
from aiogram.types import Message


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
    def __init__(self, keyboard, text, frame_custom_handler: Callable=None, buttons_generation_func: Callable=None):
        if
        self.keyboard = keyboard
        self.text = text
        self.frame_custom_handler = frame_custom_handler
        self.buttons_generation_func = buttons_generation_func

    def to_send(self):
        return {'reply_markup': self.keyboard, 'text': self.text}

    def

    def generate_message(self):
        Message(text=self.text, reply_markup=self.keyboard)


class FrameManager:
    dp: Dispatcher = Dispatcher()
    def __init__(self, bot: Bot, states: StatesGroup, context: FSMContext):
        # Реализовать паттерн state
        self.bot = bot
        self.current_state: int = 0     # Текущий стейт (его индекс)
        self.states = [state for state in states.__all_states_names__]  # Текстовый группы стейтов
        self.frames = dict()
        self.context = context

    def add_frame(self, text, keyboard, state_key: str):
        if state_key in self.states:
            self.frames[state_key] = Frame(text, keyboard)

    @dp.callback_query()    # 'key'=value
    async def handle_event(self, callback_query: CallbackQuery, state: FSMContext):
        await state.update_data(**{self.states[self.current_state]: callback_query.data})

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

