from dataclasses import dataclass
from typing import List, TypeVar, Union


class MessageError(Exception):
    def __init__(self, message, chat_id):
        super().__init__(message)
        self.chat_id = chat_id
        self.message = message


class ArgsLenError(MessageError):
    pass


class ArgsTypeError(MessageError):
    pass


class InvalidSymbolError(MessageError):
    pass


class NotAlertFound(MessageError):
    pass


X = TypeVar('X')
Maybe = Union[X, MessageError]


@dataclass
class Alert:
    chat_id: int
    symbol: str
    max_rsi: int = 70
    min_rsi: int = 30


@dataclass
class PersistentData:
    alerts: List[Alert]
