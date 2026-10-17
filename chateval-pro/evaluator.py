import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Dict

# 1. Load environment variables from .env
load_dotenv()

# 2. Update client to point to Groq
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")
)

class MetricScore(BaseModel):
    score: int
    justification: str

class EvaluationResult(BaseModel):
    accuracy: MetricScore
    relevance: MetricScore
    clarity: MetricScore
    completeness: MetricScore
    safety: MetricScore
    consistency: MetricScore
    overall_score: float
    strengths: list[str]
    weaknesses: list[str]
    suggested_improvements: list[str]

def evaluate_response(test_prompt: str, chatbot_response: str, context: str = "") -> Dict:
    # Ensure EVALUATION_PROMPT is imported or defined above
    full_prompt = EVALUATION_PROMPT.format(
        test_prompt=test_prompt,
        response=chatbot_response
    )
    
    # 3. Change model to a Groq-supported model (like llama-3.3-70b-versatile)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", 
        messages=[{"role": "system", "content": "You are a strict QA evaluator."},
                  {"role": "user", "content": full_prompt}],
        temperature=0.3,
        response_format={"type": "json_object"}
    )
    
    result = json.loads(response.choices[0].message.content)
    return result