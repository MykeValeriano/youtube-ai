from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from agents.summary_agent import generate_summary
from agents.notes_agent import generate_notes
from agents.flashcard_agent import generate_flashcards
from agents.quiz_agent import generate_quiz
from fastapi.middleware.cors import CORSMiddleware
import os
from agents.query_agent import query_video
from rag.rag_agent import load_vector_db
from utils.youtube_agent import get_transcript_from_youtube

app = FastAPI()

# Allow all origins for development; restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class YoutubeRequest(BaseModel):
    url: str
    count: int = 5

@app.post("/summary")
async def summary_endpoint(req: YoutubeRequest):
    summary = generate_summary(req.url)
    return {"summary": summary}

@app.post("/notes")
async def notes_endpoint(req: YoutubeRequest):
    notes = generate_notes(req.url)
    return {"notes": notes}

@app.post("/flashcards")
async def flashcards_endpoint(req: YoutubeRequest):
    flashcards = generate_flashcards(req.url, count=req.count, output_file="public/flashcards.json")
    return {"flashcards": flashcards}

@app.post("/quiz")
async def quiz_endpoint(req: YoutubeRequest):
    quiz = generate_quiz(source=req.url, count=req.count, output_file="public/quiz.json")
    return {"quiz": quiz}

@app.get("/health")
async def health():
    return {"status": "ok"}

class QuizRateRequest(BaseModel):
    quiz: list
    user_answers: list

@app.post("/quiz/rate")
async def quiz_rate_endpoint(req: QuizRateRequest):
    from agents.quiz_agent import rate_quiz
    result = rate_quiz(req.quiz, req.user_answers)
    # Save to /public/quiz_score.json
    with open("public/quiz_score.json", "w", encoding="utf-8") as f:
        import json
        json.dump(result, f, ensure_ascii=False, indent=2)
    return result

class QueryRequest(BaseModel):
    url: str
    question: str

@app.post("/query")
async def query_endpoint(req: QueryRequest):
    transcript = get_transcript_from_youtube(req.url)
    vectorstore = load_vector_db(transcript)
    answer = query_video(req.question, vectorstore)
    # Optionally save to /public/query_answer.json
    with open("public/query_answer.json", "w", encoding="utf-8") as f:
        import json
        json.dump({"question": req.question, "answer": answer}, f, ensure_ascii=False, indent=2)
    return {"answer": answer}

# To run: uvicorn api_server:app --reload
