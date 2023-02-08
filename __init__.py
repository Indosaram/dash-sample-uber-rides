import numpy as np
import pandas as pd

# Plotly mapbox public token
MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoiaW5kb3NhcmFtIiwiYSI6ImNsZHY4cWF1aDBkYnU0MXJxN3l0Nmc5ZWoifQ.YLRrfM57_eZvjEuuOLMPfg"

# Dictionary of important locations in New York
LOCATIONS = {
    "Madison Square Garden": {"lat": 40.7505, "lon": -73.9934},
    "Yankee Stadium": {"lat": 40.8296, "lon": -73.9262},
    "Empire State Building": {"lat": 40.7484, "lon": -73.9857},
    "New York Stock Exchange": {"lat": 40.7069, "lon": -74.0113},
    "JFK Airport": {"lat": 40.644987, "lon": -73.785607},
    "Grand Central Station": {"lat": 40.7527, "lon": -73.9772},
    "Times Square": {"lat": 40.7589, "lon": -73.9851},
    "Columbia University": {"lat": 40.8075, "lon": -73.9626},
    "United Nations HQ": {"lat": 40.7489, "lon": -73.9680},
}


def init_data():
    df1 = pd.read_csv("assets/uber-rides-data1.csv")
    df2 = pd.read_csv("assets/uber-rides-data2.csv")
    df3 = pd.read_csv("assets/uber-rides-data3.csv")
    df = pd.concat([df1, df2, df3], axis=0)
    df["Date/Time"] = pd.to_datetime(df["Date/Time"], format="%Y-%m-%d %H:%M")
    df.index = df["Date/Time"]
    df.drop("Date/Time", axis=1, inplace=True)

    return np.array(
        [
            [day[1] for day in month[1].groupby(month[1].index.day)]
            for month in df.groupby(df.index.month)
        ],
        dtype=object,
    )


TOTAL_DATA = init_data()
