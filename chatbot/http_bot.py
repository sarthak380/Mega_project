import os
from groq import Groq

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY",
    "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"
)
MODEL_NAME = "llama-3.1-8b-instant"
client = Groq(api_key=GROQ_API_KEY)

class HTTPRestaurantBot:

    def __init__(self):
        self.system_prompt = (
            "You are a restaurant assistant helping a customer place an order. "
            "Use friendly and concise language, confirm item names clearly, "
            "and keep the interaction focused on ordering food."
        )

    def reply(self, message):
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.6
        )
        return response.choices[0].message.content.strip()


class EducationalConsultantBot:

    def __init__(self):
        self.system_prompt = (
            "You are an educational consultant chatbot providing study guidance, "
            "learning strategies, and clear explanations. Be supportive, patient, "
            "and help the user understand concepts step by step."
        )

    def reply(self, message):
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()


# Compatibility alias for legacy imports
HTTPBot = HTTPRestaurantBot
