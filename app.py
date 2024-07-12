import streamlit as st
import pandas as pd
import boto3
import json
from datetime import datetime, timedelta

# Use Streamlit secrets to get AWS credentials
aws_access_key_id = st.secrets["AWS_ACCESS_KEY_ID"]
aws_secret_access_key = st.secrets["AWS_SECRET_ACCESS_KEY"]
region_name = st.secrets["AWS_DEFAULT_REGION"]

# Initialize the boto3 client for SageMaker
sagemaker_client = boto3.client(
    'sagemaker-runtime',
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

# Streamlit UI
st.title("Stock Forecast")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    data = pd.read_csv(uploaded_file)
    
    # Display the columns of the dataframe
    st.write("Columns in the dataset:")
    st.write(data.columns)
    
    # Ensure the ticker column exists in the dataset
    if 'ticker' not in data.columns:
        st.error("The dataset must contain a 'ticker' column.")
    else:
        # User inputs
        ticker = st.selectbox("Select Ticker", data['ticker'].unique())
        days = st.number_input("Number of Days for Forecast", min_value=1, step=1)

        # Filter the data for the selected ticker
        filtered_data = data[data['ticker'] == ticker]

        if not filtered_data.empty:
            # For simplicity, we'll use the first row of the filtered dataset for the prediction
            row = filtered_data.iloc[0]
            features = row.drop('closePrice').to_dict()
            
            # Adding number of days to the features
            features['days'] = days
            
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
                st.write(f"Forecast Days: {days}")
                st.write(f"Forecasted Close Price: {result['predicted_value']}")
        else:
            st.write("No data available for the selected ticker.")
