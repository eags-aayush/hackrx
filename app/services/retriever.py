import faiss
import os
import json
import numpy as np

def save_to_faiss(embeddings, metadatas, index_path="vector_store/faiss_index/index"):
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)

    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    vectors = np.array(embeddings).astype("float32")
    index.add(vectors)

    faiss.write_index(index, index_path)

    with open(index_path + "_metadata.json", "w") as f:
        json.dump(metadatas, f)

def load_faiss_index(index_path="vector_store/faiss_index/index"):
    index = faiss.read_index(index_path)
    with open(index_path + "_metadata.json") as f:
        metadata = json.load(f)
    return index, metadata

def retrieve_chunks(query):
    from app.services import embedder
    index, metadata = load_faiss_index()
    query_vec = np.array([embedder.embed_query(query)]).astype('float32')
    D, I = index.search(query_vec, k=10)  
    chunks = [metadata[i] for i in I[0] if i < len(metadata)]

    keywords = ["surgery", "hospitalization", "waiting period", "covered", "pre-existing", "treatment", "day care", "exclusion"]
    relevant_chunks = []
    for chunk in chunks:
        text_lower = chunk["text"].lower()
        if any(keyword in text_lower for keyword in keywords):
            relevant_chunks.append(chunk)

    return relevant_chunks if relevant_chunks else chunks
