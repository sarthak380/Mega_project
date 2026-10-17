# 🍽️ 🤖 AI Restaurant Chatbot (Streamlit)

## 🎯 What This Project Will Do
- Talk like a real waiter
- Show menu
- Take orders in natural language
- Suggest food
- Calculate bill

## 📦 Requirements
Install libraries:
```
pip install -r requirements.txt
```

## 🔑 Get API Key
1. Go to Groq website (https://groq.com/)
2. Create API key
3. Update the `.env` file with your API key:
```
GROQ_API_KEY=your_actual_groq_api_key_here
```

## ▶️ Run the App
```
streamlit run app.py
```

## 💬 Example Conversation
- You: Hi
- Bot: Welcome! What would you like to order? 😊

- You: I want pizza and coke
- Bot: Great choice! Anything else?

- You: show bill
- Bot: 🧾 Total Bill: ₹250

## 🔥 Advanced Features (Add Later)
- ✅ Smart Suggestions ("People also order burger with pizza")
- ✅ Order Confirmation (Ask name, address)
- ✅ Database (MySQL) (Store orders)
- ✅ Voice Chat (Speech-to-text)

## 🧠 Important Concept
Combining:
- Streamlit → UI
- Groq API → Brain
- Python Logic → Order handling