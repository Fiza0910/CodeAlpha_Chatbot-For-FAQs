// API base URL
const API_URL = 'http://localhost:5000/api';

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    initializeTheme();
    loadFAQs();
});

/** Set up light/dark mode and remember the visitor's preference. */
function initializeTheme() {
    const themeToggle = document.getElementById('themeToggle');
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    applyTheme(savedTheme || (prefersDark ? 'dark' : 'light'));

    themeToggle.addEventListener('click', function() {
        const nextTheme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
        applyTheme(nextTheme);
        localStorage.setItem('theme', nextTheme);
    });
}

function applyTheme(theme) {
    const themeToggle = document.getElementById('themeToggle');
    const isDark = theme === 'dark';

    document.documentElement.dataset.theme = theme;
    themeToggle.innerHTML = `<span aria-hidden="true">${isDark ? '☀' : '☾'}</span>`;
    themeToggle.setAttribute('aria-label', `Switch to ${isDark ? 'light' : 'dark'} mode`);
    themeToggle.title = `Switch to ${isDark ? 'light' : 'dark'} mode`;
}

/**
 * Send message and get chatbot response
 */
function sendMessage(event) {
    event.preventDefault();
    
    const userInput = document.getElementById('userInput');
    const question = userInput.value.trim();
    
    if (!question) return;
    
    // Add user message to UI
    addMessageToUI(question, 'user-message');
    userInput.value = '';
    
    // Disable send button
    const sendBtn = document.querySelector('.send-btn');
    sendBtn.disabled = true;
    
    // Send to server
    fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: question })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Build bot message with confidence and matched question
            let messageText = data.answer;
            let metaInfo = '';
            
            if (data.matched_question) {
                metaInfo += `<div class="matched-question"><strong>Matched:</strong> "${data.matched_question}"</div>`;
            }
            
            if (data.confidence !== undefined) {
                metaInfo += `<div class="message-meta"><strong>Confidence:</strong> <span class="confidence">${(data.confidence * 100).toFixed(1)}%</span></div>`;
            }
            
            addMessageToUI(messageText + metaInfo, 'bot-message', true);
        } else {
            addMessageToUI(data.answer, 'bot-message');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        addMessageToUI('Sorry, an error occurred. Please try again.', 'bot-message');
    })
    .finally(() => {
        sendBtn.disabled = false;
        userInput.focus();
    });
}

/**
 * Add message to the chat UI
 */
function addMessageToUI(message, messageClass, isHTML = false) {
    const messageContainer = document.getElementById('messageContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${messageClass}`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    if (isHTML) {
        messageContent.innerHTML = message;
    } else {
        messageContent.textContent = message;
    }
    
    messageDiv.appendChild(messageContent);
    messageContainer.appendChild(messageDiv);
    
    // Auto scroll to bottom
    messageContainer.scrollTop = messageContainer.scrollHeight;
}

/**
 * Load and display FAQs in the sidebar
 */
function loadFAQs() {
    fetch(`${API_URL}/faqs`)
    .then(response => response.json())
    .then(data => {
        const faqList = document.getElementById('faqList');
        faqList.innerHTML = '';
        
        if (data.faqs && data.faqs.length > 0) {
            data.faqs.forEach(faq => {
                const faqItem = document.createElement('div');
                faqItem.className = 'faq-item';
                faqItem.innerHTML = `
                    <div class="faq-item-question">${faq.question}</div>
                    <div class="faq-item-answer">${faq.answer}</div>
                `;
                
                // Click to use in chat
                faqItem.addEventListener('click', function() {
                    document.getElementById('userInput').value = faq.question;
                    document.getElementById('userInput').focus();
                });
                
                faqList.appendChild(faqItem);
            });
        } else {
            faqList.innerHTML = '<p class="error-message">No FAQs available</p>';
        }
    })
    .catch(error => {
        console.error('Error loading FAQs:', error);
        document.getElementById('faqList').innerHTML = '<p class="error-message">Failed to load FAQs</p>';
    });
}

/**
 * Search FAQs (optional utility function)
 */
function searchFAQs(query) {
    if (!query.trim()) return;
    
    fetch(`${API_URL}/search`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success && data.matches) {
            console.log('Search results:', data.matches);
            // You can use this to update UI with search results
        }
    })
    .catch(error => {
        console.error('Search error:', error);
    });
}
