from collections.abc import Callable

from pydantic import BaseModel, model_validator

from keyboards import KeyboardsCreator, models


class FrameModel(BaseModel):
    text: str
    buttons: list[str] = None
    keyboard_type: str = 'inline'
    cstm_back_btn: str = None
    cstm_frwd_btn: str = None
    move_forward: bool | None = None
    move_back: bool | None = None
    buttons_generator: Callable = None
    custom_handler: Callable = None
