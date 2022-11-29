import numpy as np
import talib
import pandas as pd

from constants import MARKET_INFO
from helper.DBHelper import DBHelper

REQUIRED_COLUMNS = ['open', 'high', 'low', 'close', 'volume']


# Volume Ratio
def volume_ratio(volume, d):
    n = volume.shape[0]
    vr = np.zeros(n)

    for i in range(n):
        if i <= d:
            vr[i] = np.sum(volume.values[:i] > volume.values[i]) / np.sum(volume.values[:i + 1] <= volume.values[i])
        else:
            vr[i] = np.sum(volume.values[i - d + 1:i] > volume.values[i]) / np.sum(
                volume.values[i - d + 1:i + 1] <= volume.values[i])

    return vr


# AroonIndex
def aroon_index(close, d):
    close = close.values
    n = len(close)
    aroon_up = np.empty(n)
    aroon_down = np.empty(n)

    for ind in range(n):
        if ind <= d:
            aroon_up = (ind - np.argmax(close[:ind + 1])) / (ind + 1) * 100
            aroon_down = (ind - np.argmin(close[:ind + 1])) / (ind + 1) * 100
        else:
            aroon_up = (d - np.argmax(close[ind - d + 1:ind] + 1)) / d * 100
            aroon_down = (d - np.argmin(close[ind - d + 1:ind + 1])) / d * 100

    return aroon_up, aroon_down


# exponiential moving average of return
def ema(ret, days):
    ret = ret.values
    beta = 1 - 1 / days
    n = len(ret)
    ema = np.zeros(n)

    for i in range(n):
        if i == 0:
            ema[i] = ret[i]
        else:
            ema[i] = (beta * ema[i - 1] + (1 - beta) * ret[i])

    return ema


def prepare_data(data: pd.DataFrame, label_return_period=10, rolling_day=30, annual_return=0.08):
    for col in REQUIRED_COLUMNS:
        assert col in data.columns, f"Column {col} is required."

    # context of the model
    threshold = (annual_return * label_return_period) / 365
    if data.index.name != 'date':
        data.set_index("date", drop=True, inplace=True)

    data.dropna(how="any", axis="rows", inplace=True)

    labels = ((data.close.pct_change(label_return_period).dropna().values > threshold) + 0).tolist()
    data["labels"] = labels + label_return_period * [np.NAN]

    pct_change = data.close.pct_change()
    data["meanReturn"] = pct_change.rolling(window=rolling_day).mean()
    data["stdReturn"] = pct_change.rolling(window=rolling_day).std()
    data["d-day-sharp-ratio"] = data.meanReturn / data.stdReturn
    data["volumeRatio"] = volume_ratio(data.volume, rolling_day)

    data["bbUp"], data['bbMiddle'], data["bbDown"] = talib.BBANDS(data.close, timeperiod=label_return_period,
                                                                  matype=talib.MA_Type.T3)
    data["aroonDown"], data["aroonUp"] = talib.AROON(data.high, data.low, timeperiod=label_return_period)

    data.dropna(how="any", axis="rows", inplace=True)

    data["ema 12"] = talib.EMA(data.close, 12)
    data["ema 26"] = talib.EMA(data.close, 26)

    data.dropna(how="any", axis="rows", inplace=True)


if __name__ == '__main__':
    db = DBHelper('shuibi')
    results = db.execute(
        f"Select date, open, high, low, close, volume, symbol from {MARKET_INFO} where symbol = 'AAPL'"
    )

    hist = pd.DataFrame(results, columns=["date", *REQUIRED_COLUMNS, 'symbol'])
    hist['date'] = pd.to_datetime(hist.date, infer_datetime_format=False)

    prepare_data(hist)
