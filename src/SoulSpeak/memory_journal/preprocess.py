import re

def preprocess(text: str) -> str:
    """
    Clean user input before emotional analysis.
    - Lowercase the text
    - Remove leading/trailing spaces
    - Strip URLs and non-basic characters
    """
    text = text.strip().lower()
    text = re.sub(r'https?://\S+', '', text)  # Remove links
    text = re.sub(r'[^\w\s.,!?\'\"-]', '', text)  # Keep standard punctuation
    return text