import streamlit as st
import requests

# Streamlit app title
st.title("Advert Processing")

# File upload components for the image and heatmap
image_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
heatmap_file = st.file_uploader("Upload Heatmap", type=["jpg", "jpeg", "png"])

if image_file:
    # Display uploaded files
    st.image(image_file, caption="Uploaded Image", use_column_width=True)

if heatmap_file:
    st.image(heatmap_file, caption="Uploaded Heatmap", use_column_width=True)

# Button to trigger API call
clicked = st.button("Process Advert", disabled=not (image_file and heatmap_file))

if clicked:
    # Convert files to binary
    image_data = image_file.getvalue()
    heatmap_data = heatmap_file.getvalue()

    # API endpoint URL
    API_URL = (
        "http://backend:8080/process_advert"  # Replace with your actual API endpoint
    )
    # Make the API request
    response = requests.post(
        API_URL, files={"image": image_data, "heatmap": heatmap_data}
    )

    # Check for a successful response
    if response.status_code == 200:
        result = response.json()
        st.success("API call successful!")
        st.json(result)  # Display the JSON response in a readable format
    else:
        st.error(f"API call failed with status code: {response.status_code}")
        st.text(response.text)
