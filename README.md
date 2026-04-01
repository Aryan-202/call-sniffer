# Priority AI: Intelligent Emergency & Emotion Classification

Priority AI is a modular machine learning system designed to analyze text (such as emergency calls or user feedback) and classify it across three dimensions: **Emotion**, **Domain Category**, and **Urgency**.

## 🚀 Features

- **Emotion Detection**: Classifies text using fine-tuned models trained on the `GoEmotions` dataset.
- **Category Classification**: Identifies the domain (e.g., EMS, Fire, Police) using 911 call data.
- **Urgency Scoring**: Prioritizes situations into Low, Medium, and High urgency levels.
- **Modular Architecture**: Clean, class-based trainers and predictors for easy maintenance.
- **Shared Utilities**: Unified preprocessing pipeline for consistent data handling.

## 📁 Project Structure

```text
priority_ai/
├── data/               # Project datasets (not tracked in Git)
├── models/             # Model training scripts and saved artifacts (.pkl)
│   ├── emotion_model.py
│   ├── category_model.py
│   └── urgency_model.py
├── utils/              # Shared helper functions
│   └── preprocessing.py
├── main.py             # Entry point for the application
└── requirements.txt    # Python dependencies
```

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Data-Warehousing-and-Mining-Project/priority_ai
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 📈 Training the Models

To train the models from scratch, ensure you have the required datasets in the `priority_ai/data/` directory, then run the training scripts.

### Using PowerShell:
```powershell
$env:PYTHONPATH="priority_ai"
.\priority_ai\venv\Scripts\python.exe .\priority_ai\models\emotion_model.py
.\priority_ai\venv\Scripts\python.exe .\priority_ai\models\category_model.py
.\priority_ai\venv\Scripts\python.exe .\priority_ai\models\urgency_model.py
```

### Using CMD:
```cmd
set PYTHONPATH=priority_ai
priority_ai\venv\Scripts\python.exe priority_ai\models\emotion_model.py
priority_ai\venv\Scripts\python.exe priority_ai\models\category_model.py
priority_ai\venv\Scripts\python.exe priority_ai\models\urgency_model.py
```

## 🚀 Running the Application

Once the models are trained, use the main entry point to start the interactive AI system.

### Using PowerShell:
```powershell
$env:PYTHONPATH="priority_ai"
.\priority_ai\venv\Scripts\python.exe .\priority_ai\main.py
```

### Using CMD:
```cmd
set PYTHONPATH=priority_ai
priority_ai\venv\Scripts\python.exe priority_ai\main.py
```

## 📝 Dependencies

- `pandas`: Data manipulation
- `scikit-learn`: Machine learning algorithms and utilities
- `pickle`: Model serialization
