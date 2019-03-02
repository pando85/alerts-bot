from typing import List, NamedTuple


class Alert(NamedTuple):
    chat_id: int
    symbol: str
    max_rsi: int = 70
    min_rsi: int = 30


class PersistentData(NamedTuple):
    alerts: List[Alert]
