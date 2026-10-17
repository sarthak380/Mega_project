import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.title("🍽️ AI Restaurant Chatbot")
    st.error("Missing GROQ_API_KEY in .env")
    st.stop()

# Groq client
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

st.title("🍽️ AI Restaurant Chatbot")

# Menu
menu = {
    "pizza": 200,
    "burger": 100,
    "pasta": 150,
    "coke": 50
}

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "cart" not in st.session_state:
    st.session_state.cart = []

# Show chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Input
user_input = st.chat_input("Type your message...")

def calculate_total():
    return sum(menu[item] for item in st.session_state.cart)

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Add to cart
    for item in menu:
        if item in user_input.lower():
            st.session_state.cart.append(item)

    system_prompt = f"""
    You are a smart restaurant chatbot 🍽️.
    Menu: {menu}

    Rules:
    - Be friendly
    - Help user order food
    - Suggest items
    - Answer clearly
    """

    # ✅ FIXED MODEL
    response = client.chat.completions.create(
         model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            *st.session_state.messages
        ]
    )

    bot_reply = response.choices[0].message.content

    # Bill
    if "bill" in user_input.lower():
        total = calculate_total()
        bot_reply += f"\n\n🧾 Total Bill: ₹{total}"

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.chat_message("assistant").write(bot_reply)