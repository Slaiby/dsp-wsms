import numpy as np
from joblib import load
import pandas as pd
import os
from .constants import (CONTINUOUS_FEATURES,
                                    CATEGORICAL_FEATURES)


def make_predictions(input_dict: dict):
    scaler = load(os.getcwd() + '/logic_layer/model/scaler.joblib')
    encoder = load(os.getcwd() + '/logic_layer/model/encoder.joblib')
    model = load(os.getcwd() + '/logic_layer/model/model.joblib')

    continuous_features = np.array([[input_dict[feature] for feature in CONTINUOUS_FEATURES]])

    categorical_features = np.array([[input_dict[feature] for feature in CATEGORICAL_FEATURES]])
    categorical_features_encoded = encoder.transform(categorical_features).toarray()

    continuous_features_scaled = scaler.transform(continuous_features)

    input_vector_processed = np.concatenate([continuous_features_scaled, categorical_features_encoded], axis=1)

    predictions = model.predict(input_vector_processed)
    
    return predictions
