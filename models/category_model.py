import pandas as pd
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from utils.preprocessing import clean_text

# Configuration
CONFIG = {
    "datasets": [
        {
            "path": "data/customer_support_tickets.csv",
            "text_cols": ["Ticket Subject", "Ticket Description"],
            "label_col": "Ticket Type",
            "map": {
                "Technical issue": "technical",
                "Billing inquiry": "billing",
                "Cancellation request": "account",
                "Product inquiry": "inquiry",
                "Refund request": "billing"
            }
        },
        {
            "path": "data/dataset-tickets-multi-lang-4-20k.csv",
            "text_cols": ["subject", "body"],
            "label_col": "queue",
            "map": {
                "Technical Support": "technical",
                "Billing and Payments": "billing",
                "Account Management": "account",
                "Customer Onboarding": "account",
                "General Inquiry": "inquiry",
                "Sales and Pre-Sales": "inquiry",
                "Product Feedback": "feature_request",
                "Feature Request": "feature_request"
            }
        },
        {
            "path": "data/dataset-tickets-german_normalized_50_5_2.csv",
            "text_cols": ["subject", "body"],
            "label_col": "queue",
            "map": {
                "Technical Support": "technical",
                "Billing and Payments": "billing",
                "Account Management": "account",
                "Customer Onboarding": "account",
                "General Inquiry": "inquiry",
                "Sales and Pre-Sales": "inquiry",
                "Product Feedback": "feature_request",
                "Feature Request": "feature_request"
            }
        }
    ],
    "model_path": "models/category_classifier.pkl",
    "vectorizer_path": "models/category_vectorizer.pkl",
    "max_features": 10000,
    "test_size": 0.2,
    "random_state": 42,
    "max_iter": 2000,
}

class CategoryModelTrainer:
    def __init__(self, config):
        self.config = config
        self.vectorizer = TfidfVectorizer(max_features=self.config["max_features"], ngram_range=(1, 2))
        self.model = LogisticRegression(max_iter=self.config["max_iter"], class_weight='balanced')

    def load_and_preprocess(self):
        """Loads and combines multiple datasets."""
        all_dfs = []
        
        for ds in self.config["datasets"]:
            path = ds["path"]
            if not os.path.exists(path):
                print(f"Warning: Dataset not found at {path}, skipping...")
                continue
                
            print(f"Loading {path}...")
            df = pd.read_csv(path)
            
            # Create features
            t_cols = ds["text_cols"]
            df["full_text"] = df[t_cols[0]].astype(str)
            for i in range(1, len(t_cols)):
                df["full_text"] += " " + df[t_cols[i]].astype(str)
            
            # Map labels
            df["category"] = df[ds["label_col"]].map(ds["map"])
            
            # Keep only needed columns
            df = df[["full_text", "category"]].dropna()
            all_dfs.append(df)
            
        if not all_dfs:
            raise ValueError("No datasets loaded successfully!")
            
        combined_df = pd.concat(all_dfs, ignore_index=True)
        print(f"Combined dataset size: {len(combined_df)}")
        
        print("Cleaning text...")
        combined_df["clean_text"] = combined_df["full_text"].apply(clean_text)
        
        return combined_df

    def train(self):
        """Executes the training pipeline."""
        df = self.load_and_preprocess()

        print("Converting text to numerical features...")
        X = self.vectorizer.fit_transform(df["clean_text"])
        y = df["category"]

        print("Splitting dataset...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=self.config["test_size"], 
            random_state=self.config["random_state"]
        )

        print(f"Training category model (Samples: {X_train.shape[0]})...")
        self.model.fit(X_train, y_train)

        print("Evaluating model...")
        y_pred = self.model.predict(X_test)
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))

        self.save_artifacts()

    def save_artifacts(self):
        """Saves the trained model and vectorizer."""
        print("Saving artifacts...")
        os.makedirs(os.path.dirname(self.config["model_path"]), exist_ok=True)
        
        with open(self.config["model_path"], "wb") as f:
            pickle.dump(self.model, f)
        
        with open(self.config["vectorizer_path"], "wb") as f:
            pickle.dump(self.vectorizer, f)
            
        print(f"Model saved to {self.config['model_path']}")
        print(f"Vectorizer saved to {self.config['vectorizer_path']}")

if __name__ == "__main__":
    trainer = CategoryModelTrainer(CONFIG)
    try:
        trainer.train()
    except Exception as e:
        print(f"An error occurred during training: {e}")

