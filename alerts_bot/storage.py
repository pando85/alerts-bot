import ujson

from alerts_bot.config import STORAGE_FILE_PATH
from alerts_bot.types import Alert, PersistentData


def save_data(data: PersistentData) -> PersistentData:
    with open(STORAGE_FILE_PATH, 'w') as f:
        ujson.dump(data, f)
    return data


def read_data() -> PersistentData:
    with open(STORAGE_FILE_PATH, 'r') as f:
        data = PersistentData(ujson.load(f))
    return data


def append_alert(alert: Alert) -> PersistentData:
    data = read_data()
    data.alerts.append(alert)
    return save_data(data)


def remove_alert(alert: Alert) -> PersistentData:
    data = read_data()
    data._replace(alerts=list(filter(
        lambda x: False if x.chat_id == alert.chat_id and x.symbol == alert.symbol else True,
        data.alerts)))
    return save_data(data)
