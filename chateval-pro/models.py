import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
# Initialize the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# When calling the model:
completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile", # or another Groq model
    messages=[{"role": "user", "content": "What is Encapsulation?"}]
)