import streamlit as st
import boto3
import json

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

# Define the endpoint name
endpoint_name = 'canvas-FP2-Test-Deployment-2'

# Streamlit UI
st.title("Stock Forecast")

# User inputs
ticker = st.text_input("Enter Ticker", "AAPL")
days = st.number_input("Number of Days for Forecast", min_value=1, step=1)

# Prepare the payload
features = {
    "ticker": ticker,
    "days": days
}

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
