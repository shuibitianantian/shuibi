from constants import PROCESSED_DATA_COLUMNS
from helper.utils import get_symbols, get_dataset
from modeling.logistic_regression import fit_logistic_regression
import pandas as pd
import datetime
import pickle
from helper.utils import register_performance_data

LOGISTIC_REGRESSION = 'lg'


def update_models(size=-1, dump_performance=False, save_model=False):
    symbols = get_symbols()

    assert size < len(symbols), f"size should smaller than {len(symbols)}"
    all_data = []
    for idx, symbol in enumerate(symbols[:size]):
        print(f"{idx + 1}/{len(symbols)} {symbol}")
        data = get_dataset(symbol)
        data = pd.DataFrame(data, columns=PROCESSED_DATA_COLUMNS)
        data.drop('symbol', axis=1, inplace=True)

        all_data.append(data)

    a = pd.concat(all_data)
    y = a.label.astype(int)
    x = a.drop(['label', 'date'], axis=1)

    today = str(datetime.date.today())
    performance, models = [], {}

    lg_clf, accuracy = fit_logistic_regression(x, y, True, True)
    performance.append((today, LOGISTIC_REGRESSION, accuracy, size))
    models[LOGISTIC_REGRESSION] = lg_clf

    if save_model:
        with open(f'../models/{today}.pkl', 'wb') as f:
            pickle.dump(models, f)

    if dump_performance:
        register_performance_data(performance)
