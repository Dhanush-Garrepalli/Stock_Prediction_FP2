import streamlit as st
import pandas as pd
import boto3
import json
from datetime import datetime

# Set AWS credentials as environment variables (for local testing, not needed for Streamlit Cloud if you use Secrets Management)
import os
os.environ['AWS_ACCESS_KEY_ID'] = 'AKIAU6GDV7LVBUZHSS5H'
os.environ['AWS_SECRET_ACCESS_KEY'] = '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'
os.environ['AWS_DEFAULT_REGION'] = 'Global'

# Initialize the boto3 client for SageMaker
sagemaker_client = boto3.client('sagemaker-runtime', region_name=os.environ['AWS_DEFAULT_REGION'])

# Load the dataset
file_path = 'https://github.com/Dhanush-Garrepalli/Stock_Prediction_FP2/blob/main/DhanukaAgritech_Historical_Data.csv'  # Ensure this is the correct path to your dataset
data = pd.read_csv(file_path)

# The endpoint name
endpoint_name = 'canvas-FP2-Test-Deployment-2'

# Streamlit UI
st.title("Stock Forecast")

# User inputs
ticker = st.selectbox("Select Ticker", data['ticker'].unique())
forecast_date = st.date_input("Select Forecast Date", datetime.today())

# Filter the data for the selected ticker
filtered_data = data[data['ticker'] == ticker]

if not filtered_data.empty:
    # For simplicity, we'll use the first row of the filtered dataset for the prediction
    row = filtered_data.iloc[0]
    features = row.drop('closePrice').to_dict()
    
    # Convert the payload to JSON format
    payload = json.dumps(features)

    # Make prediction
    if st.button("Get Forecast"):
        response = sagemaker_client.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType='application/json',
            Body=payload
        )

        # Parse the response
        result = json.loads(response['Body'].read().decode())

        # Display the forecast result
        st.write(f"Ticker: {ticker}")
        st.write(f"Forecast Date: {forecast_date}")
        st.write(f"Forecasted Close Price: {result['predicted_value']}")
else:
    st.write("No data available for the selected ticker.")
