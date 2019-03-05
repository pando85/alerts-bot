from aiofunctools import bind
from aiogram.types import Message

from alerts_bot import symbols
from alerts_bot.types import Alert, ArgsLenError, ArgsTypeError, InvalidSymbolError, Maybe


@bind
def get_alert(message: Message) -> Alert:
    text_list = message.text.split(' ')
    if len(text_list) == 2:
        return Alert(message.chat.id, text_list[1])

    return Alert(message.chat.id, text_list[1], int(text_list[2]), int(text_list[3]))


def validate_message(message: Message) -> Maybe[Alert]:
    text_list = message.text.split(' ')
    _len = len(text_list)
    if _len > 4 or _len < 2:
        return ArgsLenError('Invalid number of arguments sent', message.chat.id)
    if text_list[1] not in symbols.ALL:
        return InvalidSymbolError('Invalid symbol, try another one.', message.chat.id)
    if _len == 2:
        return message
    try:
        int(text_list[2])
        int(text_list[3])
    except ValueError:
        return ArgsTypeError('max_rsi and min_rsi must be integer values', message.chat.id)
    return message
