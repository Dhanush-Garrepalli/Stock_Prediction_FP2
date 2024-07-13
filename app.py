import streamlit as st
import boto3
import pandas as pd

# AWS Forecast settings
REGION_NAME = "ap-south-1"
FORECAST_ARN = "arn:aws:forecast:ap-south-1:339712801514:forecast/Group16_Forecast"

# Initialize AWS Forecast client
client = boto3.client('forecast', region_name=REGION_NAME)

def get_forecast_data(forecast_arn):
    # Fetch forecast data from AWS
    response = client.query_forecast(
        ForecastArn=forecast_arn,
        Filters={"item_id": "1"}  # Adjust the filter based on your dataset
    )
    forecast_data = response['Forecast']['Predictions']
    
    # Convert to DataFrame
    df = pd.DataFrame(forecast_data['p10'], columns=['Timestamp', 'p10'])
    df['p50'] = [x['Value'] for x in forecast_data['p50']]
    df['p90'] = [x['Value'] for x in forecast_data['p90']]
    return df

st.title('AWS Forecast Data Viewer')

# Retrieve forecast data
data = get_forecast_data(FORECAST_ARN)

st.write('Forecast Data')
st.write(data)

# Plot the data
st.line_chart(data.set_index('Timestamp'))
