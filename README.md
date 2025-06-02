# Fraternity Bylaws Assistant for the Beta-Iota Chapter of Sigma Phi Delta

A retrieval-augmented LLM service that answers natural-language questions SPD's bylaws. This repository contains:

1. **Indexing script (`index_bylaws.py`)**  
   Reads a raw `bylaws.txt` file, splits it into chunks, computes OpenAI embeddings, and persists them into a Chroma vector store (`chroma_bylaws_db/`).

2. **FastAPI backend (`main.py`)**  
   - On startup, checks for or rebuilds the Chroma store.  
   - Exposes:
     - `GET /ping` (health check)  
     - `POST /query` (accepts `{ "question": "..."} → { "answer": "...", "sources": [...] }`)  

3. **Deployment configurations**  
   - **Render (Python 3 service)**: no Docker required.  
   - **Optional Dockerfile** (for full container control).

4. **Example front-end (optional)**  
   A React/Next.js UI can call `POST /query` to fetch answers. (See separate repo or integrate your own.)

## Features

- **Retrieval-Augmented Generation**: Splits bylaws into 1,000-character chunks, embeds them via OpenAI, and stores in Chroma.  
- **FastAPI Backend**:  
  - Automatically re-indexes on startup if no vector store is found.  
  - CORS-enabled for easy front-end integration.  
  - Returns concise answers referencing specific article/section metadata.  
- **Scalable Deployment**:  
  - Deploy to Render with a few clicks (no Docker required).  
  - Optional Dockerfile for full containerization.
