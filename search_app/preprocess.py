import os
import pandas as pd
import kagglehub
import requests
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
from tqdm import tqdm
import numpy as np
import json
from io import BytesIO
import time

# Create necessary directories
os.makedirs("dataset/images", exist_ok=True)
os.makedirs("embeddings", exist_ok=True)
os.makedirs("vectordb", exist_ok=True)

# Download dataset
print("Downloading Amazon Product Dataset 2020...")
path = kagglehub.dataset_download("promptcloud/amazon-product-dataset-2020")
path = os.path.join(os.path.join(path,"home"),"sdf")
print(f"Dataset path: {path}")

print("Loading dataset...")
csv_file = os.listdir(path)[0]
data_file = os.path.join(path, csv_file)
df = pd.read_csv(data_file)

# Preprocessing
print("Preprocessing data...")
columns_to_use = ['Uniq Id', 'Product Name', 'Category', 'Selling Price', 
                 'About Product', 'Product Specification', 'Image']
df = df[[col for col in columns_to_use if col in df.columns]]
df = df.dropna(subset=['Product Name']).fillna("")
df['description'] = df['Product Name'] + ' ' + df['About Product'] + ' ' + df['Product Specification']
df['description'] = df['description'].str.strip()

# Save preprocessed data
df.to_csv("dataset/preprocessed_data.csv", index=False)
print(f"Preprocessed data saved with {len(df)} products")

# Load CLIP model with fast processor
print("Loading CLIP model...")
device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)

# Initialize both with use_fast=True
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32", use_fast=True)
tokenizer = processor.tokenizer  # Get the tokenizer from processor

def download_image(url, product_id, retries=3):
    """Download and save an image with retries"""
    for attempt in range(retries):
        try:
            response = requests.get(url, stream=True, timeout=10)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content)).convert('RGB')
                img_path = f"dataset/images/{product_id}.jpg"
                img.save(img_path)
                return img_path
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {url}: {str(e)}")
            time.sleep(2)
    return None

def process_image_urls(image_urls, product_id):
    """Process multiple image URLs for a product"""
    if pd.isna(image_urls) or not isinstance(image_urls, str):
        return None
    
    # Clean URLs and take first valid one
    urls = [url.strip() for url in image_urls.split('|') if url.strip()]
    for url in urls:
        if any(url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp']):
            # Fix common URL issues
            if url.startswith('https:/') and not url.startswith('https://'):
                url = url.replace('https:/', 'https://')
            elif url.startswith('http:/') and not url.startswith('http://'):
                url = url.replace('http:/', 'http://')
                
            img_path = download_image(url, product_id)
            if img_path:
                return img_path
    return None

def generate_embeddings(row):
    """Generate embeddings for a product with all images"""
    product_id = row['Uniq Id']
    
    # Enhanced text with metadata
    enhanced_text = (
        f"Product: {row['Product Name']}. "
        f"Category: {row['Category']}. "
        f"Price: {row['Selling Price']}. "
        f"Description: {row['About Product']}. "
        f"Specs: {row['Product Specification']}"
    )
    
    # Text embedding
    text_inputs = tokenizer(enhanced_text, return_tensors="pt", padding=True, truncation=True).to(device)
    with torch.no_grad():
        text_embedding = model.get_text_features(**text_inputs).cpu().numpy().flatten()
    
    # Process ALL images
    image_embeddings = []
    image_paths = []
    
    if pd.notna(row['Image']):
        urls = [url.strip() for url in row['Image'].split('|') if url.strip()]
        
        for i, url in enumerate(urls):
            # Skip placeholder images
            if any(placeholder in url.lower() 
                   for placeholder in ['transparent-pixel', 'placeholder', 'no-image']):
                continue
                
            img_path = f"dataset/images/{product_id}_{i}.jpg"
            
            # Download image if not already exists
            if not os.path.exists(img_path):
                try:
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        Image.open(BytesIO(response.content)).convert('RGB').save(img_path)
                except Exception as e:
                    print(f"Failed to download {url}: {str(e)}")
                    continue
            
            # Generate embedding for each valid image
            if os.path.exists(img_path):
                try:
                    image = Image.open(img_path)
                    image_inputs = processor(images=image, return_tensors="pt").to(device)
                    with torch.no_grad():
                        img_embedding = model.get_image_features(**image_inputs).cpu().numpy().flatten()
                    
                    image_embeddings.append(img_embedding.tolist())
                    image_paths.append(img_path)
                except Exception as e:
                    print(f"Error processing {img_path}: {str(e)}")
    
    return {
        "product_id": product_id,
        "text_embedding": text_embedding.tolist(),
        "image_embeddings": image_embeddings,  # List of all image embeddings
        "image_paths": image_paths,  # List of all image paths
        "metadata": {
            "name": row['Product Name'],
            "category": row['Category'],
            "price": row['Selling Price']
        }
    }

# Generate embeddings for all products
print(f"Generating embeddings for {len(df)} products...")
embeddings = []
failed_products = []

for _, row in tqdm(df.iterrows(), total=len(df)):
    try:
        embedding = generate_embeddings(row)
        embeddings.append(embedding)
    except Exception as e:
        print(f"Failed to process product {row['Uniq Id']}: {str(e)}")
        failed_products.append(row['Uniq Id'])

# Save results
with open("embeddings/all_embeddings.json", "w") as f:
    json.dump(embeddings, f, indent=2)

print(f"\nCompleted! Successfully processed {len(embeddings)} products")
print(f"Failed to process {len(failed_products)} products")
if failed_products:
    print("Failed product IDs:", failed_products)