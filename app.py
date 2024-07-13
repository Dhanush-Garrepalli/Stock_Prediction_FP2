import streamlit as st
import boto3
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# AWS Forecast settings
REGION_NAME = "ap-south-1"
FORECAST_ARN = "arn:aws:forecast:ap-south-1:339712801514:forecast/Group16_Forecast"

# Initialize AWS Forecast client
client = boto3.client('forecastquery', region_name=REGION_NAME)

# Load dataset
file_url = 'https://raw.githubusercontent.com/Dhanush-Garrepalli/Stock_Prediction_FP2/main/Group-16_FP2_dataset_final_1.csv'

# Read the dataset
try:
    dataset = pd.read_csv(file_url, delimiter=',', on_bad_lines='skip')
    stock_names = dataset['stock_name'].unique()
except pd.errors.ParserError as e:
    st.error(f"Error parsing CSV file: {e}")
    st.stop()
except Exception as e:
    st.error(f"An unexpected error occurred while reading the CSV file: {e}")
    st.stop()

def get_forecast_data(forecast_arn, item_id):
    try:
        # Fetch forecast data from AWS
        response = client.query_forecast(
            ForecastArn=forecast_arn,
            Filters={"item_id": item_id}
        )
        logging.debug(f"Response: {response}")
        forecast_data = response['Forecast']['Predictions']
        
        # Convert to DataFrame
        df = pd.DataFrame(forecast_data['p10'], columns=['Timestamp', 'p10'])
        df['p50'] = [x['Value'] for x in forecast_data['p50']]
        df['p90'] = [x['Value'] for x in forecast_data['p90']]
        return df
    except Exception as e:
        logging.error(f"Error querying forecast: {e}")
        st.error(f"Error querying forecast: {e}")
        return pd.DataFrame()

st.title('AWS Forecast Data Viewer')

# Dropdown for selecting stock name (item_id)
selected_stock = st.selectbox('Select Stock', stock_names)

if selected_stock:
    # Retrieve forecast data for the selected stock
    data = get_forecast_data(FORECAST_ARN, selected_stock)

    if not data.empty:
        st.write(f'Forecast Data for {selected_stock}')
        st.write(data)

        # Plot the data
        st.line_chart(data.set_index('Timestamp'))
    else:
        st.write('No data available')
