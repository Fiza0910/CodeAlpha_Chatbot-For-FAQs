# FAQ Chatbot Application

A smart FAQ chatbot that matches user questions to the most relevant FAQ answers using NLP and cosine similarity.

## Features

- **NLP Preprocessing**: Tokenization, stopword removal, and lemmatization using NLTK
- **Cosine Similarity Matching**: Intelligent question matching algorithm
- **REST API**: Flask backend with multiple endpoints
- **Modern Web UI**: Responsive HTML/CSS/JS frontend
- **FAQ Sidebar**: Quick access to all available FAQs
- **Confidence Scoring**: Shows how confident the chatbot is in its answer
- **Multiple Results**: Can return top K matching FAQs

## Project Structure

```
code_alpha_chatbotForFAQ/
├── backend/
│   ├── __init__.py
│   ├── app.py              # Flask application and API endpoints
│   ├── preprocessor.py     # Text preprocessing module
│   └── matcher.py          # FAQ matching algorithm
├── frontend/
│   ├── index.html          # Main chat UI
│   └── static/
│       ├── style.css       # Styling
│       └── script.js       # Frontend logic
├── data/
│   └── faqs.json           # FAQ database
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
cd d:\code_alpha_chatbotForFAQ
pip install -r requirements.txt
```

This will install:

- Flask (web framework)
- Flask-CORS (cross-origin support)
- NLTK (natural language toolkit)

### Step 2: Download NLTK Data

The NLTK data is automatically downloaded when you first run the application. However, you can manually download it:

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
```

## Running the Application

### Start the Backend Server

```bash
cd backend
python app.py
```

The server will start at `http://localhost:5000`

You should see:

```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### Access the Frontend

Open your browser and navigate to:

```
http://localhost:5000
```

## API Endpoints

### 1. Chat Endpoint

**POST** `/api/chat`

Request:

```json
{
  "question": "How do I reset my password?"
}
```

Response:

```json
{
  "success": true,
  "answer": "To reset your password, click on 'Forgot Password' on the login page...",
  "matched_question": "How do I reset my password?",
  "confidence": 0.9876,
  "type": "answer"
}
```

### 2. Get All FAQs

**GET** `/api/faqs`

Response:

```json
{
  "faqs": [
    {
      "id": 1,
      "question": "How do I reset my password?",
      "answer": "To reset your password..."
    },
    ...
  ]
}
```

### 3. Search FAQs

**POST** `/api/search`

Request:

```json
{
  "query": "payment methods"
}
```

Response:

```json
{
  "success": true,
  "query": "payment methods",
  "matches": [
    {
      "id": 3,
      "question": "What payment methods do you accept?",
      "answer": "We accept credit cards...",
      "similarity_score": 0.8234
    },
    ...
  ],
  "count": 3
}
```

### 4. Health Check

**GET** `/api/health`

Response:

```json
{
  "status": "healthy",
  "message": "FAQ Chatbot API is running"
}
```

## How It Works

### 1. Text Preprocessing

The `TextPreprocessor` class handles:

- Text cleaning (lowercase, trim whitespace)
- Tokenization (split into words)
- Punctuation removal
- Stopword removal (common words like "the", "a")
- Lemmatization (convert to base form)

### 2. Similarity Matching

The `CosineSimilarityMatcher` class:

- Converts text to frequency vectors
- Calculates cosine similarity between user question and FAQ questions
- Returns the best match above a confidence threshold (default: 0.2)
- Can return top K matches sorted by confidence

### 3. Confidence Score

Ranges from 0 to 1:

- 0.0 = no similarity
- 1.0 = perfect match
- Below 0.2 (default threshold) = "I don't know" response

## Customization

### Add New FAQs

Edit `data/faqs.json` and add new Q&A pairs:

```json
{
  "id": 11,
  "question": "Your question here?",
  "answer": "Your answer here."
}
```

### Adjust Confidence Threshold

In `backend/app.py`, modify the threshold parameter:

```python
match = matcher.find_best_match(user_question, threshold=0.3)  # 30% confidence
```

### Change Port

In `backend/app.py`, modify the port:

```python
app.run(debug=True, port=8000)  # Change from 5000 to 8000
```

## Example Usage

1. **User asks**: "How do I change my password?"
2. **Chatbot preprocessing**: Removes stopwords, lemmatizes to "change password"
3. **Matching**: Compares with all FAQs using cosine similarity
4. **Result**: Finds high match with "How do I reset my password?" (89% confidence)
5. **Response**: Returns the matching answer

## Technologies Used

- **Backend**: Python, Flask, NLTK
- **Frontend**: HTML, CSS, JavaScript
- **Database**: JSON file
- **NLP**: NLTK (Natural Language Toolkit)
- **Similarity**: Cosine Similarity (TF-IDF concept)

## Limitations & Future Improvements

### Current Limitations

- FAQ database stored in JSON file (no persistence)
- Single-turn conversations (no conversation history)
- English language only
- No sentiment analysis
- No context awareness across multiple questions

### Future Enhancements

- [ ] Add database support (SQLite, MongoDB)
- [ ] Implement conversation history
- [ ] Multi-language support
- [ ] Intent recognition
- [ ] Feedback mechanism to improve accuracy
- [ ] Admin dashboard to manage FAQs
- [ ] Chat history export
- [ ] Suggested questions based on user input
- [ ] Integration with external APIs

## Troubleshooting

### Port Already in Use

If port 5000 is already in use:

```bash
# Find process using port 5000 (Windows)
netstat -ano | findstr :5000

# Kill the process (replace PID with the actual process ID)
taskkill /PID <PID> /F
```

### NLTK Data Not Found

If you get NLTK data errors:

```python
import nltk
nltk.download('all')
```

### CORS Errors

The application uses Flask-CORS to handle cross-origin requests. If you still see errors, check that the frontend is accessing the correct API URL.

## License

This project is open source and available for educational and commercial use.

## Support

For issues, questions, or suggestions, please reach out to the development team.

---

**Version**: 1.0  
**Last Updated**: 2024  
**Created for**: FAQ Chatbot Task
