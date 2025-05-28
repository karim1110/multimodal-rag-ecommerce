import os
import json
import pinecone
from tqdm import tqdm
import numpy as np
from sklearn.metrics import top_k_accuracy_score
from collections import defaultdict
import time

# Configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "multimodal"
EMBEDDING_DIM = 512  # CLIP base model uses 512-dimensional embeddings
BATCH_SIZE = 100  # Number of items to upsert at once
EVAL_SAMPLE_SIZE = 100  # Number of items to evaluate (set to 0 to skip evaluation)
print("Loaded Pinecone key:", bool(PINECONE_API_KEY))


def initialize_pinecone():
    """Initialize Pinecone connection and create index if needed"""
    pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)
    
    # Check if index exists
    if INDEX_NAME not in pc.list_indexes().names():
        print(f"Creating new Pinecone index '{INDEX_NAME}'...")
        pc.create_index(
            name=INDEX_NAME,
            dimension=EMBEDDING_DIM,
            metric="cosine",
            spec=pinecone.ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        print("Index created successfully!")
    
    return pc.Index(INDEX_NAME)

def prepare_vectors(embedding_data):
    """Convert embedding data to Pinecone vector format - only add if index is empty"""
    index = initialize_pinecone()
    stats = index.describe_index_stats()
    
    # Skip ID checking if index is empty (faster)
    if stats['total_vector_count'] > 0:
        print("Index already contains vectors - skipping upload to avoid duplicates")
        return []
    
    print("Index is empty - preparing all vectors for upload")
    vectors = []
    
    for item in tqdm(embedding_data, desc="Preparing vectors"):
        # Text embedding
        vectors.append({
            'id': f"{item['product_id']}_text",
            'values': item['text_embedding'],
            'metadata': item['metadata']
        })
        
        # Image embeddings
        for i, emb in enumerate(item['image_embeddings']):
            vectors.append({
                'id': f"{item['product_id']}_img_{i}",
                'values': emb,
                'metadata': {**item['metadata'], 'img_idx': i}
            })
    
    print(f"Prepared {len(vectors)} vectors for upload")
    return vectors

def evaluate_retrieval(index, embeddings, sample_size=100):
    """Fixed evaluation using exact ID matching"""
    print("\nRunning retrieval evaluation...")
    
    # Create ID to embedding mapping
    id_to_emb = {
        f"{e['product_id']}_text": e['text_embedding']
        for e in embeddings if 'text_embedding' in e
    }
    # Add image embeddings
    for e in embeddings:
        if 'image_embeddings' in e:
            for i, emb in enumerate(e['image_embeddings']):
                id_to_emb[f"{e['product_id']}_img_{i}"] = emb
    
    if len(id_to_emb) < sample_size:
        print(f"Not enough embeddings ({len(id_to_emb)}) for evaluation")
        return
    
    # Select random sample of IDs
    test_ids = np.random.choice(list(id_to_emb.keys()), size=min(sample_size, len(id_to_emb)), replace=False)
    
    # Evaluation metrics
    metrics = {
        'text': {'recall@1': 0, 'recall@5': 0, 'recall@10': 0},
        'image': {'recall@1': 0, 'recall@5': 0, 'recall@10': 0}
    }
    total = 0
    
    for vec_id in tqdm(test_ids, desc="Evaluating"):
        vec_type = 'text' if vec_id.endswith('_text') else 'image'
        query_vec = id_to_emb[vec_id]
        
        try:
            results = index.query(
                vector=query_vec,
                top_k=10,
                include_metadata=True,
                filter={"type": {"$eq": vec_type}}  # Only search same type
            )
            
            retrieved_ids = [m['id'] for m in results['matches']]
            true_id = vec_id
            
            for k in [1, 5, 10]:
                if true_id in retrieved_ids[:k]:
                    metrics[vec_type][f'recall@{k}'] += 1
            
            total += 1
            
        except Exception as e:
            print(f"Error evaluating {vec_id}: {str(e)}")
    
    # Calculate final metrics
    print("\nEvaluation Results:")
    for vec_type in ['text', 'image']:
        if total > 0:
            print(f"\n{vec_type.capitalize()} Retrieval:")
            for k in [1, 5, 10]:
                recall = metrics[vec_type][f'recall@{k}'] / total
                print(f"Recall@{k}: {recall:.2%}")
    
    return metrics

def main(embeddings_path="embeddings/all_embeddings.json"):
    """Optimized main function"""
    # Load embeddings
    print(f"Loading embeddings from {embeddings_path}...")
    with open(embeddings_path) as f:
        embeddings = json.load(f)
    
    # Initialize Pinecone and prepare vectors
    index = initialize_pinecone()
    vectors = prepare_vectors(embeddings)  # This now handles all existence checking
    
    # Only proceed if we have vectors to upsert
    if vectors:
        # Upsert in batches
        for i in tqdm(range(0, len(vectors), BATCH_SIZE), desc="Upserting"):
            index.upsert(vectors=vectors[i:i+BATCH_SIZE])
    
    # Always run evaluation (uses existing index)
    evaluate_retrieval(index, embeddings)
    
    print(f"\nFinal stats: {index.describe_index_stats()}")
    
if __name__ == "__main__":
    main()
