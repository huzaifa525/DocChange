from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk

class TextProcessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        # Download necessary NLTK data
        nltk.download('punkt')
        nltk.download('wordnet')

    def preprocess(self, text: str) -> str:
        tokens = word_tokenize(text)
        lemmatized_tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        return ' '.join(lemmatized_tokens)