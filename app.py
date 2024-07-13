import streamlit as st
import requests

# Set your Amazon endpoint URL here
endpoint_url = "https://runtime.sagemaker.eu-north-1.amazonaws.com/endpoints/canvas-Group16ModelDeployment/invocations"

# Streamlit UI
st.title("Amazon Endpoint Connector")

# Text input from the user
input_text = st.text_area("Enter text to analyze")

# Button to submit the input
if st.button("Submit"):
    if input_text:
        # Data to be sent to the endpoint
        data = {"text": input_text}

        # Send a POST request to the endpoint
        response = requests.post(endpoint_url, json=data)

        # Check if the request was successful
        if response.status_code == 200:
            # Display the response from the endpoint
            st.write("Response from the endpoint:")
            st.write(response.json())
        else:
            st.write("Error:", response.status_code)
            st.write(response.text)
    else:
        st.write("Please enter some text before submitting.")

