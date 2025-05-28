import streamlit as st

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
            response = get_chatbot_response(image_file=uploaded_image)
            st.warning("Both text and image provided. Processing based on image for now.")
        elif text_query:
            response = get_chatbot_response(text_query=text_query)
        elif uploaded_image:
            response = get_chatbot_response(image_file=uploaded_image)
        else:
            response = get_chatbot_response()

    st.success("✅ Here's what we found:")
    st.markdown("### 💬 Chatbot Response")
    st.markdown(response["answer"])

    if response["image_url"]:
        st.image(response["image_url"], caption="Identified Product", use_column_width=True)

    if response["retrieved_items"]:
        st.markdown("### 📚 Related Products")
        num_items = len(response["retrieved_items"])
        if num_items > 0:
            result_cols = st.columns(min(num_items, 3))

            for i, item in enumerate(response["retrieved_items"]):
                if i < 3:
                    with result_cols[i]:
                        st.markdown("<div class='product-card'>", unsafe_allow_html=True)
                        st.image(item["image"], use_column_width=True)
                        st.markdown(f"**{item['title']}**")
                        st.caption(item["description"])
                        st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No related products found for this query.")


# --- Backend Placeholder Functions (Replace with your actual model calls) ---
def get_chatbot_response(text_query=None, image_file=None):
    """
    This function will simulate the backend calls to your multimodal chatbot.
    In a real scenario, this would:
    1. Send text_query and/or image_file to your RAG system.
    2. Utilize CLIP for embedding generation.
    3. Query your vector database (e.g., Google Vertex AI Vector Search) for retrieval.
    4. Pass the retrieved context to your LLM (e.g., Meta-Llama-3.1 or Mixtral).
    5. Generate the final multimodal response.
    """
    if text_query:
        if "Samsung Galaxy S21" in text_query:
            return {
                "answer": "The Samsung Galaxy S21 comes with a 6.2-inch Dynamic AMOLED display, a triple-camera setup (12MP wide, 64MP telephoto, 12MP ultrawide), and a 4000mAh battery.",
                "image_url": None,
                "retrieved_items": []
            }
        elif "compare" in text_query and "Amazon Echo Dot" in text_query and "Google Nest Mini" in text_query:
            return {
                "answer": "The Amazon Echo Dot features Alexa voice assistant, a 1.6-inch speaker, and Bluetooth connectivity. The Google Nest Mini, on the other hand, comes with Google Assistant, a 40mm driver, and supports both Bluetooth and Wi-Fi. Both devices are designed for smart home control and music playback, but the choice depends on your preferred ecosystem (Amazon Alexa or Google Assistant).",
                "image_url": None,
                "retrieved_items": []
            }
        elif "Apple AirPods Pro" in text_query and ("show me a picture" in text_query or "picture of" in text_query):
            return {
                "answer": "Sure, here is an image of the Apple AirPods Pro: The AirPods Pro features active noise cancellation, a customizable fit with silicone tips, and are sweat and water-resistant, making them ideal for workouts and daily use.",
                "image_url": "https://m.media-amazon.com/images/I/71SUjE2d7TL._AC_SL1500_.jpg",
                "retrieved_items": []
            }
        elif "Samsung TV" in text_query and "resolution" in text_query:
            return {
                "answer": "This is the **Samsung 4K UHD Smart TV**. It features a crystal display, HDR, built-in Alexa, and 3 HDMI ports.",
                "image_url": "https://m.media-amazon.com/images/I/81c+9BOQNWL._AC_SL1500_.jpg",
                "retrieved_items": [
                    {
                        "title": "Samsung Crystal UHD 55-Inch",
                        "description": "4K UHD HDR Smart TV with Alexa Built-In, 3 HDMI, Motion Xcelerator.",
                        "image": "https://m.media-amazon.com/images/I/81c+9BOQNWL._AC_SL1500_.jpg"
                    },
                    {
                        "title": "LG 55-Inch 4K Smart TV",
                        "description": "AI-powered, webOS, built-in streaming apps, voice remote.",
                        "image": "https://m.media-amazon.com/images/I/71ZJL7xDfCL._AC_SL1500_.jpg"
                    }
                ]
            }
        else:
            return {
                "answer": "I'm not sure how to answer that specific text query yet. Please try another sample question or provide more details.",
                "image_url": None,
                "retrieved_items": []
            }
    elif image_file:
        # Simulate image processing and product identification
        # In a real scenario, you'd pass image_file.getvalue() to your model
        # and get a response based on the image content.
        if uploaded_image:
             return {
                "answer": "This is a **KitchenAid Artisan Stand Mixer**. It is used for mixing, kneading, and whipping ingredients, making it ideal for baking and cooking tasks. It comes with multiple attachments for various culinary tasks, such as making pasta or grinding meat.",
                "image_url": None, # No additional image to display for this type of query
                "retrieved_items": []
            }
        else:
            return {
                "answer": "I can identify products from images. Please upload an image to proceed.",
                "image_url": None,
                "retrieved_items": []
            }
    else:
        return {
            "answer": "Please provide either a text question or an image to get a response.",
            "image_url": None,
            "retrieved_items": []
        }
