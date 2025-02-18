import streamlit as st

# from stock_processor import StockDataProducer, StockDataConsumer
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

        self.stock_consumer = StockDataConsumer("raw_stock_data")
        self.metrics_consumer = StockDataConsumer("stock_metrics")
        self.prediction_consumer = StockDataConsumer("prediction_data")
        self.realtime_consumer = StockDataConsumer("realtime_stock_data")


def main():
    st.title("Stock Data Analysis")

    processor = StockProcessor()

    # if 'stock_consumer' not in st.session_state:
    #     st.session_state['stock_consumer'] = StockDataConsumer('stock_data')
    # if 'prediction_consumer' not in st.session_state:
    #     st.session_state['prediction_consumer'] = StockDataConsumer('prediction_data')
    # if 'realtime_consumer' not in st.session_state:
    #     st.session_state['realtime_consumer'] = StockDataConsumer('realtime_stock_data')

    page = st.sidebar.selectbox(
        "Choose a page", ["Data Visualization", "ML Prediction", "Real-Time Data"]
    )

    if page == "Data Visualization":
        visualization_page(processor)
    elif page == "ML Prediction":
        ml_prediction_page(processor)
    else:
        realtime_page(processor)


if __name__ == "__main__":
    main()
