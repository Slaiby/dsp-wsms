import os
import numpy as np
import pandas as pd
from joblib import load
from .constants import CONTINUOUS_FEATURES, CATEGORICAL_FEATURES

class PredictionModel:
    def __init__(self):
        self.scaler = load(os.path.join(os.getcwd(), 'logic_layer/model/scaler.joblib'))
        self.encoder = load(os.path.join(os.getcwd(), 'logic_layer/model/encoder.joblib'))
        self.model = load(os.path.join(os.getcwd(), 'logic_layer/model/model.joblib'))

    def make_prediction(self, input_dict: dict):
        continuous_features = np.array([[input_dict[feature] for feature in CONTINUOUS_FEATURES]])
        categorical_features = np.array([[input_dict[feature] for feature in CATEGORICAL_FEATURES]])
        categorical_features_encoded = self.encoder.transform(categorical_features).toarray()
        continuous_features_scaled = self.scaler.transform(continuous_features)

        input_vector_processed = np.concatenate([continuous_features_scaled, categorical_features_encoded], axis=1)
        prediction = self.model.predict(input_vector_processed)
        
        return prediction

    def make_predictions_from_csv(self, csv_path: str):
        df = pd.read_csv(csv_path)
        predictions = []

        for _, row in df.iterrows():
            row_dict = row.to_dict()
            prediction = self.make_prediction(row_dict)
            predictions.append(prediction[0])

        return predictions