import numpy as np

from app import TOTAL_DATA


# Get the Coordinates of the chosen months, dates and times
def get_lat_lon_color(selected_data, month, day):
    coords = TOTAL_DATA[month][day]

    # No times selected, output all times for chosen month and date
    if not selected_data:
        return coords

    return coords[coords.index.hour in selected_data]


# Get the amount of rides per hour based on the time selected
# This also higlights the color of the histogram bars based on
# if the hours are selected
def get_selection(month, day, selection):
    color_val = [
        "#F4EC15",
        "#DAF017",
        "#BBEC19",
        "#9DE81B",
        "#80E41D",
        "#66E01F",
        "#4CDC20",
        "#34D822",
        "#24D249",
        "#25D042",
        "#26CC58",
        "#28C86D",
        "#29C481",
        "#2AC093",
        "#2BBCA4",
        "#2BB5B8",
        "#2C99B4",
        "#2D7EB0",
        "#2D65AC",
        "#2E4EA4",
        "#2E38A4",
        "#3B2FA0",
        "#4E2F9C",
        "#603099",
    ]

    # Put selected times into a list of numbers x_selected
    x_selected = [int(x) for x in selection]
    x_val = list(range(24))
    y_val = []
    for i in x_val:
        # If bar is selected then color it white
        if i in x_selected and len(x_selected) < 24:
            color_val[i] = "#FFFFFF"

        # Get the number of rides at a particular time
        today = TOTAL_DATA[month][day]
        y_val.append(len(today[today.index.hour == i]))
    return [np.array(x_val), np.array(y_val), np.array(color_val)]
