import os
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib


def get_data_path():
    base = os.path.dirname(__file__)
    return os.path.join(base, "data", "emergency_reports.csv")


def load_data(path):
    df = pd.read_csv(path)
    df = df.dropna(subset=["Description", "Category", "Severity"])
    df["text"] = df["Category"].astype(str) + " -- " + df["Description"].astype(str)
    return df


def train_and_save(path, out_dir="models"):
    df = load_data(path)
    X = df["text"].values
    y = df["Severity"].values

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1,2))),
        ("clf", RandomForestClassifier(n_estimators=200, random_state=42))
    ])

    print("Training model on {} samples".format(len(X)))
    pipeline.fit(X, y)

    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "severity_pipeline.joblib")
    joblib.dump(pipeline, out_path)
    print(f"Saved pipeline to {out_path}")


if __name__ == "__main__":
    data_path = get_data_path()
    if not os.path.exists(data_path):
        print(f"Data file not found: {data_path}")
        print("Place your CSV at the path or use the provided synthetic dataset.")
    else:
        train_and_save(data_path)