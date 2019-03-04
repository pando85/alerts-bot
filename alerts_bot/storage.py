import logging
import ujson

from aiofunctools import bind
from typing import List

from alerts_bot.config import STORAGE_FILE_PATH
from alerts_bot.types import Alert, Maybe, NotAlertFound, PersistentData

log = logging.getLogger(__name__)


def save_data(data: PersistentData) -> PersistentData:
    log.debug(f'Write data: {data}')
    with open(STORAGE_FILE_PATH, 'w') as f:
        ujson.dump(data, f)
    return data


def read_data() -> PersistentData:
    try:
        with open(STORAGE_FILE_PATH, 'r') as f:
            data = PersistentData([Alert(**alert) for alert in ujson.load(f)['alerts']])
    except FileNotFoundError:
        return PersistentData([])
    log.debug(f'Read data: {data}')
    return data


@bind
def append_alert(alert: Alert) -> Alert:
    data = read_data()
    log.info(data)
    log.info(data.alerts)
    data.alerts.append(alert)
    save_data(data)
    log.info(f'Append alert: {alert}')
    return alert


@bind
def remove_alert(alert: Alert) -> Maybe[Alert]:
    data = read_data()
    if alert not in data.alerts:
        return NotAlertFound('Not alert found in registered alerts', alert.chat_id)
    data.alerts = list(filter(
        lambda x: False if x.chat_id == alert.chat_id and x.symbol == alert.symbol else True,
        data.alerts))
    save_data(data)
    log.info(f'Remove alert: {alert}')
    return alert


@bind
def list_all(chat_id: int) -> List[Alert]:
    data = read_data()
    return list(filter(lambda x: True if x.chat_id == chat_id else False, data.alerts))