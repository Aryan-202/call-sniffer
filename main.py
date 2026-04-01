import sys
import os
import csv
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.priority_engine import PriorityEngine

def save_to_csv(results, file_path="results.csv"):
    """Appends prediction results to a CSV file."""
    file_exists = os.path.isfile(file_path)
    
    # Prepare data row with timestamp
    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "original_text": results["original_text"],
        "emotion": results["emotion"],
        "category": results["category"],
        "urgency": results["urgency"],
        "priority_score": results["priority_score"],
        "priority_tier": results["priority_tier"]
    }
    
    with open(file_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

def main():
    print("="*50)
    print("      SYSTEM INITIALIZATION: PRIORITY AI")
    print("="*50)
    
    try:
        engine = PriorityEngine()
    except Exception as e:
        print(f"Failed to initialize models: {e}")
        return

    print("\nModels loaded successfully. System ready.")
    print("Results will be saved to 'results.csv'")
    print("Type 'exit' to quit.\n")

    while True:
        text = input("Enter text to analyze: ").strip()
        
        if text.lower() in ['exit', 'quit']:
            break
            
        if not text:
            continue

        results = engine.predict(text)
        
        # Save to CSV
        save_to_csv(results)
        
        print("\n" + "-"*40)
        print(f"ANAYLSIS RESULTS (Saved to CSV)")
        print("-"*40)
        print(f"Emotion  : {results['emotion'].capitalize()}")
        print(f"Category : {results['category'].capitalize()}")
        print(f"Urgency  : {results['urgency'].upper()}")
        print(f"Score    : {results['priority_score']}/10")
        print(f"Tier     : {results['priority_tier']}")
        print("-"*40 + "\n")

if __name__ == "__main__":
    main()
