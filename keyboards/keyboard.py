from typing import Union
from aiogram.types import InlineKeyboardMarkup, Message
from aiogram import Bot, Dispatcher
from .buttons import Buttons, ButtonTypes
from .models import ButtonModel, ButtonRowModel


bot = Bot('7158763984:AAER036-nXFByWbM_yu20MBB9kk13rSDtvw')
dp = Dispatcher()

class Keyboards:
    class MyBaseKeyboard(InlineKeyboardMarkup):
        __pydantic_extra__ = 'forbid'
        def __init__(self, row_width: int,
                     buttons: list[ButtonModel], state_group_state: str,
                     **kwargs):
            """
            Сгенирировать клавиатуру
            :param row_width:
            :param buttons: Сюда список с текстом. Если указан словарь, то в нём должен быть указан тип кнопки и все
            именованные параметры для её инициализации. По-умолчанию - inline
            :param state: текстовый варинат стейта, при котором нужно создать клавиатуру
            :param kwargs:
            """
            self.row_width = row_width
            self.state_group_state = state_group_state
            self.kwargs = kwargs
            self.keyboard = self.__generate_inline_keyboard(buttons, row_width, state_group_state)
            super().__init__(
                inline_keyboard=self.keyboard, **kwargs
            )

        @staticmethod
        def __generate_inline_keyboard(buttons: list[ButtonModel],
                                     row_width: int,
                                     state_group_state: str) -> list[list[Buttons.IButton.mro()]]:
            keyboard = []
            for i, el in enumerate(buttons):
                if i % row_width == 0:
                    keyboard.append([])

                if isinstance(el, str):
                    keyboard[-1].append(Buttons.MyInlineKeyboardButton(text=el, callback_data=f'{state_group_state}:{i}'))
                elif isinstance(el, dict):
                    keyboard[-1].append(ButtonTypes.get_button_type(text=el['type'])(**el, callback_data=f'{state_group_state}:{i}'))

            return keyboard

    class MyInlineKeyboard(MyBaseKeyboard):
        def __init__(self, row_width: int, buttons: list[ButtonModel],
                     state_group_state: str,**kwargs):
            super().__init__(row_width, buttons, state_group_state, **kwargs)

    class MyPaginatedInlineKeyboard(MyBaseKeyboard):
        def __init__(self, row_width: int, buttons: list[ButtonModel], state_group_state: str,
                     nav_buttons: ButtonRowModel, **kwargs):
            super().__init__(row_width=row_width, buttons=buttons, state_group_state=state_group_state)

class KeyboardsCreator:
    @classmethod
    def get_type(cls, keyboard_type: str) -> Union[Keyboards.MyBaseKeyboard.mro()]:
        return {
            'inline': Keyboards.MyInlineKeyboard,
            'paginated_inline': Keyboards.MyPaginatedInlineKeyboard
        }.get(keyboard_type, Keyboards.MyInlineKeyboard)

    @classmethod
    def get_keyboard(cls, keyboard_type: str,
                     row_width: int,
                     buttons: list[ButtonModel],
                     state_group_state: str,
                     **kwargs):
        """
        Сгенерировать клавиатуру
        :param keyboard_type: inline or paginated_inline. Default - inline
        :param row_width:
        :param buttons: Сюда список с текстом. Если указан словарь, то в нём должен быть указан тип кнопки и все
        именованные параметры для её инициализации. По-умолчанию - inline
        :param state_group_state: текстовый вариант стейта, при котором нужно создать клавиатуру
        :param kwargs:
        """
        return cls.get_type(keyboard_type)(row_width=row_width,
                                           buttons=buttons,
                                           state_group_state=state_group_state,
                                           **kwargs)
