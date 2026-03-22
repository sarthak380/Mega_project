import streamlit as st
import time
from main import run_simulation
from analytics import show_analytics
from utils.report_generator import generate_report

st.set_page_config(
    page_title="AI Chatbot Tester",
    page_icon="🤖",
    layout="wide"
)

st.title("AI Chatbot Testing Platform")

menu=st.sidebar.selectbox(
    "Navigation",
    ["Chat Simulation","Analytics"]
)

if "history" not in st.session_state:
    st.session_state.history=[]

if menu=="Chat Simulation":

    bot=st.selectbox(
        "Select Chatbot",
        ["ChatGPT","HTTPBot"]
    )

    if st.button("Run Test"):

        history,bot_name=run_simulation(bot)

        st.session_state.history=history

    if st.session_state.history:

        st.subheader("Conversation")

        if st.button("Replay Conversation"):

            for u,b in st.session_state.history:

                with st.chat_message("user"):
                    st.write(u)

                time.sleep(1)

                with st.chat_message("assistant"):
                    st.write(b)

                time.sleep(1)

        report=generate_report(st.session_state.history)

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
    ]

    show_analytics(data)