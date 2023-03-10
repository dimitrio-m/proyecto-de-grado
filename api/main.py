import datetime
import pandas as pd
from flask import Flask, request
from flask_cors import CORS
from lifetimes import BetaGeoFitter
from lifetimes.utils import summary_data_from_transaction_data
from lifetimes.utils import calculate_alive_path

model = BetaGeoFitter()
model.load_model("./modelo.pkl")

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "Index Page"


@app.route("/conditional-probability-alive", methods=["POST"])
def conditionalProbabilityAlive():
    if request.method == "POST":
        # Lectura de datos
        customer_field = "customer"
        date_field = "date"
        data = request.json["transactions"]
        # Validaciones
        if data.get("customer") is None or data.get("date") is None:
            return "Bad Request", 400
        if type(data.get("customer")) not in (tuple, list):
            return "Bad Request", 400
        if type(data.get("date")) not in (tuple, list):
            return "Bad Request", 400
        if len(data.get("date")) != len(data.get("customer")):
            return "Bad Request", 400
        # Crear DataFrame
        df = pd.DataFrame.from_dict(data)
        # Formato RFM
        rfm_data = summary_data_from_transaction_data(
            df, customer_field, date_field)
        # Calcular probabilidad siguiente periodo
        rfm_data["p_alive"] = model.conditional_probability_alive(
            rfm_data["frequency"], rfm_data["recency"], rfm_data["T"]
        )
        # Resultado
        result = rfm_data.to_dict("index")
        # Predecir probabilidad futura por usuario
        for i, _row in rfm_data.iterrows():
            path = (
                calculate_alive_path(
                    model, df[df[customer_field] == i], date_field, 500
                )
                .to_numpy()
                .tolist()
            )
            result[i]["path"] = [item for sublist in path for item in sublist]
        return {"result": result}
    else:
        raise RuntimeError("Unsupported method {}".format(request.method))
