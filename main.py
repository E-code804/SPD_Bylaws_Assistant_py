# main.py - activate venv: source ~/envs/bylaw-assistant/bin/activate

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 1. Load environment variables (so OPENAI_API_KEY is set)
load_dotenv()

# 2. LangChain imports (updated to use langchain_community where needed)
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOpenAI

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


# 3. Define request/response schemas
class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[str]


# 4. Initialize FastAPI
app = FastAPI(title="Fraternity Bylaw Assistant")

origins = [
    "http://localhost:3000",
    # "https://your-production-domain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow any origin
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, OPTIONS, etc.
    allow_headers=["*"],  # Allow all headers (e.g. Content-Type)
)

# 5. Load or reinstantiate your Chroma vector store
VECTOR_STORE_DIR = "chroma_bylaws_db"
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

# If the directory already exists, Chroma will load from it.
vectorstore = Chroma(
    persist_directory=VECTOR_STORE_DIR, embedding_function=embedding_model
)

# 6. Set up the chat model
chat_model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# 7. Define a prompt template
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "You are a helpful assistant for fraternity bylaws. "
        "Use the context below to answer the question.\n\n"
        "CONTEXT:\n{context}\n\n"
        "QUESTION: {question}\n\n"
        "Answer precisely and quote or reference the relevant Article/Section if possible."
    ),
)

# 8. Create a retriever (e.g., top 3 similar chunks)
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# 9. Build the RetrievalQA chain (passing the prompt via chain_type_kwargs)
qa_chain = RetrievalQA.from_chain_type(
    llm=chat_model,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt_template},
)


# 10. Health check endpoint
@app.get("/ping")
async def ping():
    return {"pong": "pong"}


# 11. Main query endpoint
@app.post("/query", response_model=QueryResponse)
async def query_bylaws(req: QueryRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # Run the RetrievalQA chain
    result = qa_chain({"query": req.question})
    answer_text = result["result"]
    docs = result["source_documents"]

    # Collect simple source identifiers
    sources = []
    for doc in docs:
        # e.g., doc.metadata might have 'source' or 'chunk_id'
        src = doc.metadata.get("source") or doc.metadata.get("chunk_id") or "Unknown"
        sources.append(src)

    return QueryResponse(answer=answer_text, sources=sources)
