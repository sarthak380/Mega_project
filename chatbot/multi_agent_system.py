from groq import Groq
import json
from pathlib import Path

# Project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"

# Load configuration
with open(DATA_DIR / "personas.json", 'r', encoding='utf-8') as f:
    PERSONAS = json.load(f)

with open(DATA_DIR / "tasks.json", 'r', encoding='utf-8') as f:
    TASKS = json.load(f)

client = Groq(api_key="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")

class StateTrackingAgent:
    """
    State Tracking Agent maintains structured task state by tracking current confirmed items
    against target goals, enabling precise progress tracking.
    """

    def __init__(self):
        self.current_state = {"Tcurrent": [], "Ttarget": []}

    def update_state(self, input_message, target_task=None):
        """
        Updates the task state based on input message and target task.
        Returns updated state: {Tcurrent: list of confirmed items, Ttarget: target items}
        """
        if target_task:
            self.current_state["Ttarget"] = target_task.get("items", [])

        # Use LLM to extract confirmed items from the input message
        prompt = f"""
        You are a State Tracking Agent. Your task is to maintain accurate task state.

        Current State:
        - Confirmed items (Tcurrent): {self.current_state["Tcurrent"]}
        - Target items (Ttarget): {self.current_state["Ttarget"]}

        Input message: "{input_message}"

        Based on the input message, update the confirmed items (Tcurrent).
        - Add items that are clearly confirmed/ordered
        - Remove items that are cancelled
        - Keep items that are still valid

        Return only the updated Tcurrent as a JSON array of strings.
        Example: ["pizza", "coke"]
        """

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1  # Low temperature for consistency
            )

            result = response.choices[0].message.content.strip()
            # Try to parse as JSON
            try:
                updated_current = json.loads(result)
                if isinstance(updated_current, list):
                    self.current_state["Tcurrent"] = updated_current
            except json.JSONDecodeError:
                # Fallback: extract items manually
                self.current_state["Tcurrent"] = self._extract_items_fallback(result)

        except Exception as e:
            print(f"State tracking error: {e}")

        return self.current_state

    def _extract_items_fallback(self, text):
        """Fallback method to extract items from text"""
        items = []
        common_food_items = ["pizza", "burger", "coke", "pepsi", "fries", "salad", "pasta", "sandwich"]
        text_lower = text.lower()
        for item in common_food_items:
            if item in text_lower:
                items.append(item)
        return items

    def is_task_complete(self):
        """Check if current state matches target state"""
        current_set = set(self.current_state["Tcurrent"])
        target_set = set(self.current_state["Ttarget"])
        return current_set == target_set


class MessageAttributesGenerationAgent:
    """
    Message Attributes Generation Agent determines behavioral characteristics for each user response,
    while preserving persona consistency based on task progress and assigned persona.
    """

    def __init__(self, persona):
        self.persona = persona

    def generate_attributes(self, current_state):
        """
        Generate behavioral attributes based on persona and current task state.

        Returns:
        {
            "mood_tone": "casual|frustrated|confused|enthusiastic",
            "task_execution_style": "one-by-one|all-at-once",
            "exploration_style": "explores|does-not-explore",
            "task_completion_status": "complete|incomplete"
        }
        """

        # Check task completion
        state_tracker = StateTrackingAgent()
        state_tracker.current_state = current_state
        is_complete = state_tracker.is_task_complete()

        # Base attributes from persona
        attributes = {
            "mood_tone": self.persona.get("mood_tone", "casual"),
            "task_execution_style": self.persona.get("task_execution_style", "one-by-one"),
            "exploration_style": self.persona.get("exploration_style", "does-not-explore"),
            "task_completion_status": "complete" if is_complete else "incomplete"
        }

        # Dynamic adjustment based on state (could add more complex logic here)
        if not is_complete and len(current_state.get("Tcurrent", [])) > 0:
            # If task is in progress, maintain persona's base mood
            pass
        elif is_complete:
            # If task is complete, keep persona mood consistent or allow the persona's base tone to guide the response.
            pass

        return attributes


class UserAgent:
    """
    User Agent orchestrates the overall interaction, generating simulated user responses
    in the conversation by coordinating with the State Tracking and Message Attributes agents.
    """

    def __init__(self, persona_name):
        # Find persona by name
        self.persona = next((p for p in PERSONAS if p["name"] == persona_name), PERSONAS[0])
        self.state_agent = StateTrackingAgent()
        self.attributes_agent = MessageAttributesGenerationAgent(self.persona)
        self.conversation_history = []

    def reply(self, message, target_task=None):
        """
        Generate a user response by coordinating with sub-agents.
        Follows the protocol: State Tracking → Message Attributes Generation → Response Generation
        """

        # Step 1: Update state using State Tracking Agent
        current_state = self.state_agent.update_state(message, target_task)

        # Step 2: Generate behavioral attributes using Message Attributes Agent
        attributes = self.attributes_agent.generate_attributes(current_state)

        # Step 3: Generate response using state and attributes
        response = self._generate_response(message, current_state, attributes)

        # Update conversation history
        self.conversation_history.append({"role": "user", "message": message, "response": response})

        return response

    def _generate_response(self, input_message, current_state, attributes):
        """Generate the actual response using LLM with state and attributes context"""

        system_prompt = f"""
        You are role-playing as a restaurant customer with the following persona:

        Name: {self.persona['name']}
        Biography: {self.persona['biography']}
        Communication Style: {self.persona['communication_style']}

        Current behavioral attributes:
        - Mood: {attributes['mood_tone']}
        - Task execution style: {attributes['task_execution_style']}
        - Exploration style: {attributes['exploration_style']}
        - Task completion status: {attributes['task_completion_status']}

        Current order state:
        - Confirmed items: {current_state['Tcurrent']}
        - Target items: {current_state['Ttarget']}

        Respond as this customer would in a restaurant ordering conversation.
        Stay in character and follow the behavioral attributes.
        Keep responses natural and conversational.
        """

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Restaurant: {input_message}"}
        ]

        # Add conversation history for context (last few exchanges)
        if len(self.conversation_history) > 0:
            recent_history = self.conversation_history[-2:]  # Last 2 exchanges
            for exchange in recent_history:
                messages.append({"role": "assistant", "content": f"Customer: {exchange['response']}"})
                messages.append({"role": "user", "content": f"Restaurant: {exchange['message']}"})

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                temperature=0.7  # Moderate temperature for natural variation
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"I apologize, but I'm having trouble responding right now. ({str(e)})"

    def get_current_state(self):
        """Get current task state"""
        return self.state_agent.current_state

    def get_persona_info(self):
        """Get current persona information"""
        return self.persona


# Convenience function to create agents for different personas
def create_persona_agent(persona_name):
    """Create a UserAgent for the specified persona"""
    return UserAgent(persona_name)


# Example usage
if __name__ == "__main__":
    # Test the three active personas
    frustrated_agent = create_persona_agent("Frustrated Customer")
    happy_agent = create_persona_agent("Happy Customer")
    confused_agent = create_persona_agent("Confused Customer")

    # Test with a sample restaurant message
    test_message = "Welcome to our restaurant! What would you like to order today?"

    print("=== Testing Multi-Agent System ===")

    personas = [
        ("😡 Frustrated Customer", frustrated_agent),
        ("😊 Happy Customer", happy_agent),
        ("😕 Confused Customer", confused_agent)
    ]

    for label, agent in personas:
        print(f"\n{label}:")
        response = agent.reply(test_message, TASKS[0])  # order_food task
        print(f"Response: {response}")
