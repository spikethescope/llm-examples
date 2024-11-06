import streamlit as st
from streamlit_echarts import st_echarts

# Display title
st.title("Interactive Line Chart using Apache ECharts")

# User inputs for x-axis and y-axis values
st.subheader("Enter up to 10 data points for X and Y axes")

# Input fields for X-axis values
x_values = st.text_input("X-axis values (comma-separated, e.g., Jan, Feb, Mar):")
x_values = [x.strip() for x in x_values.split(",")][:10]  # Limit to 10 values

# Input fields for Y-axis values
y_values = st.text_input("Y-axis values (comma-separated, e.g., 820, 932, 901):")
try:
    y_values = [float(y.strip()) for y in y_values.split(",")][:10]  # Limit to 10 values and convert to floats
except ValueError:
    st.error("Please ensure Y-axis values are numeric.")

# Ensure both lists are of the same length and not empty before displaying the chart
if len(x_values) == len(y_values) and len(x_values) > 0:
    # Configure ECharts options for a line chart
    options = {
        "title": {
            "text": "User-Defined Line Chart"
        },
        "tooltip": {
            "trigger": "axis"
        },
        "xAxis": {
            "type": "category",
            "data": x_values
        },
        "yAxis": {
            "type": "value"
        },
        "series": [
            {
                "data": y_values,
                "type": "line",
                "smooth": True
            }
        ]
    }

    # Render the line chart using streamlit-echarts
    st_echarts(options=options, height="400px")
else:
    st.info("Please enter up to 10 values for both X and Y axes, ensuring both have the same number of entries.")
