import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Man City Passing Stats", layout="wide")
st.title("Man City Passing Stats Visualizations")

# Define the API URL (update if hosted elsewhere)
API_URL = "http://localhost:8000/passing-stats"

@st.cache_data(show_spinner=False)
def load_data():
    # Fetch the data from FastAPI
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        return df
    else:
        st.error("Failed to fetch data from API.")
        return pd.DataFrame()

# Load data
df = load_data()

if df.empty:
    st.write("No data available to display.")
else:
    st.write("### Raw Data")
    st.dataframe(df)

    st.sidebar.header("Visualization Options")
    vis_type = st.sidebar.selectbox("Select Visualization", ["Bar Chart", "Line Chart", "Scatter Plot"])

    if vis_type == "Bar Chart":
        st.subheader("Average Passing Completion % by Competition")
        # Group by competition and calculate average completion percentage
        if "Comp" in df.columns and "Cmp%" in df.columns:
            comp_avg = df.groupby("Comp")["Cmp%"].mean().reset_index()
            fig = px.bar(comp_avg, x="Comp", y="Cmp%", title="Average Pass Completion % by Competition",
                         labels={"Cmp%": "Average Completion %", "Comp": "Competition"})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("Required columns (Comp, Cmp%) not found in data.")

    #elif vis_type == "Line Chart":
     #   st.subheader("Passing Trends Over Time")
        # Make sure Date column is in datetime format
      #  if "Date" in df.columns and "Cmp" in df.columns:
       #     df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        #    df_sorted = df.sort_values("Date")
         #   fig = px.line(df_sorted, x="Date", y="Cmp", title="Completed Passes Over Time",
          #                labels={"Cmp": "Completed Passes", "Date": "Date"})
           # st.plotly_chart(fig, use_container_width=True)
        #else:
         #   st.write("Required columns (Date, Cmp) not found in data.")

    elif vis_type == "Line Chart":
        st.subheader("Relationship Between Attempts and Completions with Trendline")
    if "Date" in df.columns and "PrgP" in df.columns:
        # Convert Date to datetime, drop missing values, and sort
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date", "PrgP"])
        df["PrgP"] = df["PrgP"].astype(float)
        df = df.sort_values("Date")
        
        # Create a scatter plot with an OLS trendline
        fig = px.scatter(
            df, 
            x="Date", 
            y="PrgP", 
            trendline="ols",
            trendline_color_override="red",
            title="Progressive Passes Across the Seasons with Trendline",
            labels={"Date": "Date", "PrgP": "Completed Passes"}
        )
        # Update traces to show lines connecting points along with markers
        fig.update_traces(mode="lines+markers")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Required columns (Date, PrgP) not found in data.")
