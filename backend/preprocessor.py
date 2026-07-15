import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

try:
    nltk.data.find('corpora/omw-1.4')
except LookupError:
    nltk.download('omw-1.4')


class TextPreprocessor:
    """Preprocesses text for FAQ matching"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.punctuation = string.punctuation
    
    def clean_text(self, text):
        """
        Clean text by converting to lowercase and removing extra whitespace
        """
        return text.lower().strip()
    
    def tokenize(self, text):
        """
        Tokenize text into words
        """
        return word_tokenize(text)
    
    def remove_punctuation(self, tokens):
        """
        Remove punctuation from tokens
        """
        return [token for token in tokens if token not in self.punctuation]
    
    def remove_stopwords(self, tokens):
        """
        Remove common stopwords
        """
        return [token for token in tokens if token not in self.stop_words]
    
    def lemmatize(self, tokens):
        """
        Lemmatize tokens to their base form
        """
        return [self.lemmatizer.lemmatize(token) for token in tokens]
    
    def preprocess(self, text):
        """
        Complete preprocessing pipeline
        """
        # Clean text
        text = self.clean_text(text)
        
        # Tokenize
        tokens = self.tokenize(text)
        
        # Remove punctuation
        tokens = self.remove_punctuation(tokens)
        
        # Remove stopwords
        tokens = self.remove_stopwords(tokens)
        
        # Lemmatize
        tokens = self.lemmatize(tokens)
        
        return tokens
