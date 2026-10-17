import json
from pathlib import Path
from config import MAX_TURNS
from chatbot.multi_agent_system import create_persona_agent
from chatbot.http_bot import HTTPRestaurantBot, EducationalConsultantBot
from chatbot.evaluation import evaluate_conversation

def load_data():
    root = Path(__file__).resolve().parent
    data_dir = root / "data"

    with open(data_dir / "personas.json", encoding="utf-8") as f:
        personas = json.load(f)

    with open(data_dir / "tasks.json", encoding="utf-8") as f:
        tasks = json.load(f)

    return personas, tasks

def run_simulation(bot_type="ChatGPT", persona_name="Confused Customer"):
    """
    Run simulation with specified bot type and persona
    """
    personas, tasks = load_data()

    # Find the selected persona
    persona = next((p for p in personas if p["name"] == persona_name), personas[0])
    task = tasks[0]  # Use first task for now

    if bot_type == "ChatGPT":
        bot = create_persona_agent(persona_name)
    elif bot_type == "HTTPRestaurantBot":
        bot = HTTPRestaurantBot()
    elif bot_type == "EducationalConsultantBot":
        bot = EducationalConsultantBot()
    else:
        bot = HTTPRestaurantBot()

    conversation = []
    restaurant_messages = [
        "Hello! Welcome to our restaurant. How can I help you today?",
        "Could you tell me more about our menu options?",
        "What would you like to order?",
        "Would you like anything else with that?",
        "Can I help you with any customizations or special requests?",
        "Do you want any side items or desserts with your meal?",
        "Which drink would you like to go with your order?",
        "Would you like me to repeat the order summary?",
        "Is everything correct before I send this to the kitchen?",
        "Thank you for your order. Anything else I can help you with?"
    ]

    for i in range(MAX_TURNS):
        message = restaurant_messages[i] if i < len(restaurant_messages) else restaurant_messages[-1]

        if hasattr(bot, 'reply'):
            if bot_type == "ChatGPT":
                reply = bot.reply(message, task)
            else:
                reply = bot.reply(message)
        else:
            reply = "Bot not available"

        conversation.append((message, reply))

    metrics = evaluate_conversation(conversation, persona_name, task)
    return conversation, bot_type, persona_name, metrics

def generate_evaluation_conclusion(results):
    """Generate a human-readable conclusion for a set of persona evaluation results."""
    if not results:
        return "No persona evaluation results were generated."

    average = lambda key: sum(item["metrics"][key] for item in results) / len(results)
    avg_pas = int(average("PAS"))
    avg_bvs = int(average("BVS"))
    avg_tra = int(average("TRA"))
    avg_dei = int(average("DEI"))
    avg_crrs = int(average("CRRS"))

    best_persona = max(results, key=lambda item: item["metrics"]["CRRS"])
    worst_persona = min(results, key=lambda item: item["metrics"]["CRRS"])

    conclusion = (
        f"The chatbot evaluation across {len(results)} personas shows an overall average CRRS of {avg_crrs}%. "
        f"Persona adherence is currently averaging {avg_pas}%, behavioral variety is {avg_bvs}%, task completion accuracy is {avg_tra}%, "
        f"and explainability is {avg_dei}%. The strongest persona performance was for '{best_persona['persona']}' ({best_persona['metrics']['CRRS']}%), "
        f"while the weakest performance was for '{worst_persona['persona']}' ({worst_persona['metrics']['CRRS']}%). "
        "To improve the evaluation chatbot, focus on strengthening persona adherence and decision explainability across diverse customer styles."
    )
    return conclusion


def run_full_persona_evaluation(bot_type="ChatGPT"):
    personas, _ = load_data()
    results = []

    for persona in personas:
        conversation, _, persona_name, metrics = run_simulation(bot_type, persona["name"])
        results.append({
            "persona": persona_name,
            "conversation": conversation,
            "metrics": metrics
        })

    conclusion = generate_evaluation_conclusion(results)
    return results, conclusion


def get_available_personas():
    """Get list of available persona names"""
    personas, _ = load_data()
    return [p["name"] for p in personas]