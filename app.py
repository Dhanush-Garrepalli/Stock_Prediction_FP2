import streamlit as st
import boto3
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use Streamlit secrets to get AWS credentials
try:
    aws_access_key_id = st.secrets["AWS_ACCESS_KEY_ID"]
    aws_secret_access_key = st.secrets["AWS_SECRET_ACCESS_KEY"]
    region_name = st.secrets["AWS_DEFAULT_REGION"]
except KeyError as e:
    st.error(f"Missing required secrets: {e}")
    logger.error(f"Missing required secrets: {e}")
    st.stop()

# Initialize the boto3 client for SageMaker
try:
    sagemaker_client = boto3.client(
        'sagemaker-runtime',
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
except Exception as e:
    st.error("Failed to initialize the SageMaker client.")
    logger.error(f"Failed to initialize the SageMaker client: {e}")
    st.stop()

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
    try:
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
    except sagemaker_client.exceptions.EndpointConnectionError as e:
        st.error("Failed to connect to the SageMaker endpoint.")
        logger.error(f"Failed to connect to the SageMaker endpoint: {e}")
    except Exception as e:
        st.error("An error occurred while making the prediction.")
        logger.error(f"An error occurred while making the prediction: {e}")
