from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State

from ..keyboards.keyboard import KeyboardsCreator
from ..keyboards.models import ButtonModel
from .models import FrameModel


class Frame:
    def __init__(self, text: str, buttons: list[str], state: str, **kwargs):
        """
        :param text:
        :param buttons:
        :param kwargs: тут могут быть ключи:
        cstm_back_btn , cstm_frwd_btn, buttons_generator: Callable, custom_handler: Callable,
        move_forward, move_back
        """
        self.text = text
        self.custom_handler = kwargs.get('custom_handler')
        if kwargs.get('image'): self.image = kwargs.get('image')

        if kwargs.get('save_answer'): self.save_answer = kwargs.get('save_answer')

        if not kwargs.get('buttons_generator'): self.keyboard = self.generate_keyboard(buttons, state, **kwargs)
        else:
            self.state = state
            self.buttons_generator = kwargs.get('buttons_generator')

    def generate_keyboard(self, buttons, state, **kwargs):
        l = list()
        for button in buttons:
            l.append(ButtonModel(
                text=str(button), type='inline',
                ))
        if kwargs.get('move_back'):
            if kwargs.get('cstm_back_btn'):
                l.append(ButtonModel(text=kwargs.get('cstm_back_btn'),
                                     type='inline',
                                     move_back=True))
            else:
                l.append(ButtonModel(text='Назад', type='inline',
                                     move_back=True))
        if kwargs.get('move_forward'):
            if kwargs.get('cstm_frwd_btn'):
                l.append(ButtonModel(text=kwargs.get('cstm_frwd_btn'),
                                     type='inline',
                                     move_forward=True))
            else:
                l.append(ButtonModel(text='Далее', type='inline',
                                 move_forward=True))
        res = KeyboardsCreator.get_keyboard(keyboard_type='inline', row_width=2,
                                                      buttons=l, state_group_state=state)
        return res

    async def get_for_send(self, **kwargs):
        res = {}
        if self.image:
            res |= {'photo': self.image, 'caption': self.text}
        if hasattr(self, 'keyboard'): return res | {'text': self.text, 'reply_markup': self.keyboard}
        else: return res | {'text': self.text, 'reply_markup': self.generate_keyboard(state=self.state,
                                                                              **(await self.buttons_generator(**kwargs)),
                                                                                    )}

class FrameManager:
    router: Router
    def __init__(self, states: StatesGroup, frames: list[FrameModel], is_start_route=False):
        self.router = Router(name=StatesGroup.__name__)
        self.states = self.generate_frames(states, frames)
        self.register(is_start_route)
        print(f'frames registered, router {StatesGroup.__name__} is ready to work')

    def generate_frames(self, states, frames):
        res = dict()
        states_len = len(states.__states__)
        for i in range(len(states.__states__)):
            frame = frames[i].model_dump()
            if frame['move_forward'] is None and i < states_len - 1:
                frame['cstm_frwd_btn'] = 'Далее' if frame['cstm_frwd_btn'] is None else frame['cstm_frwd_btn']
                frame['move_forward'] = True
            if frame['move_back'] is None and i > 0:
                frame['cstm_back_btn'] = 'Назад' if frame['cstm_back_btn'] is None else frame['cstm_back_btn']
                frame['move_back'] = True

            res[i] = [states.__states__[i], Frame(**frame, state=states.__all_states_names__[i])]
        return res

    def register(self, is_start_route):
        if is_start_route:
            @self.router.message(Command('start'))
            async def start(message: Message, state: FSMContext):
                await state.update_data(current_state=0)
                current_state = 0
                await state.set_state(self.states[current_state][0])
                frame = self.states[current_state][1]
                if frame.image: await message.answer_photo(**(await frame.get_for_send()), parse_mode='HTML')

                else: await message.answer(**(await frame.get_for_send()), parse_mode='HTML')

        @self.router.callback_query(F.data.split(':')[-1] == 'forward')
        async def forward(callback_query: CallbackQuery, state: FSMContext):
            current_state = (await state.get_data()).get('current_state') + 1
            await state.update_data(current_state=current_state)
            await state.set_state(self.states[current_state][0])
            frame = self.states[current_state][1]
            if frame.image: await callback_query.message.answer_photo(**(await frame.get_for_send()), parse_mode='HTML')

            else: await callback_query.message.answer(**(await frame.get_for_send()), parse_mode='HTML')

        @self.router.callback_query(F.data.split(':')[-1] == 'back')
        async def back(callback_query: CallbackQuery, state: FSMContext):
            current_state = (await state.get_data()).get('current_state') - 1
            await state.update_data(current_state=current_state)
            await state.set_state(self.states[current_state][0])
            frame = self.states[current_state][1]
            if frame.image: await callback_query.message.answer_photo(**(await frame.get_for_send()), parse_mode='HTML')

            else: await callback_query.message.answer(**(await frame.get_for_send()), parse_mode='HTML')

        for index in self.states:
            @self.router.callback_query(self.states[index][0])
            async def handle_event(callback_query: CallbackQuery, state: FSMContext):
                current_state = (await state.get_data()).get('current_state')
                if self.states[current_state][1].custom_handler:
                    await self.states[current_state][1].custom_handler(callback_query, state)

                else:
                    frame = self.states[current_state][1]
                    if frame.save_answer: await state.update_data(**{callback_query.data.split(':')[1]: callback_query.data.split(':')[-1]})

                    if frame.image: await callback_query.message.answer_photo(**(await frame.get_for_send()), parse_mode='HTML')

                    else: await callback_query.message.answer(**(await frame.get_for_send()), parse_mode='HTML')