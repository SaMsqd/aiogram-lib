from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Filter, StateFilter


class MyFilter(Filter):
    def __init__(self, states: StatesGroup, all_filters):
        pass

    def __call__(self, *args, **kwargs):
        return True


class TestStates(StatesGroup):
    first = State()
    second = State()
    third = State()


class FrameManager:
    def __init__(self, bot: Bot, dp: Dispatcher, states: StatesGroup, context: FSMContext):
        self.bot = bot
        self.dispatcher = dp
        self.states = {i: {'state': state, 'buttons': None, 'filters': None, 'text': None}
                       for i, state in enumerate(states.__all_states_names__)}
        self.context = context
