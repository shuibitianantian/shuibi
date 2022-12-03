import datetime
import os
from pathlib import Path
import pickle

from constants import COMPANY_INFO
from helper.DBHelper import DBHelper
from modeling.predict import register_prediction
from scripts.buildModels import LOGISTIC_REGRESSION

MODELS_DIRECTORY = os.path.join(Path(__file__).parent.parent.absolute(), 'models/')
TARGET_MODELS = [LOGISTIC_REGRESSION]


def update_prediction():
    today = str(datetime.date.today())

    with open(os.path.join(MODELS_DIRECTORY, f"{today}.pkl"), 'rb') as f:
        models = pickle.load(f)

    db_helper = DBHelper("shuibi")
    symbols = db_helper.execute(f"SELECT symbol from {COMPANY_INFO}")

    for model in TARGET_MODELS:
        for (symbol, ) in symbols:
            print(f"Predicting: {model} on {symbol}")
            register_prediction(models, model, symbol, db_helper)
