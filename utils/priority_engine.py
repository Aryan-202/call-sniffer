import pickle
import os
from utils.preprocessing import clean_text

# Scoring weights for each label
URGENCY_SCORES = {
    "critical": 10,
    "high":      7,
    "medium":    4,
    "low":       1
}

EMOTION_SCORES = {
    # High distress boosts score
    "anger":          3,
    "fear":           3,
    "nervousness":    2,
    "grief":          2,
    "disgust":        2,
    "annoyance":      1,
    "disappointment": 1,
    "confusion":      1,
    # Neutral / positive emotions reduce urgency
    "neutral":        0,
    "curiosity":      0,
    "approval":      -1,
    "joy":           -1,
    "admiration":    -1,
    "gratitude":     -2,
}

PRIORITY_TIERS = [
    (9, "P1 — Critical (Respond in minutes)"),
    (7, "P2 — High (Respond within the hour)"),
    (4, "P3 — Medium (Respond within the day)"),
    (0, "P4 — Low (Respond within the week)"),
]

# GoEmotions label mapping
EMOTION_LABELS = {
    0: "admiration", 1: "amusement", 2: "anger", 3: "annoyance", 4: "approval",
    5: "caring", 6: "confusion", 7: "curiosity", 8: "desire", 9: "disappointment",
    10: "disapproval", 11: "disgust", 12: "embarrassment", 13: "excitement",
    14: "fear", 15: "gratitude", 16: "grief", 17: "joy", 18: "love",
    19: "nervousness", 20: "optimism", 21: "pride", 22: "realization",
    23: "relief", 24: "remorse", 25: "sadness", 26: "surprise", 27: "neutral"
}

class PriorityEngine:
    def __init__(self, models_dir=None):
        if models_dir is None:
            # Default to the 'models' directory at the project root
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.models_dir = os.path.join(base_dir, "models")
        else:
            self.models_dir = models_dir
            
        self.models = {}
        self.vectorizers = {}
        self._load_all()

    def _load_pickle(self, filename):
        path = os.path.join(self.models_dir, filename)
        if not os.path.exists(path):
            print(f"Warning: Artifact not found at {path}")
            return None
        with open(path, "rb") as f:
            return pickle.load(f)

    def _load_all(self):
        """Loads all classifier and vectorizer artifacts."""
        # Emotion Model
        self.models["emotion"] = self._load_pickle("emotion_classifier.pkl")
        self.vectorizers["emotion"] = self._load_pickle("tfidf_vectorizer.pkl")

        # Category Model
        self.models["category"] = self._load_pickle("category_classifier.pkl")
        self.vectorizers["category"] = self._load_pickle("category_vectorizer.pkl")

        # Urgency Model
        self.models["urgency"] = self._load_pickle("urgency_classifier.pkl")
        self.vectorizers["urgency"] = self._load_pickle("urgency_vectorizer.pkl")

    def compute_priority_score(self, urgency, emotion):
        """
        Combines urgency and emotion into a numeric priority score (1-10)
        and maps it to a human-readable priority tier (P1-P4).
        
        Logic:
          - Urgency gives the base score (critical=10, high=7, medium=4, low=1)
          - Emotion adjusts the score up or down (+3 for anger/fear, -2 for gratitude)
          - Final score is clamped between 1 and 10
        """
        base_score = URGENCY_SCORES.get(urgency, 4)
        emotion_boost = EMOTION_SCORES.get(emotion, 0)
        
        # Clamp score to valid range
        final_score = max(1, min(10, base_score + emotion_boost))
        
        # Determine tier from score
        tier = "P4 — Low (Respond within the week)"
        for threshold, label in PRIORITY_TIERS:
            if final_score >= threshold:
                tier = label
                break
        
        return final_score, tier

    def predict(self, text):
        """
        Runs the input text through all three classification models.
        Returns a dictionary with:
          - emotion    : detected emotion label
          - category   : ticket category
          - urgency    : urgency level text
          - priority_score : numeric score from 1-10
          - priority_tier  : P1/P2/P3/P4 label with response time guidance
        """
        cleaned = clean_text(text)
        results = {"original_text": text}

        for task in ["emotion", "category", "urgency"]:
            model = self.models.get(task)
            vectorizer = self.vectorizers.get(task)

            if model and vectorizer:
                X = vectorizer.transform([cleaned])
                pred = model.predict(X)[0]
                
                # Convert numeric emotion ID to text if necessary
                if task == "emotion":
                    try:
                        # Attempt to convert to int (handles numpy.int64, etc.)
                        val = int(pred)
                        results[task] = EMOTION_LABELS.get(val, f"unknown({val})")
                    except (ValueError, TypeError):
                        results[task] = pred
                else:
                    results[task] = pred
            else:
                results[task] = "Error: Model not loaded"

        # Compute combined priority score from urgency + emotion
        score, tier = self.compute_priority_score(
            results.get("urgency", "medium"),
            results.get("emotion", "neutral")
        )
        results["priority_score"] = score
        results["priority_tier"]  = tier

        return results

if __name__ == "__main__":
    engine = PriorityEngine()
    tests = [
        "My server is down and I am losing money every second, HELP!",
        "How do I reset my password?",
        "I was double charged, please refund me.",
        "Love the new feature, works great!"
    ]
    print("\n" + "="*55)
    for text in tests:
        r = engine.predict(text)
        print(f"\nText     : {text}")
        print(f"Emotion  : {r['emotion']}")
        print(f"Category : {r['category']}")
        print(f"Urgency  : {r['urgency']}")
        print(f"Score    : {r['priority_score']}/10")
        print(f"Tier     : {r['priority_tier']}")
        print("-"*55)
