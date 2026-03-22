import json
from config import MAX_TURNS
from chatbot.chatgpt_api import ChatGPTBot
from chatbot.http_bot import HTTPBot

def load_data():

    with open("data/personas.json") as f:
        personas=json.load(f)

    with open("data/tasks.json") as f:
        tasks=json.load(f)

    return personas,tasks

def run_simulation(bot_type="ChatGPT"):

    personas,tasks=load_data()

    persona=personas[0]

    task=tasks[0]

    if bot_type=="ChatGPT":
        bot=ChatGPTBot()
    else:
        bot=HTTPBot()

    conversation=[]

    message="Hello"

    for i in range(MAX_TURNS):

        reply=bot.reply(message)

        conversation.append((message,reply))

        message="Tell me more about menu"

    return conversation,bot_type