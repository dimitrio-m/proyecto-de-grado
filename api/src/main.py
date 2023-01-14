import datetime
import pandas as pd
from flask import Flask
from lifetimes import BetaGeoFitter
from lifetimes.utils import summary_data_from_transaction_data
from lifetimes.utils import calculate_alive_path
from lifetimes.plotting import plot_history_alive

model = BetaGeoFitter()
model.load_model("../modelo/modelo.pkl")

app = Flask(__name__)


@app.route("/")
def index():
    return "Index Page"


@app.route("/conditional-probability-alive", methods=["GET"])
def conditionalProbabilityAlive():
    customer_field = "customer"
    date_field = "date"
    data = {
        "customer": [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3],
        "date": [
            datetime.datetime(2022, 1, 2),
            datetime.datetime(2022, 2, 2),
            datetime.datetime(2022, 3, 2),
            datetime.datetime(2022, 4, 2),
            datetime.datetime(2022, 5, 2),
            datetime.datetime(2022, 6, 2),
            datetime.datetime(2022, 7, 2),
            datetime.datetime(2022, 4, 2),
            datetime.datetime(2022, 5, 2),
            datetime.datetime(2022, 6, 2),
            datetime.datetime(2022, 7, 2),
            datetime.datetime(2022, 1, 2),
            datetime.datetime(2022, 1, 5),
            datetime.datetime(2022, 1, 7),
            datetime.datetime(2022, 1, 15),
            datetime.datetime(2022, 2, 2),
        ]
    }
    df = pd.DataFrame.from_dict(data)
    rfm_data = summary_data_from_transaction_data(
        df, customer_field, date_field)
    rfm_data["p_alive"] = model.conditional_probability_alive(
        rfm_data["frequency"], rfm_data["recency"], rfm_data["T"])
    result = rfm_data.to_dict("index")

    for i, row in rfm_data.iterrows():
        path = calculate_alive_path(
            model, df[df[customer_field] == i], date_field, 500).to_numpy().tolist()
        result[i]["path"] = [item for sublist in path for item in sublist]
    return {"result": result}
