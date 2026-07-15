# Quick Start Guide

## 5-Minute Setup

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the Application

**On Windows:**

```bash
run.bat
```

**On Linux/Mac:**

```bash
bash run.sh
```

### Step 3: Open in Browser

Once you see the server running, open:

```
http://localhost:5000
```

## Quick Usage

1. **Ask a Question**: Type any question in the chat input box
2. **View FAQs**: Check the sidebar to see all available FAQs
3. **Click FAQ Items**: Click any FAQ in the sidebar to auto-fill it as your question

## Example Questions to Try

- "How do I reset my password?"
- "What shipping options are available?"
- "How do I return an item?"
- "Do you offer a warranty?"
- "What are your payment methods?"
- "How can I track my order?"

## Understanding the Confidence Score

- **90-100%**: Perfect or near-perfect match
- **70-89%**: Good match, likely what you're looking for
- **50-69%**: Possible match, may need refinement
- **Below 50%**: Poor match, try rephrasing your question

## File Descriptions

| File              | Purpose                |
| ----------------- | ---------------------- |
| `app.py`          | Flask API server       |
| `preprocessor.py` | NLP text preprocessing |
| `matcher.py`      | FAQ matching algorithm |
| `faqs.json`       | FAQ database           |
| `index.html`      | Web UI                 |
| `style.css`       | UI styling             |
| `script.js`       | Frontend interactions  |

## API Testing (Optional)

Test the chat endpoint with curl:

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"How do I reset my password?\"}"
```

## Common Issues

### Issue: "Port 5000 already in use"

**Solution**:

- Close other applications using port 5000, or
- Modify the port in `backend/app.py` line: `app.run(debug=True, port=8000)`

### Issue: "No module named 'flask'"

**Solution**: Run `pip install -r requirements.txt` again

### Issue: Frontend not loading

**Solution**: Make sure you're accessing `http://localhost:5000` (not `http://127.0.0.1:5000` in some cases)

## Customization

### Add Custom FAQs

Edit `data/faqs.json` and add new questions/answers:

```json
{
  "id": 11,
  "question": "What is your return policy?",
  "answer": "We offer 30-day returns with original packaging."
}
```

### Change Matching Sensitivity

In `backend/app.py`, adjust the threshold (0.0-1.0):

```python
match = matcher.find_best_match(user_question, threshold=0.5)  # More strict
```

---

**That's it! You're ready to go!** 🚀
