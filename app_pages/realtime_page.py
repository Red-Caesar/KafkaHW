import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from time import sleep
from datetime import datetime, timedelta


def realtime_page(processor):
    st.header("Real-Time Stock Data Visualization")

    col1, col2, col3 = st.columns(3)

    with col1:
        symbol = st.text_input("Enter stock symbol (e.g., AAPL):", "AAPL")

    with col2:
        start_date = st.date_input(
            "Start date", value=datetime.now() - timedelta(days=30)
        ).strftime("%Y-%m-%d")

    with col3:
        end_date = st.date_input("End date (optional)", value=None)
        end_date = end_date.strftime("%Y-%m-%d") if end_date else None

    update_interval = st.slider(
        "Update interval (seconds)", min_value=1, max_value=60, value=5
    )

    if "historical_data" not in st.session_state:
        st.session_state["historical_data"] = []

    if st.button("Start Streaming"):
        st.session_state["historical_data"] = []

        processor.data_producer.start_realtime_streaming(
            symbol, start_date=start_date, end_date=end_date, interval=update_interval
        )

        chart_placeholder = st.empty()

        while True:
            new_data = processor.realtime_consumer.get_latest_data()

            if new_data:
                st.session_state["historical_data"].append(
                    {
                        "Date": pd.to_datetime(new_data["data"]["Date"]),
                        "Close": new_data["data"]["Close"],
                    }
                )

                df = pd.DataFrame(st.session_state["historical_data"])

                df["Returns"] = df["Close"].pct_change() * 100

                fig1 = go.Figure()
                fig2 = go.Figure()

                fig1.add_trace(
                    go.Scatter(
                        x=df["Date"],
                        y=df["Close"],
                        name="Price",
                        line=dict(color="blue"),
                    )
                )

                fig1.update_layout(
                    title=f"{symbol} Stock Price",
                    xaxis_title="Date",
                    yaxis_title="Price",
                    height=300,
                    showlegend=True,
                    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                )

                fig2.add_trace(
                    go.Scatter(
                        x=df["Date"],
                        y=df["Returns"],
                        name="Returns (%)",
                        line=dict(color="red"),
                    )
                )

                fig2.update_layout(
                    title="Returns (%)",
                    xaxis_title="Date",
                    yaxis_title="Returns (%)",
                    height=300,
                    showlegend=True,
                    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                )

                chart_placeholder.plotly_chart(fig1, use_container_width=True)
                chart_placeholder.plotly_chart(fig2, use_container_width=True)

            sleep(1)
