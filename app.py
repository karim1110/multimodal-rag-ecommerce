import os
os.environ["STREAMLIT_SERVER_ENABLE_FILE_WATCHER"] = "false"


from chatbot_backend import query_vector_db as get_chatbot_response
import streamlit as st
import io # Import io module for handling uploaded file as bytes

import pandas as pd

# --- Page Config ---
st.set_page_config(page_title="Search a Product from Amazon", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
    /* Dark theme colors */
    :root {
        --dark-bg: #121212;  /* Dark grey/black */
        --darker-blue: #0a1a2e;  /* Dark blue alternative */
        --card-bg: #1e1e1e;  /* Slightly lighter for cards */
        --text-color: #ffffff;  /* White text */
        --accent-color: #ff9900;  /* Amazon orange for accents */
    }
    
    /* Set the entire body background */
    body {
        background-color: var(--dark-bg);
        color: var(--text-color);
    }

    /* Target Streamlit's main content area */
    .stApp {
        background-color: var(--dark-bg);
        color: var(--text-color);
    }

    /* Override Streamlit's internal header */
    .stApp > header {
        background-color: var(--dark-bg) !important;
    }

    /* Adjust padding */
    .stApp > div:first-child > div:first-child > div:first-child {
        padding-top: 0rem;
        padding-bottom: 0rem;
    }

    /* Main container styling */
    .main-container {
        width: 100%;
        padding-left: 1rem;
        padding-right: 1rem;
        background-color: var(--dark-bg);
        color: var(--text-color);
    }
    
    /* Header styling */
    .header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
        justify-content: flex-start;
        background-color: var(--dark-bg);
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Product card styling */
    .product-card {
        background-color: var(--card-bg);
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        margin-bottom: 1rem;
        color: var(--text-color);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        border: 1px solid #333;  /* subtle border */
    }

    /* Rest of your existing CSS remains the same, just update color references */
    .header-title {
        font-size: 28px;
        font-weight: 700;
        margin: 0;
        color: var(--text-color);
        text-align: left;
    }
    
    .header-subtitle {
        font-size: 16px;
        color: #E0E0E0;
        text-align: left;
        margin-top: -10px;
        margin-bottom: 20px;
    }
    
    .stButton>button {
        background-color: var(--accent-color);
        color: var(--text-color);
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        font-size: 16px;
    }
    
    /* Update input fields */
    .stTextInput > div > div > input {
        background-color: #2a2a2a !important;
        color: var(--text-color) !important;
        border: 1px solid #444 !important;
    }
    
    /* Update file uploader */
    .stFileUploader > div > div {
        background-color: #2a2a2a !important;
        color: var(--text-color) !important;
        border: 1px solid #444 !important;
    }
    
    /* Keep the rest of your existing CSS */
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="main-container">
    <div class="header">
        <img src='https://www.marcellus.michlibrary.org/site-assets/images/amazon-logo.jpg/@@images/image.jpeg' width='150'/>
        <h1 class='header-title'>Search a Product from Amazon</h1>
    </div>
    <p class='header-subtitle'>Ask about a product using <strong>text</strong>, <strong>image</strong>, or both.</p>
</div>
""", unsafe_allow_html=True)

# --- Input + Samples Side-by-Side ---
col1, col2 = st.columns([3, 2]) # Keep the section ratio as requested

with col1:
    st.subheader("🔍 What brings you here today?") # This header will now be white
    
    # Combined text and image input in one section
    text_query = st.text_input("Product question", placeholder="e.g. What's the resolution of Samsung TV?")
    uploaded_image = st.file_uploader("Upload product image (optional)", type=["jpg", "jpeg", "png"])
    
    search = st.button("Search 🔍")

with col2:
    st.subheader("💡 Sample Questions You Can Try") # This header will now be white
    st.markdown("- **What are the features of the Samsung Galaxy S21?**")
    st.markdown("- **Compare Amazon Echo Dot vs Google Nest Mini**")
    st.markdown("- **What is this product used for?** *(upload image)*")
    st.markdown("- **Can you show me a picture of the Apple AirPods Pro?**")
    st.markdown("- **What is the name of this product, and how do I use it?** *(upload image)*")

# --- Search Results ---
if search:
    with st.spinner("Retrieving results..."):
        # If an image is uploaded, pass its byte stream to the backend
        image_stream = None
        if uploaded_image:
            image_stream = io.BytesIO(uploaded_image.getvalue())

        # Determine the type of query and call the backend
        response = get_chatbot_response(text=text_query, image=image_stream)
        preprocessed_df=pd.read_csv("marketing_sample_for_amazon_com-ecommerce__20200101_20200131__10k_data.csv")
        product_id_url=response['retrieved_items'][5]['product_id']
        image_url=preprocessed_df[preprocessed_df['Uniq Id']==product_id_url]['Image']
        if not image_url.empty:
            response["image_url"] = image_url.values[0]
        else:
            response["image_url"] = None

    st.success("✅ Here's what we found:")
    st.markdown("### 💬 Chatbot Response")
    st.markdown(response["answer"])

    # Display the main product image if available and requested by LLM
    if response["image_url"]:
        st.markdown("---")
        st.markdown("### 🖼️ Identified Product Image")
        st.image(response["image_url"], caption="Identified Product", use_container_width=False, width=300) # You can adjust width

    # Display related products with their images
    if response["retrieved_items"]:
        st.markdown("---")
        st.markdown("### 📚 Related Products")
        
        # Filter out items that don't have an image to ensure cleaner display for products with images
        #items_without_images = [item for item in response["retrieved_items"][0:4]]
        items_with_images = [item for item in response["retrieved_items"][5:9]]

        if items_with_images:
            st.markdown("#### Products with Images:")
            # Display up to 3 products per row
            num_items_to_display = len(items_with_images)
            for i in range(1, num_items_to_display, 3):
                cols = st.columns(min(3, num_items_to_display - i))
                for j in range(min(3, num_items_to_display - i)):
                    item = items_with_images[i + j]
                    with cols[j]:
                        st.markdown("<div class='product-card'>", unsafe_allow_html=True)
                        product_id_url = item['product_id']
                        image_url = preprocessed_df[preprocessed_df['Uniq Id'] == product_id_url]['Image']
                        if not image_url.empty:
                            st.image(image_url.values[0], use_container_width=True)
                        st.markdown(f"**{item['title']}**")
                        st.caption(item["description"])
                        st.markdown("</div>", unsafe_allow_html=True)
        
        # if items_without_images:
        #     st.markdown("#### Other Related Products (No Image Available):")
        #     for item in items_without_images:
        #         st.markdown(f"- **{item['title']}** - {item['description']}")