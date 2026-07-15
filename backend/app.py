import os
import sys
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from matcher import CosineSimilarityMatcher

app = Flask(__name__, template_folder='../frontend', static_folder='../frontend/static')
CORS(app)

# Initialize the matcher with FAQ data
faq_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'faqs.json')
matcher = CosineSimilarityMatcher(faq_path)


@app.route('/')
def home():
    """Serve the main chat UI"""
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    API endpoint for chatbot responses
    Expects JSON: {"question": "user's question"}
    """
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({'error': 'No question provided'}), 400
        
        user_question = data['question'].strip()
        
        if not user_question:
            return jsonify({'error': 'Question cannot be empty'}), 400
        
        # Find the best matching FAQ
        match = matcher.find_best_match(user_question, threshold=0.2)
        
        if match:
            return jsonify({
                'success': True,
                'answer': match['answer'],
                'matched_question': match['question'],
                'confidence': match['similarity_score'],
                'type': 'answer'
            })
        else:
            return jsonify({
                'success': False,
                'answer': 'I could not find a relevant answer to your question. Please try rephrasing it or contact our support team.',
                'type': 'no_match'
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/faqs', methods=['GET'])
def get_faqs():
    """Get all FAQs"""
    try:
        with open(faq_path, 'r') as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/search', methods=['POST'])
def search():
    """
    Search endpoint for multiple matching FAQs
    Expects JSON: {"query": "search query"}
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({'error': 'No query provided'}), 400
        
        query = data['query'].strip()
        
        if not query:
            return jsonify({'error': 'Query cannot be empty'}), 400
        
        # Get top matches
        matches = matcher.get_top_matches(query, top_k=5, threshold=0.1)
        
        return jsonify({
            'success': True,
            'query': query,
            'matches': matches,
            'count': len(matches)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'FAQ Chatbot API is running'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
