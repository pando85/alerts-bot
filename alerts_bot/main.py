import asyncio
import logging
import sys

from aiofunctools import curry, compose
from aiogram import Bot, Dispatcher, executor, types

from alerts_bot.config import BOT_TOKEN, CHECK_PERIOD, LOG_LEVEL
from alerts_bot.data import check_alert
from alerts_bot.parser import validate_message, get_alert
from alerts_bot.types import Alert, Maybe, MessageError
from alerts_bot.storage import append_alert, list_all, read_data, remove_alert


log = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

HELP_MESSAGE = """
    Alarm bot for stock RSI changes
    /start <symbol> [<max_rsi> <min_rsi>]   Init stock alarm. Defaults: max_rsi=70 min_rsi=30
    /stop <symbol> [<max_rsi> <min_rsi>]    Remove stock alarm. Defaults: max_rsi=70 min_rsi=30
    /list                                   List registered alarms
    /help                                   show this message

    Examples:
    /start MU
    /stop MU
    /start GOOGL 80 20
    /stop GOOGL 80 20
    /list

"""


@curry
async def reply(reply_message: str, alert: Maybe[Alert]) -> Maybe[Alert]:
    if isinstance(alert, MessageError):
        await bot.send_message(alert.chat_id, alert.message)
        await bot.send_message(alert.chat_id, 'Usage: /help')
        return alert

    await bot.send_message(alert.chat_id, reply_message.format(alert.symbol))
    return alert


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when client send `/start` or `/help` commands.
    """
    await message.reply(HELP_MESSAGE)


@dp.message_handler(commands=['start'])
async def register_alarm(message: types.Message):
    if not validate_message(message):
        await bot.send_message(message.chat.id, HELP_MESSAGE)
        return

    return await compose(
        validate_message,
        get_alert,
        append_alert,
        reply('{} alert registered correctly')
    )(message)


@dp.message_handler(commands=['stop'])
async def unregister_alarm(message: types.Message):
    return await compose(
        validate_message,
        get_alert,
        remove_alert,
        reply('{} alert removed correctly')
    )(message)


@dp.message_handler(commands=['list'])
async def list_alarms(message: types.Message):
    alerts = list_all(message.chat.id)
    alerts_string_list = '\n'.join([
        f'{alert.symbol} {alert.max_rsi} {alert.min_rsi}' for alert in alerts])

    if not alerts_string_list:
        alerts_string_list = 'No alarms set yet!'
    return await bot.send_message(
        message.chat.id,
        alerts_string_list)


def setup_logging():
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)
    log.info(root_logger.handlers)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    root_logger.addHandler(screen_handler)
    log.info(root_logger.handlers)
    log.debug(f'Setup log level to {LOG_LEVEL}')


async def check_alerts():
    while True:
        await asyncio.sleep(2)

        data = read_data()

        # free API key just give 5 request per minute and 500 per day
        for alert in data.alerts:
            try:
                message = check_alert(alert)
                if message:
                    await bot.send_message(alert.chat_id, message)
            except KeyError as e:
                log.error(f'{alert.symbol}: {e}')
            except Exception as e:
                log.error(f'{alert.symbol}: {e}')
        await asyncio.sleep(CHECK_PERIOD)


def main():
    setup_logging()
    loop = asyncio.get_event_loop()
    loop.create_task(check_alerts())
    executor.start_polling(dp, loop=loop, skip_updates=True)
