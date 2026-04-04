# 🎓 AI Support Priority Engine — Viva Preparation Guide

This document provides a comprehensive overview of the project, including technical architecture, dataset details, mathematical formulas, and implementation logic to help you excel in your Viva/Presentation.

---

## 🚀 1. Project Overview
**Title:** AI-Driven Support Ticket Triage & Priority Scoring System  
**Objective:** To automate the categorization, emotion detection, and urgency assessment of customer support text, providing a unified "Priority Score" (1-10) to optimize response times.

---

## 📁 2. File Directory & Usage

| File / Folder | Purpose |
| :--- | :--- |
| `main.py` | The entry point. Interactive CLI for testing and automatic logging to `results.csv`. |
| `models/` | Contains training scripts and the generated `.pkl` (Pickle) model binaries. |
| `utils/` | Shared logic: `preprocessing.py` (text cleaning) and `priority_engine.py` (the brain). |
| `data/` | The training datasets (Large CSV files). |
| `requirements.txt` | Lists dependencies: `pandas`, `scikit-learn`, `numpy`. |
| `results.csv` | Live database of every analysis performed by the system. |
| `viva.md` | This document (Project study guide). |

---

## 📊 3. Datasets Used & Rationale

We used a **Consolidated Learning** approach, merging multiple datasets to ensure the AI understands different languages and ticket styles:

1. **`customer_support_tickets.csv`**: Provides the baseline for business logic (Ticket Priority vs. Ticket Type).
2. **`dataset-tickets-multi-lang-4-20k.csv`**: A large (20,000+ row) dataset that adds diversity and professional technical language.
3. **`dataset-tickets-german_normalized_50_5_2.csv`**: Used to ensure the model captures technical patterns even in structured/normalized translations.
4. **`goemotions.csv`**: A massive dataset (from Google) with 28 emotion labels, used specifically to make the AI "empathetic."

**Why multiple datasets?**  
To prevent **Overfitting** (the AI only knowing one specific type of ticket) and to increase the **Feature Space** (vocabulary size).

---

## 🧮 4. Mathematical Concepts & Formulas

### A. TF-IDF (Text Vectorization)
Computers can't read text; they read numbers. We use **TF-IDF (Term Frequency-Inverse Document Frequency)** to convert words into vectors.
*   **Formula:** $TF-IDF(t, d) = TF(t, d) \times IDF(t)$
*   **TF (Term Frequency):** Frequency of word $t$ in document $d$.
*   **IDF (Inverse Document Frequency):** $\log\left(\frac{Total Documents}{Documents containing word t}\right)$.
*   **Why?** It highlights "important" words (like "crash", "billing") and ignores common ones ("the", "is").

### B. Logistic Regression (Classification)
We use this algorithm because it is efficient for text classification and provides a probability for each class.
*   **Formula:** $P(y=1|x) = \frac{1}{1 + e^{-(z)}}$ where $z = \beta_0 + \beta_1x_1 + ... + \beta_nx_n$
*   We use the **Softmax function** for multi-class classification (Category and Urgency).

### C. Priority Scoring Formula (Our Internal Logic)
The final "Actionable Score" is calculated using our custom **Heuristic Formula**:
$$Final Score = \text{BaseScore}(\text{Urgency}) + \text{Boost}(\text{Emotion})$$
*   **Base Scores:** Critical=10, High=7, Medium=4, Low=1
*   **Emotion Boosts:** Anger/Fear=+3, Joy/Gratitude=-2
*   **Clamping:** Result is forced between the range $[1, 10]$.

---

## 🛠️ 5. Implementation Workflow

1.  **Preprocessing:** Text is lowercased, special characters are removed, and whitespace is normalized.
2.  **N-Grams:** We use **Bigrams** (2-word pairs). Instead of just reading "not" and "working," the model reads "not working" as a single feature, which is much more accurate.
3.  **Balanced Weights:** Since we have fewer "Critical" tickets than "Low" ones, we use `class_weight='balanced'` in our training logic to ensure the AI doesn't ignore the rare but important cases.
4.  **Pickle Serialization:** After training, models are "frozen" into `.pkl` files. This allows the system to run predictions in milliseconds without retraining every time.

---

## 💡 6. Common Viva Questions

**Q1: Why use TF-IDF instead of Deep Learning (like BERT)?**  
*A: Efficiency. For support tickets, TF-IDF + Logistic Regression is much faster, requires less RAM, and achieved high accuracy on our categorized data without needing a GPU.*

**Q2: How do you handle new, unseen words?**  
*A: The TfidfVectorizer is limited to the top 10,000 most important features found during training. New words are ignored (OOD - Out of Vocabulary), but since our dataset is 36k+ rows, the coverage is extremely high.*

**Q3: What makes your "Priority Score" unique?**  
*A: Most systems only look at the category. Ours looks at the **Sentiment**. If two users have a "Technical Issue," our system prioritizes the one who is "Angry" or "Fearful" over the one who is "Neutral."*

---
*Created for: Data Warehousing and Mining Project*
