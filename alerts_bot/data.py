import pandas

from alpha_vantage.timeseries import TimeSeries

from alerts_bot.types import Alert


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

