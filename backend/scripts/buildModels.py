from constants import PROCESSED_DATA_COLUMNS
from helper.utils import get_symbols, get_dataset, get_est_today_with_offset
from modeling.logistic_regression import fit_logistic_regression
import pandas as pd
import datetime
import pickle
from helper.utils import register_performance_data
import os
from pathlib import Path


LOGISTIC_REGRESSION = 'lg'

MODELS_DIRECTORY = os.path.join(Path(__file__).parent.parent.absolute(), 'models/')


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
    a.dropna(how="any", axis="rows", inplace=True)
    y = a.label.astype(int)
    x = a.drop(['label', 'date'], axis=1)

    today = get_est_today_with_offset()
    performance, models = [], {}

    lg_clf, accuracy = fit_logistic_regression(x, y, True, True)
    performance.append((today, LOGISTIC_REGRESSION, accuracy, size))
    models[LOGISTIC_REGRESSION] = lg_clf

    if save_model:
        with open(os.path.join(MODELS_DIRECTORY, f"{today}.pkl"), 'wb') as f:
            pickle.dump(models, f)

    if dump_performance:
        register_performance_data(performance)
