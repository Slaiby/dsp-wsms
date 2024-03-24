# train.py

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from joblib import dump
from sklearn.metrics import mean_squared_log_error
from acceptance_prediction.preprocess import prepare_data, preprocess_data


def train_model(X_train_preprocessed, y_train) -> LogisticRegression:
    model = LogisticRegression()
    model.fit(X_train_preprocessed, y_train)
    return model

def save_model_and_preprocessors(scaler, encoder, model) -> None:
    dump(scaler, '../model/scaler.joblib')
    print('scaler saved')
    dump(encoder, '../model/encoder.joblib')
    print('encoder saved')
    dump(model, '../model/model.joblib')
    print('model saved')

def compute_rmsle(y_test: np.ndarray, y_pred: np.ndarray, precision: int = 2) -> float:
    rmsle = np.sqrt(mean_squared_log_error(y_test, y_pred))
    return round(rmsle, precision)


def build_model(data: pd.DataFrame) -> dict:
    X_train, X_test, y_train, y_test = prepare_data(data)

    X_train_preprocessed, X_test_preprocessed, scaler, encoder = \
        preprocess_data(X_train, X_test)

    model = train_model(X_train_preprocessed, y_train)

    save_model_and_preprocessors(scaler, encoder, model)
     
    rmsle = compute_rmsle(y_test, model.predict(X_test_preprocessed))
    return {'rmsle': rmsle}
