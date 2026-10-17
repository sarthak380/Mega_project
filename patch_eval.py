from pathlib import Path

path = Path('main.py')
text = path.read_text(encoding='utf-8')
old = '''    metrics = evaluate_conversation(conversation, persona_name, task)
    return conversation, bot_type, persona_name, metrics


def get_available_personas():
    """Get list of available persona names"""
    personas, _ = load_data()
    return [p["name"] for p in personas]'''
new = '''    metrics = evaluate_conversation(conversation, persona_name, task)
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
    return [p["name"] for p in personas]'''
if old not in text:
    raise RuntimeError('pattern not found in main.py')
path.write_text(text.replace(old, new), encoding='utf-8')
print('main.py patched')
