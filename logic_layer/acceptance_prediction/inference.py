import numpy as np
from joblib import load
import pandas as pd
from acceptance_prediction.constants import (CONTINUOUS_FEATURES,
                                    CATEGORICAL_FEATURES)


def make_predictions(input_data: pd.DataFrame) -> np.ndarray:
    scaler = load('../models/scaler.joblib')
    encoder = load('../models/encoder.joblib')
    model = load('../models/model.joblib')

    continuous_data = scaler.transform(
        input_data[CONTINUOUS_FEATURES].fillna(
            input_data[CONTINUOUS_FEATURES].median())
    )
    categorical_data = encoder.transform(
        input_data[CATEGORICAL_FEATURES].fillna(
            input_data[CATEGORICAL_FEATURES].mode().iloc[0])
    ).toarray()

    input_data_preprocessed = np.hstack((continuous_data, categorical_data))

    predictions = model.predict(input_data_preprocessed)

    return predictions
