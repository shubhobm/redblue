from joblib import dump
import logging
import pandas as pd
import numpy as np
import os
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split

logging.basicConfig(level=logging.INFO)

HOME = os.path.join(os.path.dirname(__file__), "../..")
df = pd.read_csv(f"{HOME}/data/prompts_11152023.csv")
embeddings = np.load(f"{HOME}/data/prompts.npy")


def train_and_save_model(vuln_class):
    logging.info(f"Training detection model for {vuln_class}")
    X_train, X_test, y_train, y_test = train_test_split(
        embeddings, df[f"is_{vuln_class}"], test_size=0.2, random_state=42
    )

    # train elastic net model
    elastic = SGDClassifier(
        loss="log_loss", penalty="elasticnet", random_state=42, l1_ratio=0.01
    )
    elastic.fit(X_train, y_train)

    loc = f"{HOME}/blueteam/api/models/clf_{vuln_class}.joblib"
    dump(elastic, loc)
    logging.info(f"Saved model to {loc}")


if __name__ == "__main__":
    for vuln_class in ["security", "toxicity", "stereotype"]:
        train_and_save_model(vuln_class)
