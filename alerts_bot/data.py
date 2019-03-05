import logging
import os
import pandas
import pytz
import time

from alpha_vantage.timeseries import TimeSeries
from datetime import datetime
from typing import Optional

from alerts_bot.config import ALPHAVANTAGE_API_KEY, CHECK_PERIOD
from alerts_bot.types import Alert


log = logging.getLogger(__name__)

NASDAQ_TZ = pytz.timezone('America/New_York')


def _is_stock_market_open(current_time: datetime) -> bool:
    return current_time.hour > 9 and current_time.hour < 16 and current_time.weekday() in range(4)


def is_cache_Valid(file_path: str) -> bool:
    try:
        is_valid = time.time() < os.path.getmtime(file_path) + CHECK_PERIOD
    except FileNotFoundError:
        return False
    return is_valid


def get_rsi(series: pandas.Series, window_length: int) -> pandas.Series:
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


def check_alert(alert: Alert) -> Optional[str]:

    cache_path = f'/tmp/{alert.symbol}.pkl'
    if is_cache_Valid(cache_path):
        log.debug(f'Reading cache file: {cache_path}')
        rsi = pandas.read_pickle(cache_path)
    else:
        ts = TimeSeries(key=ALPHAVANTAGE_API_KEY, output_format='pandas')
        data, meta_data = ts.get_intraday(symbol=alert.symbol, interval='1min', outputsize='compact')
        log.debug(f'Data for symbol {alert.symbol}: {data.tail()}')
        window_length = 14
        close = data['4. close']
        # Get the difference in price from previous step
        rsi = get_rsi(close, window_length)
        rsi.to_pickle(cache_path)
    log.debug(f'{alert.symbol} rsi: {rsi} -> max: {alert.max_rsi} {alert.min_rsi}')

    if rsi[-1] >= alert.max_rsi:
        return f'{rsi.index[-1]} {alert.symbol} -> RSI: {rsi[-1]} -> SELL (last price: {close[-1]})'

    if rsi[-1] <= alert.min_rsi:
        return f'{rsi.index[-1]} {alert.symbol} -> RSI: {rsi[-1]} -> BUY (last price: {close[-1]})'

    return None
