import numpy as np

from constants import PROCESSED_DATA, PREDICTION
import datetime
import os
from pathlib import Path

MODELS_DIRECTORY = os.path.join(Path(__file__).parent.parent.absolute(), 'models/')


def register_prediction(models, model_name, symbol, db_helper):
    today = str(datetime.date.today())
    model = models[model_name]
    results = db_helper.execute(f"SELECT * from {PROCESSED_DATA} where symbol='{symbol}' and date='{today} 00:00:00';")
    if len(results) == 0:
        return
    pred = model.predict([np.array(results[0][1:-2])])[0]
    try:
        db_helper.execute(f"""CREATE TABLE {PREDICTION} (
            date VARCHAR(255),
            prediction INT,
            model VARCHAR(255),
            symbol VARCHAR(255),
            PRIMARY KEY (symbol, model, date)
        )""")
    except Exception as e:
        pass

    db_helper.execute(f"REPLACE INTO {PREDICTION} VALUES ('{today}', {pred}, '{model_name}', '{symbol}')")

