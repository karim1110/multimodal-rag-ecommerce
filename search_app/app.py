import streamlit as st

from chatbot_backend import query_vector_db as get_chatbot_response

# --- Page Config ---
st.set_page_config(page_title="Search a Product from Amazon", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
    /* Set the entire body background to Amazon blue */
    body {
        background-color: #146eb4; /* Amazon blue */
        color: white; /* Default text color for the entire app */
    }

    /* Target Streamlit's main content area container to ensure background color */
    .stApp {
        background-color: #146eb4; /* Ensure the main app content area is Amazon blue */
        color: white; /* Ensure text within the app is white */
    }

    /* Override Streamlit's internal header bar at the very top */
    .stApp > header {
        background-color: #146eb4; /* Amazon blue */
    }

    /* Adjust Streamlit's top-level container padding for a cleaner look */
    .stApp > div:first-child > div:first-child > div:first-child {
        padding-top: 0rem; /* Remove top padding if it creates a white gap */
        padding-bottom: 0rem; /* Remove bottom padding */
    }

    /* Ensure .main-container and .header are also Amazon blue and have white text */
    .main-container {
        width: 100%;
        padding-left: 1rem;
        padding-right: 1rem;
        background-color: #146eb4; /* Ensure this is also Amazon blue */
        color: white; /* All text within it is white */
    }
    .header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
        justify-content: flex-start;
        background-color: #146eb4; /* Ensure header itself is Amazon blue */
        padding-top: 1rem; /* Add some padding to the top of the header area */
        padding-bottom: 1rem; /* Add some padding to the bottom of the header area */
    }
    .header-title {
        font-size: 28px;
        font-weight: 700;
        margin: 0;
        color: white; /* Make title white */
        text-align: left;
    }
    .header-subtitle {
        font-size: 16px;
        color: #E0E0E0; /* Slightly lighter white for subtitle, or just white */
        text-align: left;
        margin-top: -10px;
        margin-bottom: 20px;
    }

    /* Product card styling for dark background */
    .product-card {
        background-color: #1F7ACC; /* Slightly darker blue for card background for contrast */
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2); /* Darker shadow for contrast */
        margin-bottom: 1rem;
        color: white; /* Text in product card is white */
    }
    .product-card .st-cq { /* Target st.caption specifically inside product cards */
        color: #B0B0B0; /* Lighter grey for captions */
    }

    /* Streamlit Button styling */
    .stButton>button {
        background-color: #ff9900; /* Amazon orange */
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #e68a00; /* Darker orange on hover */
    }

    /* Adjust text input field background and color */
    .stTextInput > div > div > input {
        background-color: #1F7ACC !important; /* Darker input field background */
        color: white !important; /* Text inside input field (typed text) */
        border: 1px solid #2B8ED9 !important; /* Border color */
    }

    /* Make placeholder text white */
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.7) !important; /* White with some transparency */
    }
    .stTextInput > label span {
        color: white !important; /* Label for text input */
    }

    /* Adjust file uploader background and color */
    .stFileUploader > div > div {
        background-color: #1F7ACC !important; /* Darker file uploader background */
        color: white !important; /* Text inside file uploader */
        border: 1px solid #2B8ED9 !important; /* Border color */
    }
    .stFileUploader label span {
        color: white !important; /* File uploader label text */
    }
    .stFileUploader button {
        color: white !important; /* Browse Files button text */
        background-color: #2B8ED9 !important; /* Browse Files button background */
    }
    .stFileUploader button:hover {
        background-color: #3C9AE0 !important;
    }

    /* Adjust Tab styling for dark background */
    .stTabs [data-baseweb="tab-list"] button {
        color: white !important; /* Tab labels */
        background-color: transparent !important; /* Make tab button background transparent */
    }
    .stTabs [data-baseweb="tab-list"] button:hover {
        background-color: #2B8ED9 !important; /* Hover for tabs */
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #146eb4 !important; /* Active tab background */
    }
    .stTabs [data-baseweb="tab-list"] [aria-selected="true"] {
        color: #ff9900 !important; /* Selected tab text color */
        border-bottom-color: #ff9900 !important; /* Underline for selected tab */
    }

    /* Streamlit success/info/warning messages */
    .stSuccess, .stInfo, .stWarning {
        background-color: #1F7ACC !important; /* Darker background for messages */
        color: white !important; /* White text for messages */
        border-left: 5px solid #ff9900 !important; /* Amazon orange bar */
    }

    /* Explicitly make markdown text in lists white */
    .stMarkdown ul li {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header (will now be Amazon blue) ---
st.markdown("""
<div class="main-container">
    <div class="header">
        <img src='https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg' width='150'/>
        <h1 class='header-title'>Search a Product from Amazon</h1>
    </div>
    <p class='header-subtitle'>Ask about a product using <strong>text</strong>, <strong>image</strong>, or both.</p>
</div>
""", unsafe_allow_html=True)

# --- Input + Samples Side-by-Side ---
col1, col2 = st.columns([3, 2]) # Keep the section ratio as requested

with col1:
    st.subheader("🔍 What brings you here today?") # This header will now be white
    tab1, tab2 = st.tabs(["📝 Text", "🌞 Image"])

    with tab1:
        text_query = st.text_input("Product question", placeholder="e.g. What's the resolution of Samsung TV?")
    with tab2:
        uploaded_image = st.file_uploader("Upload product image", type=["jpg", "jpeg", "png"])

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
        # Determine if it's a text query, image query, or both
        if text_query and uploaded_image:
            response = get_chatbot_response(image=uploaded_image)
            st.warning("Both text and image provided. Processing based on image for now.")
        elif text_query:
            response = get_chatbot_response(text=text_query)
        elif uploaded_image:
            response = get_chatbot_response(image=uploaded_image)
        else:
            response = get_chatbot_response()

    st.success("✅ Here's what we found:")
    st.markdown("### 💬 Chatbot Response")
    st.markdown(response["answer"])

    if response["image_url"]:
        st.image(response["image_url"], caption="Identified Product", use_container_width=True)

    # In your frontend code (app.py), modify the product card section:
    if response["retrieved_items"]:
        st.markdown("### 📚 Related Products")
        num_items = len(response["retrieved_items"])
        if num_items > 0:
            result_cols = st.columns(min(num_items, 3))

            for i, item in enumerate(response["retrieved_items"]):
                if i < 3:
                    with result_cols[i]:
                        st.markdown("<div class='product-card'>", unsafe_allow_html=True)
                        if item["image"] is not None:
                            st.image(item["image"], use_container_width=True)
                        st.markdown(f"**{item['title']}**")
                        st.caption(item["description"])
                        st.markdown("</div>", unsafe_allow_html=True)

