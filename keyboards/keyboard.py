from typing import Union

from aiogram.types import InlineKeyboardMarkup

from .buttons import Buttons, ButtonTypes


class Keyboards:
    class BaseKeyboard(InlineKeyboardMarkup):
        def __init__(self, row_width: int,
                     buttons: list[Union[str, dict]], state_group_state: str,
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
        def __generate_inline_keyboard(buttons: list[Union[str, dict]],
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


    class MyInlineKeyboard(BaseKeyboard):
        def __init__(self, row_width: int, buttons: list[Union[str, dict]],
                     state_group_state: str,**kwargs):
            super().__init__(row_width, buttons, state_group_state, **kwargs)

    class MyPaginatedInlineKeyboard(BaseKeyboard):
        def __init__(self, row_width: int, buttons: list[Union[str, dict]], state_group_state: str,
                     back_button: str = '⬅️', forward_button: str = '➡️'):
            buttons.extend([{'type': 'pagination_keyboard', 'text': back_button, 'static': True},
                                      {'type': 'pagination_keyboard', 'text': forward_button, 'static': True}])
            super().__init__(row_width=row_width, buttons=buttons, state_group_state=state_group_state)




class KeyboardsCreator:
    @classmethod
    def get_type(cls, keyboard_type: str) -> Union[Keyboards.BaseKeyboard.mro()]:
        return {
            'inline': Keyboards.MyInlineKeyboard,
            'paginated_inline': Keyboards.MyPaginatedInlineKeyboard
        }[keyboard_type]

    @classmethod
    def get_keyboard(cls, keyboard_type: str,
                     row_width: int,
                     buttons: list[Union[str, dict]],
                     state_group_state: str,
                     **kwargs):
        """
        Сгенирировать клавиатуру
        :param row_width:
        :param buttons: Сюда список с текстом. Если указан словарь, то в нём должен быть указан тип кнопки и все
        именованные параметры для её инициализации. По-умолчанию - inline
        :param state_group_state: текстовый варинат стейта, при котором нужно создать клавиатуру
        :param kwargs:
        """
        return cls.get_type(keyboard_type)(row_width=row_width,
                                           buttons=buttons,
                                           state_group_state=state_group_state,
                                           **kwargs)
