from aiogram.types import InlineKeyboardButton, KeyboardButton
from abc import ABC


class Buttons:

    class IButton(ABC):
        pass

    class MyInlineKeyboardButton(InlineKeyboardButton, IButton):
        def __init__(self, text: str, callback_data: str):
            super().__init__(text=text, callback_data=callback_data)

    class MyKeyboardButton(KeyboardButton, IButton):
        def __init__(self, text: str):
            super().__init__(text=text)

    class CheckBoxButton(InlineKeyboardButton, IButton):
        def __init__(self, unchecked_text: str, checked_text: str, callback_data: str, **kwargs):
            super().__init__(text=unchecked_text, callback_data=callback_data)
            self.checked_text = checked_text
            self.is_checked = False

        def __on_click(self):
            """
            Логика переключения состояния
            :return:
            """
            text = self.checked_text if self.is_checked else self.unchecked_text
            self.is_checked = not self.is_checked
            return super().__init__(text=text, callback_data=self.callback_data)


class ButtonTypes:
    @staticmethod
    def get_button_type(text: str):
        return {
            'inline': Buttons.MyInlineKeyboardButton,
            'checkbox': Buttons.CheckBoxButton
        }[text]



