import streamlit as st
import requests
import json

# Streamlit app title
st.title("Advert Processing")

# File upload components for the image and heatmap
image_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
heatmap_file = st.file_uploader("Upload Heatmap", type=["jpg", "jpeg", "png"])

if image_file and heatmap_file:
    # Display uploaded files
    st.image(image_file, caption="Uploaded Image", use_column_width=True)
    st.image(heatmap_file, caption="Uploaded Heatmap", use_column_width=True)

    # Convert files to binary
    image_data = image_file.getvalue()
    heatmap_data = heatmap_file.getvalue()

    # API endpoint URL
    api_url = (
        "http://localhost:8100/process_advert"  # Replace with your actual API endpoint
    )

    # Button to trigger API call
    if st.button("Process Advert"):
        # Make the API request
        response = requests.post(
            api_url, files={"image": image_data, "heatmap": heatmap_data}
        )

        # Check for a successful response
        if response.status_code == 200:
            result = response.json()
            st.success("API call successful!")
            st.json(result)  # Display the JSON response in a readable format
        else:
            st.error(f"API call failed with status code: {response.status_code}")
            st.text(response.text)
