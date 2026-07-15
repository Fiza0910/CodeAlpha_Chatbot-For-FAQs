import json
import math
from collections import Counter
from preprocessor import TextPreprocessor


class CosineSimilarityMatcher:
    """Matches user questions to FAQs using cosine similarity"""
    
    def __init__(self, faqs_path):
        self.preprocessor = TextPreprocessor()
        self.faqs = self.load_faqs(faqs_path)
        self.processed_faqs = self.preprocess_faqs()
    
    def load_faqs(self, faqs_path):
        """Load FAQs from JSON file"""
        with open(faqs_path, 'r') as file:
            data = json.load(file)
        return data.get('faqs', [])
    
    def preprocess_faqs(self):
        """Preprocess all FAQ questions"""
        processed = []
        for faq in self.faqs:
            tokens = self.preprocessor.preprocess(faq['question'])
            processed.append({
                'id': faq['id'],
                'question': faq['question'],
                'answer': faq['answer'],
                'tokens': tokens
            })
        return processed
    
    def vectorize(self, tokens):
        """Convert tokens to a frequency vector"""
        return Counter(tokens)
    
    def cosine_similarity(self, vec1, vec2):
        """
        Calculate cosine similarity between two vectors
        Returns a value between 0 and 1
        """
        # Get all unique words
        all_words = set(vec1.keys()) | set(vec2.keys())
        
        if not all_words:
            return 0.0
        
        # Calculate dot product
        dot_product = sum(vec1.get(word, 0) * vec2.get(word, 0) for word in all_words)
        
        # Calculate magnitudes
        mag1 = math.sqrt(sum(count ** 2 for count in vec1.values()))
        mag2 = math.sqrt(sum(count ** 2 for count in vec2.values()))
        
        # Avoid division by zero
        if mag1 == 0 or mag2 == 0:
            return 0.0
        
        # Calculate cosine similarity
        similarity = dot_product / (mag1 * mag2)
        return similarity
    
    def find_best_match(self, user_question, threshold=0.3):
        """
        Find the best matching FAQ for a user question
        
        Args:
            user_question: The user's question string
            threshold: Minimum similarity score (0-1) to consider a match
        
        Returns:
            Dictionary with 'id', 'question', 'answer', and 'similarity_score'
            or None if no match found above threshold
        """
        # Preprocess user question
        user_tokens = self.preprocessor.preprocess(user_question)
        user_vector = self.vectorize(user_tokens)
        
        best_match = None
        best_score = 0
        
        # Compare with each FAQ
        for faq in self.processed_faqs:
            faq_vector = self.vectorize(faq['tokens'])
            similarity = self.cosine_similarity(user_vector, faq_vector)
            
            if similarity > best_score:
                best_score = similarity
                best_match = {
                    'id': faq['id'],
                    'question': faq['question'],
                    'answer': faq['answer'],
                    'similarity_score': round(similarity, 4)
                }
        
        # Return match only if it meets the threshold
        if best_score >= threshold:
            return best_match
        
        return None
    
    def get_top_matches(self, user_question, top_k=3, threshold=0.1):
        """
        Get top K matching FAQs for a user question
        
        Args:
            user_question: The user's question string
            top_k: Number of top matches to return
            threshold: Minimum similarity score
        
        Returns:
            List of dictionaries with match information, sorted by similarity score
        """
        # Preprocess user question
        user_tokens = self.preprocessor.preprocess(user_question)
        user_vector = self.vectorize(user_tokens)
        
        matches = []
        
        # Compare with each FAQ
        for faq in self.processed_faqs:
            faq_vector = self.vectorize(faq['tokens'])
            similarity = self.cosine_similarity(user_vector, faq_vector)
            
            if similarity >= threshold:
                matches.append({
                    'id': faq['id'],
                    'question': faq['question'],
                    'answer': faq['answer'],
                    'similarity_score': round(similarity, 4)
                })
        
        # Sort by similarity score (descending) and return top K
        matches.sort(key=lambda x: x['similarity_score'], reverse=True)
        return matches[:top_k]
