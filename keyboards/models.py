from typing import Any

from pydantic import BaseModel,  model_validator
from pydantic_core.core_schema import ValidationInfo


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
    @classmethod
    def validate_navigation(cls, data: Any):
        """
        Валидатор для проверки, что если is_navigation=True, то move_forward или move_back должны быть True.
        """
        if isinstance(data, dict):
            values = data
        else:
            # Если это объект модели или другой тип, пробуем получить dict
            values = data.model_dump() if hasattr(data, 'model_dump') else {}

        # Проверка условий валидации
        is_navigation = values.get('is_navigation', False)
        move_forward = values.get('move_forward', False)
        move_back = values.get('move_back', False)

        if is_navigation and not (move_forward or move_back):
            raise ValueError(
                'Если is_navigation=True, то move_forward или move_back должны быть True'
            )

        return values


class ButtonRowModel(BaseModel):
    buttons: list[ButtonModel]
