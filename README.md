# Mega Project: Multi-Agent Persona Control System

## Overview

This project implements a **three-agent framework for realistic user simulation** in interactive scenarios, based on the research paper *"Agentic Persona Control and Task State Tracking for Realistic User Simulation in Interactive Scenarios"*.

The system simulates restaurant customers with distinct personas using specialized AI agents that coordinate to create realistic, explainable, and controllable conversational behavior.

## 🏗️ Architecture

### Three-Agent Framework

#### 🤖 **User Agent (Orchestrator)**
- **Role**: Main coordinator that generates customer responses
- **Function**: Combines message input, task state, and behavioral attributes
- **Protocol**: Invokes sub-agents in sequence (State Tracking → Message Attributes → Response Generation)

#### 📊 **State Tracking Agent**
- **Role**: Maintains structured task state during conversations
- **Tracks**: `Tcurrent` (confirmed items) and `Ttarget` (target items)
- **Function**: Updates order state based on conversation progress using LLM analysis

#### 🎭 **Message Attributes Generation Agent**
- **Role**: Controls conversational attributes based on persona and task progress
- **Attributes**:
  - `mood_tone`: casual, frustrated, confused, enthusiastic
  - `task_execution_style`: one-by-one, all-at-once
  - `exploration_style`: explores, does-not-explore
  - `task_completion_status`: complete, incomplete

## 👥 Available Personas

### � **Confused Customer**
- **Biography**: A customer who gets easily overwhelmed by choices and needs clarification on menu items, options, and processes.
- **Mood**: Confused, questioning
- **Style**: One-by-one task execution
- **Exploration**: Explores while seeking reassurance and guidance

### 😡 **Frustrated Customer**
- **Biography**: A customer who gets easily frustrated by complex menus and slow service.
- **Mood**: Frustrated, impatient
- **Style**: Direct, one-by-one task execution
- **Exploration**: Prefers quick order completion and minimal extra detail

### 😊 **Happy Customer**
- **Biography**: A cheerful customer who enjoys exploring menu options and chatting with staff.
- **Mood**: Enthusiastic, friendly
- **Style**: All-at-once task execution
- **Exploration**: Explores menu options and responds positively

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Groq API key (for Llama model access)

### Installation
```bash
pip install -r requirements.txt
```

### Running the System

#### 1. Test Multi-Agent System
```bash
python chatbot/multi_agent_system.py
```

#### 2. Run Interactive Dashboard
```bash
streamlit run ui/dashboard.py
```

#### 3. Run Comprehensive Demo
```bash
python demo_multi_agent.py
```

## 📁 Project Structure

```
Mega_project/
├── chatbot/
│   ├── multi_agent_system.py    # Three-agent implementation
│   ├── chatgpt_api.py          # Legacy single-agent system
│   └── http_bot.py             # HTTP-based bot
├── data/
│   ├── personas.json           # Customer persona definitions
│   └── tasks.json              # Task/order definitions
├── ui/
│   └── dashboard.py            # Streamlit web interface
├── utils/
│   ├── logger.py
│   └── report_generator.py
├── analytics.py
├── main.py                     # Simulation runner
├── demo_multi_agent.py         # Comprehensive demo
└── README.md
```

## 🔧 Configuration

### Personas Configuration (`data/personas.json`)
```json
[
  {
    "name": "Frustrated Customer",
    "biography": "Customer description...",
    "mood_tone": "frustrated",
    "task_execution_style": "one-by-one",
    "exploration_style": "does-not-explore",
    "communication_style": "direct and impatient"
  }
]
```

### Tasks Configuration (`data/tasks.json`)
```json
[
  {
    "task": "order_food",
    "items": ["pizza", "coke"]
  }
]
```

## 🎯 Key Features

- ✅ **Persona Control**: Realistic customer behavior simulation
- ✅ **Task State Tracking**: Maintains accurate order progress
- ✅ **Behavioral Consistency**: Attributes adapt based on persona and context
- ✅ **Explainable Decisions**: Tool-based agent coordination
- ✅ **Scalable Architecture**: Separated concerns for reliable simulation
- ✅ **Multi-Persona Support**: Three distinct customer types
- ✅ **Interactive Dashboard**: Web-based testing interface

## 📊 Evaluation Metrics (from Research Paper)

- **Persona Adherence Score (PAS)**: How well responses match assigned persona
- **Behavioral Variance Score (BVS)**: Realistic behavioral fluctuations
- **Task Restriction Adherence (TRA)**: Accuracy in achieving target state (F1-score)
- **Decision Explainability Index (DEI)**: Traceability of agent decisions
- **Composite Realism Score (CRRS)**: Overall simulation quality

This project now includes a Groq-backed HTTP restaurant bot (`chatbot/http_bot.py`) and a metrics evaluation module (`chatbot/evaluation.py`) for more research-aligned performance measurement.

## 🔬 Research Foundation

This implementation is based on the paper:
> **"Agentic Persona Control and Task State Tracking for Realistic User Simulation in Interactive Scenarios"**
>
> The system achieves **102.6% improvement** in simulation quality over single-LLM baselines, with significant gains in:
> - Persona adherence: +19.9%
> - Behavioral variance: +284.5%
> - Task completion accuracy: +29.1%

## 🛠️ Technical Details

### Dependencies
- `groq`: For Llama model API access
- `streamlit`: Web dashboard
- `json`: Data handling

### API Usage
- **Model**: `llama-3.1-8b-instant` (fast, lightweight LLM)
- **Provider**: Groq (alternative to OpenAI)
- **Architecture**: Multi-agent orchestration with structured protocols

## 🤝 Future Scope (Based on Research Paper)

1. **Adaptive Persona Evolution**: Dynamic behavioral adjustment during conversations
2. **Multi-Modal Integration**: Voice-based prosodic features and visual gesture recognition
3. **Cross-Domain Validation**: Healthcare consultations, e-commerce, customer support
4. **Efficiency Optimization**: Agent caching and selective tool invocation
5. **Advanced Behavioral Modeling**: Complex human behaviors like indecision and social dynamics

## 📈 Usage Examples

### Basic Persona Testing
```python
from chatbot.multi_agent_system import create_persona_agent

# Create agents
frustrated = create_persona_agent("Frustrated Customer")
happy = create_persona_agent("Happy Customer")
confused = create_persona_agent("Confused Customer")

# Test responses
message = "Welcome! What would you like to order?"
response = frustrated.reply(message, {"task": "order_food", "items": ["pizza", "coke"]})
```

### Full Conversation Simulation
```python
from main import run_simulation

# Run simulation with specific persona
history, bot_type, persona = run_simulation("ChatGPT", "Happy Customer")
```

## 📝 License

This project implements research concepts from the referenced paper for educational and research purposes.

## 🙏 Acknowledgments

- Research paper authors for the multi-agent framework concept
- Groq for providing efficient LLM access
- Streamlit for the interactive dashboard framework
