import pandas as pd
import plotly.express as px
import streamlit as st

def show_analytics(data):

    df=pd.DataFrame(data)

    st.subheader("Chatbot Performance")

    fig=px.bar(
        df,
        x="bot",
        y="success_rate",
        color="bot"
    )

    st.plotly_chart(fig)

    fig2=px.line(
        df,
        x="bot",
        y="avg_turns"
    )

    st.plotly_chart(fig2)