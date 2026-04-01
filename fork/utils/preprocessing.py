import re

def clean_text(text):
    """
    Cleans the input text by converting to lowercase and removing 
    all non-alphabetic characters except spaces.
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[^a-zA-Z ]", "", text)
    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text
