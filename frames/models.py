from collections.abc import Callable
from io import BufferedReader

from pydantic import BaseModel, ConfigDict
from aiogram.types import InputFileUnion

from ..keyboards import KeyboardsCreator, models


class FrameModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    text: str
    buttons: list[str] = None
    keyboard_type: str = 'inline'
    cstm_back_btn: str = None
    cstm_frwd_btn: str = None
    move_forward: bool | None = None
    move_back: bool | None = None
    image: InputFileUnion = None
    buttons_generator: Callable = None
    custom_handler: Callable = None
    save_answer: bool = True
