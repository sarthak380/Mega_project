"""
Multi-Agent Persona Control System Demo

This script demonstrates the three-agent framework for realistic user simulation
based on the research paper: "Agentic Persona Control and Task State Tracking
for Realistic User Simulation in Interactive Scenarios"

The system includes:
1. User Agent - Main orchestrator that generates customer responses
2. State Tracking Agent - Maintains task state (Tcurrent, Ttarget)
3. Message Attributes Generation Agent - Controls behavioral attributes

Three personas are available:
- Frustrated Customer: Direct, impatient, prefers straightforward order completion
- Happy Customer: Cheerful, positive, enjoys suggestions and friendly interaction
- Confused Customer: Questioning, seeks clarification, needs step-by-step guidance
"""

from chatbot.multi_agent_system import create_persona_agent
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"

def demo_persona_responses():
    """Demonstrate how each persona responds to the same restaurant greeting"""

    # Create agents for each persona
    frustrated_agent = create_persona_agent("Frustrated Customer")
    happy_agent = create_persona_agent("Happy Customer")
    confused_agent = create_persona_agent("Confused Customer")

    # Sample restaurant greeting
    restaurant_message = "Welcome to our restaurant! What would you like to order today?"

    # Sample task (ordering pizza and coke)
    with open(DATA_DIR / "tasks.json", "r", encoding="utf-8") as f:
        tasks = json.load(f)
    task = tasks[0]  # order_food task

    print("🍽️ Multi-Agent Persona Control System Demo")
    print("=" * 60)
    print(f"Restaurant: {restaurant_message}")
    print(f"Target Order: {task['items']}")
    print()

    # Test each persona
    personas = [
        ("😡 Frustrated Customer", frustrated_agent),
        ("😊 Happy Customer", happy_agent),
        ("😕 Confused Customer", confused_agent)
    ]

    for emoji_name, agent in personas:
        print(f"{emoji_name}:")
        response = agent.reply(restaurant_message, task)

        # Show agent internal state
        state = agent.get_current_state()
        print(f"  Response: {response}")
        print(f"  Current State: Tcurrent={state['Tcurrent']}, Ttarget={state['Ttarget']}")
        print()

def demo_conversation_flow():
    """Demonstrate a full conversation flow with state tracking"""

    print("\n🔄 Full Conversation Flow Demo")
    print("=" * 60)

    # Use confused customer for this demo (shows most interaction)
    agent = create_persona_agent("Confused Customer")

    with open(DATA_DIR / "tasks.json", "r", encoding="utf-8") as f:
        tasks = json.load(f)
    task = tasks[0]

    # Simulate conversation turns
    conversation_flow = [
        "Welcome to our restaurant! What would you like to order today?",
        "We have pizza, burgers, pasta, and salads. What sounds good to you?",
        "Our pizza comes with cheese, pepperoni, or vegetarian toppings. Which would you like?",
        "Great choice! Would you like a drink with that?",
        "We have Coke, Pepsi, water, and various juices. What would you prefer?"
    ]

    for i, restaurant_msg in enumerate(conversation_flow, 1):
        print(f"\nTurn {i}:")
        print(f"🍽️ Restaurant: {restaurant_msg}")

        customer_response = agent.reply(restaurant_msg, task)
        print(f"👤 Confused Customer: {customer_response}")

        # Show state tracking
        state = agent.get_current_state()
        print(f"📊 State: Confirmed={state['Tcurrent']}, Target={state['Ttarget']}")

        # Check if task is complete
        if set(state['Tcurrent']) == set(state['Ttarget']):
            print("✅ Task Complete!")
            break

def show_agent_architecture():
    """Explain the three-agent architecture"""

    print("\n🏗️ Agent Architecture Overview")
    print("=" * 60)

    architecture = {
        "🤖 User Agent (Orchestrator)": {
            "role": "Main coordinator that generates customer responses",
            "function": "rt = fuser(mt,st,at) - combines message, state, and attributes",
            "protocol": "Invokes sub-agents: State Tracking → Message Attributes → Response"
        },
        "📊 State Tracking Agent": {
            "role": "Maintains structured task state",
            "tracks": "Tcurrent (confirmed items), Ttarget (target items)",
            "function": "st = fstateTracking(input_message) = {Tcurrent,Ttarget}"
        },
        "🎭 Message Attributes Generation Agent": {
            "role": "Controls conversational attributes based on persona",
            "attributes": "mood_tone, task_execution_style, exploration_style, task_completion_status",
            "function": "at = fmsgAttrGen(pbio,st)"
        }
    }

    for agent_name, details in architecture.items():
        print(f"\n{agent_name}:")
        for key, value in details.items():
            print(f"  • {key}: {value}")

if __name__ == "__main__":
    # Run all demos
    demo_persona_responses()
    demo_conversation_flow()
    show_agent_architecture()

    print("\n🎯 Key Benefits:")
    print("• Realistic persona-driven behavior simulation")
    print("• Explainable agent decisions through structured protocols")
    print("• Task state tracking for coherent conversations")
    print("• Behavioral consistency with controlled variation")
    print("• Scalable architecture for different domains")