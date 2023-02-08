from datetime import datetime as dt

import numpy as np
from dash.dependencies import Input, Output
from plotly import graph_objects as go
from plotly.graph_objects import Layout, Scattermapbox

from app import LOCATIONS, MAPBOX_ACCESS_TOKEN, TOTAL_DATA, app
from utils import get_lat_lon_color, get_selection


# Selected Data in the Histogram updates the Values in the Hours selection dropdown menu
@app.callback(
    Output("bar-selector", "value"),
    [Input("histogram", "selectedData"), Input("histogram", "clickData")],
)
def update_bar_selector(value, click_data):
    holder = []
    if click_data:
        holder.append(str(int(click_data["points"][0]["x"])))
    if value:
        for x in value["points"]:
            holder.append(str(int(x["x"])))
    return list(set(holder))


# Clear Selected Data if Click Data is used
@app.callback(Output("histogram", "selectedData"), [Input("histogram", "clickData")])
def update_selected_data(click_data):
    if click_data:
        return {"points": []}


# Update the total number of rides Tag
@app.callback(Output("total-rides", "children"), [Input("date-picker", "date")])
def update_total_rides(date_picked):
    date_picked = dt.strptime(date_picked, "%Y-%m-%d")
    return "Total Number of rides: {:,d}".format(
        len(TOTAL_DATA[date_picked.month - 4][date_picked.day - 1])
    )


# Update the total number of rides in selected times
@app.callback(
    [
        Output("total-rides-selection", "children"),
        Output("date-value", "children"),
    ],
    [Input("date-picker", "date"), Input("bar-selector", "value")],
)
def update_total_rides_selection(date_picked, selection):
    first_output = ""

    if selection:
        date_picked = dt.strptime(date_picked, "%Y-%m-%d")
        total_in_selection = 0
        for x in selection:
            total_in_selection += len(
                TOTAL_DATA[date_picked.month - 4][date_picked.day - 1][
                    TOTAL_DATA[date_picked.month - 4][date_picked.day - 1].index.hour
                    == int(x)
                ]
            )
        first_output = "Total rides in selection: {:,d}".format(total_in_selection)

    if (
        date_picked is None
        or selection is None
        or len(selection) == 24
        or len(selection) == 0
    ):
        return first_output, (date_picked, " - showing hour(s): All")

    holder = sorted([int(x) for x in selection])

    if holder == list(range(min(holder), max(holder) + 1)):
        return (
            first_output,
            (
                date_picked,
                " - showing hour(s): ",
                holder[0],
                "-",
                holder[len(holder) - 1],
            ),
        )

    holder_to_string = ", ".join(str(x) for x in holder)
    return first_output, (date_picked, " - showing hour(s): ", holder_to_string)


# Update Histogram Figure based on Month, Day and Times Chosen
@app.callback(
    Output("histogram", "figure"),
    Input("date-picker", "date"),
    Input("bar-selector", "value"),
)
def update_histogram(date_picked, selection):
    date_picked = dt.strptime(date_picked, "%Y-%m-%d")
    month_picked = date_picked.month - 4
    day_picked = date_picked.day - 1

    [x_val, y_val, color_val] = get_selection(month_picked, day_picked, selection)

    layout = go.Layout(
        bargap=0.01,
        bargroupgap=0,
        barmode="group",
        margin=go.layout.Margin(l=10, r=0, t=0, b=50),
        showlegend=False,
        plot_bgcolor="#323130",
        paper_bgcolor="#323130",
        dragmode="select",
        font=dict(color="white"),
        xaxis=dict(
            range=[-0.5, 23.5],
            showgrid=False,
            nticks=25,
            fixedrange=True,
            ticksuffix=":00",
        ),
        yaxis=dict(
            range=[0, max(y_val) + max(y_val) / 4],
            showticklabels=False,
            showgrid=False,
            fixedrange=True,
            rangemode="nonnegative",
            zeroline=False,
        ),
        annotations=[
            dict(
                x=xi,
                y=yi,
                text=str(yi),
                xanchor="center",
                yanchor="bottom",
                showarrow=False,
                font=dict(color="white"),
            )
            for xi, yi in zip(x_val, y_val)
        ],
    )

    return go.Figure(
        data=[
            go.Bar(x=x_val, y=y_val, marker=dict(color=color_val), hoverinfo="x"),
            go.Scatter(
                opacity=0,
                x=x_val,
                y=y_val / 2,
                hoverinfo="none",
                mode="markers",
                marker=dict(color="rgb(66, 134, 244, 0)", symbol="square", size=40),
                visible=True,
            ),
        ],
        layout=layout,
    )


# Update Map Graph based on date-picker, selected data on histogram and location dropdown
@app.callback(
    Output("map-graph", "figure"),
    [
        Input("date-picker", "date"),
        Input("bar-selector", "value"),
        Input("location-dropdown", "value"),
    ],
)
def update_graph(date_picked, selected_data, selected_location):
    zoom = 12.0
    lat_initial = 40.7272
    lon_initial = -73.991251
    bearing = 0

    if selected_location:
        zoom = 15.0
        lat_initial = LOCATIONS[selected_location]["lat"]
        lon_initial = LOCATIONS[selected_location]["lon"]

    date_picked = dt.strptime(date_picked, "%Y-%m-%d")
    month_picked = date_picked.month - 4
    day_picked = date_picked.day - 1
    coords = get_lat_lon_color(selected_data, month_picked, day_picked)

    return go.Figure(
        data=[
            # Data for all rides based on date and time
            Scattermapbox(
                lat=coords["Lat"],
                lon=coords["Lon"],
                mode="markers",
                hoverinfo="lat+lon+text",
                text=coords.index.hour,
                marker=dict(
                    showscale=True,
                    color=np.append(np.insert(coords.index.hour, 0, 0), 23),
                    opacity=0.5,
                    size=5,
                    colorscale=[
                        [0, "#F4EC15"],
                        [0.04167, "#DAF017"],
                        [0.0833, "#BBEC19"],
                        [0.125, "#9DE81B"],
                        [0.1667, "#80E41D"],
                        [0.2083, "#66E01F"],
                        [0.25, "#4CDC20"],
                        [0.292, "#34D822"],
                        [0.333, "#24D249"],
                        [0.375, "#25D042"],
                        [0.4167, "#26CC58"],
                        [0.4583, "#28C86D"],
                        [0.50, "#29C481"],
                        [0.54167, "#2AC093"],
                        [0.5833, "#2BBCA4"],
                        [1.0, "#613099"],
                    ],
                    colorbar=dict(
                        title="Time of<br>Day",
                        x=0.93,
                        xpad=0,
                        nticks=24,
                        tickfont=dict(color="#d8d8d8"),
                        titlefont=dict(color="#d8d8d8"),
                        thicknessmode="pixels",
                    ),
                ),
            ),
            # Plot of important locations on the map
            Scattermapbox(
                lat=[LOCATIONS[i]["lat"] for i in LOCATIONS],
                lon=[LOCATIONS[i]["lon"] for i in LOCATIONS],
                mode="markers",
                hoverinfo="text",
                text=LOCATIONS,
                marker=dict(size=8, color="#ffa0a0"),
            ),
        ],
        layout=Layout(
            autosize=True,
            margin=go.layout.Margin(l=0, r=35, t=0, b=0),
            showlegend=False,
            mapbox=dict(
                accesstoken=MAPBOX_ACCESS_TOKEN,
                center=dict(lat=lat_initial, lon=lon_initial),  # 40.7272  # -73.991251
                style="dark",
                bearing=bearing,
                zoom=zoom,
            ),
            updatemenus=[
                dict(
                    buttons=(
                        [
                            dict(
                                args=[
                                    {
                                        "mapbox.zoom": 12,
                                        "mapbox.center.lon": "-73.991251",
                                        "mapbox.center.lat": "40.7272",
                                        "mapbox.bearing": 0,
                                        "mapbox.style": "dark",
                                    }
                                ],
                                label="Reset Zoom",
                                method="relayout",
                            )
                        ]
                    ),
                    direction="left",
                    pad={"r": 0, "t": 0, "b": 0, "l": 0},
                    showactive=False,
                    type="buttons",
                    x=0.45,
                    y=0.02,
                    xanchor="left",
                    yanchor="bottom",
                    bgcolor="#323130",
                    borderwidth=1,
                    bordercolor="#6d6d6d",
                    font=dict(color="#FFFFFF"),
                )
            ],
        ),
    )
