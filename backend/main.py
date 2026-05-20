import os
import time
from google import genai
from google.genai import errors as genai_errors
from pymongo import MongoClient
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

gemini = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY"),
    http_options={"api_version": "v1"},
)

mongo = MongoClient(os.getenv("MONGODB_URI"))
collection = mongo["portfolio"]["resume_chunks"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET", "OPTIONS"], 
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str


def embed_query(text: str) -> list:
    response = gemini.models.embed_content(
        model="gemini-embedding-2",
        contents=text,
    )
    return list(response.embeddings[0].values)


def retrieve_context(query: str, top_k: int = 3) -> str:
    query_embedding = embed_query(query)
    results = collection.aggregate([
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": 20,
                "limit": top_k,
            }
        },
        {
            "$project": {
                "text": 1,
                "_id": 0,
                "score": {"$meta": "vectorSearchScore"},
            }
        }
    ])
    chunks = [doc["text"] for doc in results]
    return "\n\n".join(chunks)


def build_prompt(context: str, question: str) -> str:
    return f"""You are a helpful AI assistant on Avinash Gembali's portfolio website.
Answer questions about Avinash using the context provided below.
Be concise, friendly, and professional.

Important rules:
- If asked about a technology or skill not in his resume (e.g. Spring Boot, AI/ML, cloud, Docker), mention that while it may not be his primary stack, Avinash is a quick learner with strong CS fundamentals and is open to picking up new technologies. Do not say "I don't have that information" for tech-related questions.
- If asked about years of experience, calculate from July 2025 (internship start) to the present — approximately 10-11 months as of May 2026.
- Only say "I don't have that information about Avinash" for truly unrelated personal questions with no context available.
- Never make up facts. Base all answers on the context below.

Context:
{context}

Question: {question}

Answer:"""


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    context = retrieve_context(req.message)
    prompt = build_prompt(context, req.message)

    models = ["gemini-2.5-flash-lite", "gemini-2.5-flash", "gemini-3.1-flash-lite"]

    for model in models:
        for attempt in range(2):
            try:
                response = gemini.models.generate_content(
                    model=model,
                    contents=prompt,
                )
                return ChatResponse(answer=response.text.strip())
            except genai_errors.ClientError as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    break  # quota exhausted for this model, try next
                raise HTTPException(status_code=400, detail="Bad request to AI service.")
            except genai_errors.ServerError:
                if attempt < 1:
                    time.sleep(2)
                else:
                    break  # server overloaded, try next model

    raise HTTPException(status_code=503, detail="AI service temporarily unavailable. Please try again in a moment.")


@app.get("/health")
async def health():
    return {"status": "ok"}
