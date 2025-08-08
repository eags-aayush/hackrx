import os
from app.services.parser import extract_text
from app.services.chunker import chunk_text
from app.services.embedder import embed_chunks
from app.services.retriever import save_to_faiss

UPLOAD_DIR = "data/uploads"

def index_all_documents():
    all_chunks = []
    all_metadatas = []

    for filename in os.listdir(UPLOAD_DIR):
        if not filename.endswith((".pdf", ".docx", ".txt")):
            continue

        file_path = os.path.join(UPLOAD_DIR, filename)
        print(f"[+] Extracting: {filename}")
        text = extract_text(file_path)
        if not text:
            print(f"[!] Skipping empty: {filename}")
            continue

        chunks = chunk_text(text)
        all_chunks.extend(chunks)

        all_metadatas.extend([
            {
                "source": filename,
                "chunk_index": i,
                "text": chunk
            } for i, chunk in enumerate(chunks)
        ])

    print(f"[✓] Total chunks: {len(all_chunks)}")

    embeddings = embed_chunks(all_chunks)

    save_to_faiss(embeddings, all_metadatas)
    print("[✓] Indexing complete and saved to FAISS.")

if __name__ == "__main__":
    index_all_documents()
