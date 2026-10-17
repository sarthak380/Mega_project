import re
from typing import Dict, List

PERSONA_KEYWORDS = {
    "Frustrated Customer": ["frustrated", "annoyed", "impatient", "hurry", "rush", "simple", "no nonsense"],
    "Happy Customer": ["happy", "great", "awesome", "thanks", "please", "enjoy", "love", "friendly"],
    "Confused Customer": ["confused", "not sure", "which", "what", "maybe", "question", "clarify", "help", "uncertain", "overwhelmed"]
}

EXPLANATION_WORDS = [
    "because",
    "therefore",
    "so",
    "thus",
    "since",
    "hence",
    "because of",
    "as a result",
    "that is why",
    "reason"
]

STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "if", "is", "are", "was", "were", "to", "of", "in", "for", "on", "with",
    "it", "this", "that", "as", "at", "from", "by", "so", "we", "you", "your"
}


def normalize_text(text: str) -> str:
    return re.sub(r"[^a-z0-9\s]", "", text.lower())


def tokenize(text: str) -> List[str]:
    return [word for word in normalize_text(text).split() if word and word not in STOP_WORDS]


def persona_adherence_score(persona_name: str, responses: List[str]) -> int:
    keywords = PERSONA_KEYWORDS.get(persona_name, [])
    if not responses or not keywords:
        return 50

    text = " ".join(responses)
    matches = sum(1 for keyword in keywords if keyword in normalize_text(text))
    score = int(min(100, max(0, (matches / len(keywords)) * 100)))
    return score


def behavioral_variance_score(responses: List[str]) -> int:
    if len(responses) < 2:
        return 50

    token_sets = [set(tokenize(resp)) for resp in responses if resp.strip()]
    if len(token_sets) < 2:
        return 50

    similarities = []
    for first, second in zip(token_sets, token_sets[1:]):
        if not first or not second:
            similarities.append(0.0)
            continue
        intersection = first.intersection(second)
        union = first.union(second)
        similarities.append(len(intersection) / len(union))

    avg_similarity = sum(similarities) / len(similarities)
    variance = 1.0 - avg_similarity
    score = int(min(100, max(0, variance * 100 + 20)))
    return score


def extract_items_from_text(text: str, known_items: List[str]) -> List[str]:
    normalized = normalize_text(text)
    return [item for item in known_items if item in normalized]


def task_restriction_adherence(conversation: List[tuple], target_items: List[str]) -> Dict[str, float]:
    customer_responses = [reply for _, reply in conversation]
    predicted_items = set(extract_items_from_text(" ".join(customer_responses), target_items))
    actual_items = set(target_items)

    true_positives = len(predicted_items.intersection(actual_items))
    precision = true_positives / max(1, len(predicted_items))
    recall = true_positives / max(1, len(actual_items))
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

    return {
        "precision": round(precision, 2),
        "recall": round(recall, 2),
        "f1": int(f1 * 100),
        "predicted_items": sorted(predicted_items),
        "target_items": sorted(actual_items)
    }


def decision_explainability_index(conversation: List[tuple]) -> int:
    if not conversation:
        return 50

    explanation_count = 0
    for _, reply in conversation:
        lowered = normalize_text(reply)
        if any(word in lowered for word in EXPLANATION_WORDS):
            explanation_count += 1

    score = min(100, 30 + explanation_count * 15)
    return score


def composite_realism_score(scores: Dict[str, int]) -> int:
    if not scores:
        return 0
    included = [value for key, value in scores.items() if key in {"PAS", "BVS", "TRA", "DEI"}]
    if not included:
        return 0
    return int(sum(included) / len(included))


def evaluate_conversation(conversation: List[tuple], persona_name: str, target_task: dict) -> Dict[str, object]:
    customer_responses = [reply for _, reply in conversation]
    pas = persona_adherence_score(persona_name, customer_responses)
    bvs = behavioral_variance_score(customer_responses)
    tra_data = task_restriction_adherence(conversation, target_task.get("items", []))
    tra = tra_data["f1"]
    dei = decision_explainability_index(conversation)
    crrs = composite_realism_score({"PAS": pas, "BVS": bvs, "TRA": tra, "DEI": dei})

    metrics = {
        "PAS": pas,
        "BVS": bvs,
        "TRA": tra,
        "DEI": dei,
        "CRRS": crrs,
        "order_predicted": tra_data["predicted_items"],
        "order_target": tra_data["target_items"]
    }
    return metrics
