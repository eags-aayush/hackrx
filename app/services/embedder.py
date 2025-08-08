from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks):
    return model.encode(chunks).tolist()


def embed_query(text):
    return model.encode([text])[0].tolist()