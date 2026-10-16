# chateval-pro

A project for evaluating chat models.

## Project Structure

```
chateval-pro/
├── main.py                 # Streamlit UI entry point
├── evaluator.py            # Core evaluation logic
├── test_generator.py       # Generates diverse test cases
├── prompts.py              # All system prompts (evaluation, red team, etc.)
├── models.py               # Pydantic models for structured output
├── utils.py                # Helpers (scoring, tables, etc.)
├── tests/                  # Sample test cases & history
├── requirements.txt
├── .env                    # API keys
└── README.md
```