import streamlit as st
import time
import sys
from pathlib import Path

# Ensure the project root is on sys.path so ui/dashboard.py can import sibling modules.
sys.path.append(str(Path(__file__).resolve().parents[1]))

from main import run_full_persona_evaluation
from analytics import show_analytics
from utils.report_generator import generate_report

st.set_page_config(
    page_title="AI Chatbot Tester - Multi-Agent System",
    page_icon="🤖",
    layout="wide"
)

st.title("AI Chatbot Testing Platform with Multi-Agent Persona Control")

menu = st.sidebar.selectbox(
    "Navigation",
    ["Chat Simulation", "Analytics", "Agent Information"]
)

if "evaluation_results" not in st.session_state:
    st.session_state.evaluation_results = None
if "evaluation_conclusion" not in st.session_state:
    st.session_state.evaluation_conclusion = None
if "agent_info" not in st.session_state:
    st.session_state.agent_info = None

if menu == "Chat Simulation":
    bot_options = [
        "ChatGPT (Multi-Agent)",
        "HTTP Restaurant Bot",
        "Educational Consultant Bot"
    ]
    bot_type_map = {
        "ChatGPT (Multi-Agent)": "ChatGPT",
        "HTTP Restaurant Bot": "HTTPRestaurantBot",
        "Educational Consultant Bot": "EducationalConsultantBot"
    }

    selected_bot = st.selectbox(
        "Select Chatbot",
        bot_options
    )
    bot_type = bot_type_map[selected_bot]

    st.markdown("### Persona Evaluation")
    st.info("The system will automatically evaluate performance across all predefined customer personas.")

    if st.button("Run Full Persona Evaluation"):
        with st.spinner("Running evaluation for all personas..."):
            evaluation_results, conclusion = run_full_persona_evaluation(bot_type)

        st.session_state.evaluation_results = evaluation_results
        st.session_state.evaluation_conclusion = conclusion
        st.session_state.agent_info = {
            "bot_type": bot_type
        }
        st.success("Evaluation completed!")

    if st.session_state.evaluation_results:
        st.subheader("Persona Evaluation Results")

        info = st.session_state.agent_info
        st.write(f"**Bot Type:** {info['bot_type']} | **Personas Evaluated:** {len(st.session_state.evaluation_results)}")

        table_data = []
        for result in st.session_state.evaluation_results:
            metrics = result["metrics"]
            table_data.append({
                "Persona": result["persona"],
                "PAS": f"{metrics['PAS']}%",
                "BVS": f"{metrics['BVS']}%",
                "TRA": f"{metrics['TRA']}%",
                "DEI": f"{metrics['DEI']}%",
                "CRRS": f"{metrics['CRRS']}%"
            })

        st.table(table_data)

        average_metrics = {
            "PAS": int(sum(result["metrics"]["PAS"] for result in st.session_state.evaluation_results) / len(st.session_state.evaluation_results)),
            "BVS": int(sum(result["metrics"]["BVS"] for result in st.session_state.evaluation_results) / len(st.session_state.evaluation_results)),
            "TRA": int(sum(result["metrics"]["TRA"] for result in st.session_state.evaluation_results) / len(st.session_state.evaluation_results)),
            "DEI": int(sum(result["metrics"]["DEI"] for result in st.session_state.evaluation_results) / len(st.session_state.evaluation_results)),
            "CRRS": int(sum(result["metrics"]["CRRS"] for result in st.session_state.evaluation_results) / len(st.session_state.evaluation_results))
        }

        metric_cols = st.columns(5)
        metric_cols[0].metric("Avg PAS", f"{average_metrics['PAS']}%")
        metric_cols[1].metric("Avg BVS", f"{average_metrics['BVS']}%")
        metric_cols[2].metric("Avg TRA", f"{average_metrics['TRA']}%")
        metric_cols[3].metric("Avg DEI", f"{average_metrics['DEI']}%")
        metric_cols[4].metric("Avg CRRS", f"{average_metrics['CRRS']}%")

        st.subheader("Final Conclusion")
        st.write(st.session_state.evaluation_conclusion)

        if st.button("Generate Report"):
            with st.spinner("Generating report..."):
                report = generate_report(
                    [],
                    "All Personas",
                    st.session_state.agent_info['bot_type'],
                    evaluation_results=st.session_state.evaluation_results,
                    conclusion=st.session_state.evaluation_conclusion
                )

            with open(report, "rb") as f:
                st.download_button(
                    "Download PDF Report",
                    f,
                    file_name=report
                )

<<<<<<< HEAD
if menu == "Analytics":
    data = [
        {"bot": "ChatGPT (Multi-Agent)", "success_rate": 95, "avg_turns": 4},
        {"bot": "HTTP Restaurant Bot", "success_rate": 75, "avg_turns": 6},
        {"bot": "Educational Consultant Bot", "success_rate": 85, "avg_turns": 5}
=======
        with open(report,"rb") as f:

            st.download_button(
                "Download PDF Report",
                f,
                file_name="chatbot_report.pdf"
            )


if menu=="Analytics":

    data=[
        {"bot":"ChatGPT","success_rate":95,"avg_turns":4},
        {"bot":"HTTPBot","success_rate":75,"avg_turns":6}
>>>>>>> ff1bca476cd72de217a20808e59659cabfd0ed0f
    ]

    show_analytics(data)

if menu == "Agent Information":
    st.header("Multi-Agent System Architecture")

    st.markdown("""
    ## Three-Agent Framework (Based on Research Paper)

    ### 🤖 User Agent (Main Orchestrator)
    - **Role**: Coordinates the overall interaction and generates customer responses
    - **Function**: Uses state tracking and behavioral attributes to create realistic responses
    - **Protocol**: Invokes sub-agents in sequence (State Tracking → Message Attributes)

    ### 📊 State Tracking Agent
    - **Role**: Maintains structured task state during conversations
    - **Tracks**: `Tcurrent` (confirmed items) and `Ttarget` (target items)
    - **Function**: Updates order state based on conversation progress

    ### 🎭 Message Attributes Generation Agent
    - **Role**: Controls conversational attributes based on persona and task progress
    - **Attributes**: mood_tone, task_execution_style, exploration_style, task_completion_status
    - **Function**: Ensures persona consistency while allowing behavioral variation

    ## Available Personas

    ### 😡 Frustrated Customer
    - **Mood**: Frustrated, impatient
    - **Style**: Direct, one-by-one task execution
    - **Exploration**: Prefers quick order completion and minimal extra detail

    ### 😊 Happy Customer
    - **Mood**: Enthusiastic, friendly
    - **Style**: All-at-once task execution
    - **Exploration**: Enjoys suggestions and pleasant interaction

    ### 😕 Confused Customer
    - **Mood**: Confused, questioning
    - **Style**: One-by-one task execution
    - **Exploration**: Seeks clarification and reassurance

    ## Key Features
    - ✅ **Persona Control**: Realistic customer behavior simulation
    - ✅ **Task State Tracking**: Maintains accurate order progress
    - ✅ **Behavioral Consistency**: Attributes adapt based on persona and context
    - ✅ **Explainable Decisions**: Tool-based agent coordination
    - ✅ **Scalable Architecture**: Separated concerns for reliable simulation
    """)

    # Show current agent states if simulation has run
    if st.session_state.agent_info and st.session_state.history:
        st.subheader("Current Simulation State")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Bot Type", st.session_state.agent_info['bot_type'])

        with col2:
            st.metric("Persona", st.session_state.agent_info['persona'])

        with col3:
            st.metric("Conversation Turns", st.session_state.agent_info['conversation_length'])