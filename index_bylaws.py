# index_bylaws.py
from dotenv import load_dotenv
from pathlib import Path
from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document

load_dotenv()

# 1. Load the raw text file
BYLAWS_PATH = Path("bylaws_joined.txt")
loader = TextLoader(str(BYLAWS_PATH), encoding="utf-8")
raw_docs: List[Document] = loader.load()

# 2. Split into chunks—one chunk per “Article/Section”
#    You may customize the splitter to break at headings like “===Article I===”
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    separators=["===Article", "===Section", "\n\n", "\n"],
)
chunks = splitter.split_documents(raw_docs)

# 3. Compute embeddings
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",  # or whichever OpenAI embeddings model you prefer
    chunk_size=50,
)

# 4. Create or load a Chroma vector store on disk
VECTOR_STORE_DIR = "chroma_bylaws_db"
vectorstore = Chroma.from_documents(
    documents=chunks, embedding=embeddings, persist_directory=VECTOR_STORE_DIR
)

# Persist to disk so we don’t re‐embed every time
vectorstore.persist()
print(f"Indexed {len(chunks)} chunks. Vector store saved to: {VECTOR_STORE_DIR}")
