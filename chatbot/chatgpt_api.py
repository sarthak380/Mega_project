# from groq import Groq
# from config import OPENAI_MODEL

# client = Groq(api_key="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")

# class ChatGPTBot:

#     def reply(self, message):

#         response = client.chat.completions.create(
#             model="llama3-8b-8192",
#             messages=[
#                 {"role": "system", "content": "You are a helpful restaurant chatbot."},
#                 {"role": "user", "content": message}
#             ]
#         )

#         return response.choices[0].message.content
from groq import Groq

client = Groq(api_key="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")

class ChatGPTBot:

    def reply(self, message):

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful restaurant chatbot."},
                {"role": "user", "content": message}
            ]
        )

        return response.choices[0].message.content
