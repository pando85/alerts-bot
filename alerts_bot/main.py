import asyncio
import logging
import pandas

from aiogram import Bot, Dispatcher, executor, types
from alpha_vantage.timeseries import TimeSeries

from alerts_bot.config import BOT_TOKEN
from alerts_bot.types import Alert
from alerts_bot.storage import append_alert, remove_alert

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('alerts_bot')

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
loop = asyncio.get_event_loop()
dp = Dispatcher(bot)

HELP_MESSAGE = """
    Alarm bot for stock RSI changes
    /start <symbol> [<max_rsi> <min_rsi>]   Init alarm in stock. Defaults: max_rsi=70 min_rsi=30
    /stop <symbol>

    Examples:
    /start MU 70 30
    /stop MU
"""


def get_rsi(series, window_length):
    delta = series.diff()
    up = delta.copy()
    down = delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    roll_up = pandas.Series.ewm(up, span=window_length).mean()
    roll_down = pandas.Series.ewm(down, span=window_length).mean().abs()
    rs = roll_up / roll_down
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return rsi


def check_alert(alert: Alert):
    ts = TimeSeries(key='EJ69MPM068NGTJ30', output_format='pandas')

    data, meta_data = ts.get_intraday(symbol=alert.symbol, interval='1min', outputsize='compact')

    window_length = 14
    close = data['4. close']
    # Get the difference in price from previous step
    rsi = get_rsi(close, window_length)
    print(rsi)


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when client send `/start` or `/help` commands.
    """
    await message.reply(HELP_MESSAGE)


@dp.message_handler(commands=['start'])
async def register_alarm(message: types.Message):
    if not is_message_valid(message):
        await bot.send_message(message.chat.id, HELP_MESSAGE)
        return

    alert = get_alert(message)
    append_alert(alert)


def get_alert(message: types.Message) -> Alert:
    text_list = message.text.split(' ')
    if len(text_list) == 1:
        return Alert(message.chat.id, text_list[0])

    return Alert(message.chat.id, text_list[0], int(text_list[1]), int(text_list[2]))


def is_message_valid(message):
    text_list = message.text.split(' ')
    _len = len(text_list)
    if _len > 3 or _len < 1:
        return False
    if _len == 1:
        return True
    try:
        int(text_list[1])
        int(text_list[1])
    except ValueError:
        return False
    return True


def main():
    executor.start_polling(dp, loop=loop, skip_updates=True)
