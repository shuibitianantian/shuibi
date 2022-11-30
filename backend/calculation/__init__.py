import numpy as np
import talib
import pandas as pd
from sklearn.preprocessing import StandardScaler
from constants import MARKET_INFO
from helper.DBHelper import DBHelper

REQUIRED_COLUMNS = ['open', 'high', 'low', 'close', 'volume']


def prepare_data(data: pd.DataFrame, label_return_period=20, rolling_day=30, annual_return=0.12):
    for col in REQUIRED_COLUMNS:
        assert col in data.columns, f"Column {col} is required."

    # context of the model
    threshold = (annual_return * label_return_period) / 365
    if data.index.name != 'date':
        data.set_index("date", drop=True, inplace=True)

    data.sort_index(inplace=True)
    data.dropna(how="any", axis="rows", inplace=True)

    pct_change = data.close.pct_change()
    data["meanReturn"] = pct_change.rolling(window=rolling_day).mean()
    data["stdReturn"] = pct_change.rolling(window=rolling_day).std()
    data["d-day-sharp-ratio"] = data.meanReturn / data.stdReturn

    data["bbUp"], data['bbMiddle'], data["bbDown"] = talib.BBANDS(data.close, timeperiod=label_return_period,
                                                                  matype=talib.MA_Type.T3)
    data["aroonDown"], data["aroonUp"] = talib.AROON(data.high, data.low, timeperiod=label_return_period)

    data.dropna(how="any", axis="rows", inplace=True)

    data["ema 12"] = talib.EMA(data.close, 12)
    data["ema 26"] = talib.EMA(data.close, 26)

    labels = ((data.close.pct_change(label_return_period).dropna().values > threshold) + 0).tolist()

    scaler = StandardScaler()
    normalized_data = pd.DataFrame(scaler.fit_transform(data.reset_index(drop=True)), columns=data.columns,
                                   index=data.index)

    normalized_data["label"] = labels + label_return_period * [np.NAN]

    normalized_data.dropna(how="any", axis="rows", inplace=True)

    return normalized_data


if __name__ == '__main__':
    db = DBHelper('shuibi')
    results = db.execute(
        f"Select date, open, high, low, close, volume from {MARKET_INFO} where symbol = 'AAPL'"
    )

    hist = pd.DataFrame(results, columns=["date", *REQUIRED_COLUMNS])
    hist['date'] = pd.to_datetime(hist.date, infer_datetime_format=False)

    normalized_data = prepare_data(hist)
    print(normalized_data.columns)
