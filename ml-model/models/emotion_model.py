import pandas as pd
import re
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from utils.preprocessing import clean_text

# Configuration
CONFIG = {
    "data_path": "data/goemotions.csv",
    "model_path": "models/emotion_classifier.pkl",
    "vectorizer_path": "models/tfidf_vectorizer.pkl",
    "max_features": 5000,
    "test_size": 0.2,
    "random_state": 42,
    "max_iter": 1000
}

class EmotionModelTrainer:
    def __init__(self, config):
        self.config = config
        self.vectorizer = TfidfVectorizer(max_features=self.config["max_features"])
        self.model = LogisticRegression(max_iter=self.config["max_iter"])

    def load_and_preprocess(self):
        """Loads the dataset and applies text cleaning."""
        print(f"Loading dataset from {self.config['data_path']}...")
        if not os.path.exists(self.config["data_path"]):
            raise FileNotFoundError(f"Dataset not found at {self.config['data_path']}")
            
        df = pd.read_csv(self.config["data_path"])
        df = df[["text", "label"]]
        
        print("Preprocessing text...")
        df["clean_text"] = df["text"].apply(clean_text)
        return df

    def train(self):
        """Executes the full training pipeline."""
        df = self.load_and_preprocess()

        print("Converting text to numerical features...")
        X = self.vectorizer.fit_transform(df["clean_text"])
        y = df["label"]

        print("Splitting dataset...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=self.config["test_size"], 
            random_state=self.config["random_state"]
        )

        print(f"Training emotion model (Samples: {X_train.shape[0]})...")
        self.model.fit(X_train, y_train)

        print("Evaluating model...")
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model Accuracy: {accuracy:.4f}")

        self.save_artifacts()

    def save_artifacts(self):
        """Saves the trained model and vectorizer to disk."""
        print("Saving artifacts...")
        os.makedirs(os.path.dirname(self.config["model_path"]), exist_ok=True)
        
        with open(self.config["model_path"], "wb") as f:
            pickle.dump(self.model, f)
        
        with open(self.config["vectorizer_path"], "wb") as f:
            pickle.dump(self.vectorizer, f)
            
        print(f"Model saved to {self.config['model_path']}")
        print(f"Vectorizer saved to {self.config['vectorizer_path']}")

if __name__ == "__main__":
    trainer = EmotionModelTrainer(CONFIG)
    try:
        trainer.train()
    except Exception as e:
        print(f"An error occurred during training: {e}")
