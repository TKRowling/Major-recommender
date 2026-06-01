import os
import joblib

from app.config import Config

"Late this can load your real pickle models"

def load_pickle(filename):
    path = os.path.join(Config.MODELS_DIR, filename)
    if not os.path.exists(path):
        return None
    return joblib.load(path)


def load_macro_major_model():
    return load_pickle("macro_major_model.pkl")


def load_label_encoder():
    return load_pickle("label_encoder.pkl")


def load_scaler():
    return load_pickle("scaler.pkl")


def load_feature_columns():
    return load_pickle("feature_columns.pkl")


def load_category_encoders():
    return load_pickle("category_encoders.pkl")