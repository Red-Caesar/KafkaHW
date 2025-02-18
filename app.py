import streamlit as st

from backend.producers import (
    StockDataProducer,
    StockMetricsProducer,
    StockPredictionProducer,
)
from backend.consumers import StockDataConsumer
from app_pages.visualization_page import visualization_page
from app_pages.prediction_page import ml_prediction_page
from app_pages.realtime_page import realtime_page


class StockProcessor:
    def __init__(self):
        self.data_producer = StockDataProducer()
        self.metrics_producer = StockMetricsProducer()
        self.prediction_producer = StockPredictionProducer()

    def get_or_create_consumer(self, topic: str, kafka_host: str) -> StockDataConsumer:
        consumer_key = f"{topic}_consumer"
        if consumer_key not in st.session_state:
            st.session_state[consumer_key] = StockDataConsumer(topic, kafka_host)
        return st.session_state[consumer_key]

    @property
    def stock_consumer(self):
        return self.get_or_create_consumer("raw_stock_data", "kafka-raw")

    @property
    def metrics_consumer(self):
        return self.get_or_create_consumer("stock_metrics", "kafka-metrics")

    @property
    def prediction_consumer(self):
        return self.get_or_create_consumer("prediction_data", "kafka-predictions")

    @property
    def realtime_consumer(self):
        return self.get_or_create_consumer("realtime_stock_data", "kafka-raw")


def main():
    st.title("Stock Data Analysis")

    if "processor" not in st.session_state:
        st.session_state["processor"] = StockProcessor()

    page = st.sidebar.selectbox(
        "Choose a page", ["Data Visualization", "ML Prediction", "Real-Time Data"]
    )

    if page == "Data Visualization":
        visualization_page()
    elif page == "ML Prediction":
        ml_prediction_page()
    else:
        realtime_page()


if __name__ == "__main__":
    main()
