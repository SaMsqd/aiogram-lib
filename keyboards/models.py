from pydantic import BaseModel,  model_validator


class ButtonModel(BaseModel):
    """
    Модель для генерации кнопки
    """
    type: str = 'inline'
    text: str
    is_static: bool = False
    is_navigation: bool = False
    move_back: bool = False
    move_forward: bool = False
    move_button_down: bool = False
    take_all_row: bool = False

    @model_validator(mode='before')
    def validate_navigation(self, values):
        """
        Валидатор для проверки, что если is_navigation=True, то move_forward или move_back должны быть True.
        """
        is_navigation = values.get('is_navigation')
        move_forward = values.get('move_forward')
        move_back = values.get('move_back')

        if is_navigation and not (move_forward or move_back):
            raise ValueError('Если is_navigation=True, то move_forward или move_back должны быть True')

        return values


class ButtonRowModel(BaseModel):
    buttons: list[ButtonModel]
