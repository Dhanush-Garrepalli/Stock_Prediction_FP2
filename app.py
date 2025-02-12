import boto3
import pandas as pd
import streamlit as st

# Initialize a session using Amazon Forecast
session = boto3.Session(
    aws_access_key_id='AKIAU6GDV7LVBUZHSS5H',
    aws_secret_access_key='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',
    region_name='ap-south-1'
)

# Create a Forecast client
forecast = session.client('forecast')
forecast_query = session.client('forecastquery')

def filter_weekends(df):
    df['Date'] = pd.to_datetime(df['Timestamp'])
    df = df[~df['Date'].dt.dayofweek.isin([5, 6])]
    df = df.drop(columns=['Date'])
    return df

def get_forecast(forecast_arn, item_id, start_date, end_date):
    try:
        # Query the forecast
        forecast_response = forecast_query.query_forecast(
            ForecastArn=forecast_arn,
            Filters={"item_id": item_id}
        )

        # Extract the forecast data
        forecast_data = forecast_response['Forecast']['Predictions']

        # Check if 'p50' key exists in the predictions
        if 'p50' in forecast_data:
            # Convert to DataFrame
            df_forecast = pd.DataFrame(forecast_data['p50'])
            # Filter out weekends
            df_forecast = filter_weekends(df_forecast)
            # Filter the forecast data for the selected date range
            df_forecast['Date'] = pd.to_datetime(df_forecast['Timestamp']).dt.date
            df_forecast = df_forecast[(df_forecast['Date'] >= start_date) & (df_forecast['Date'] <= end_date)]
            if df_forecast.empty:
                st.write(f"No predictions available for {item_id} between {start_date} and {end_date}")
            return df_forecast
        else:
            st.write(f"No 'p50' predictions found for item_id: {item_id}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error querying forecast: {e}")
        return pd.DataFrame()

# List of stocks
stocks = ["dhanuka", "tcs", "infosys", "persistent", "cgpower", "shriramfinance", "hdfcbank", "reliance"]

# Streamlit UI
st.title("Forecast Dashboard")

# Select stock from dropdown
item_id = st.selectbox("Select Stock Name", stocks)
# Select start and end date from calendar
start_date = st.date_input("Select Start Date")
end_date = st.date_input("Select End Date")

if st.button("Get Forecast"):
    # Ensure end_date is not before start_date
    if start_date > end_date:
        st.error("End date must be after start date.")
    else:
        # Specify the forecast ARN
        forecast_arn = 'arn:aws:forecast:ap-south-1:339712801514:forecast/Group16_Forecast'
        df_forecast = get_forecast(forecast_arn, item_id, start_date, end_date)
        if not df_forecast.empty:
            st.write(f"Forecast for {item_id} from {start_date} to {end_date}")
            st.dataframe(df_forecast)
            st.download_button(
                label="Download data as CSV",
                data=df_forecast.to_csv(index=False).encode('utf-8'),
                file_name=f'forecast_{item_id}_{start_date}_to_{end_date}.csv',
                mime='text/csv',
            )
