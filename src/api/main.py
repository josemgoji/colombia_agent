from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from src.agent.wiki_agent import WikiAgent

app = FastAPI()
agent = WikiAgent()

class Question(BaseModel):
    question: str

@app.post("/ask")
def ask(question: Question = Body(...)):
    if not question.question.strip():
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacia.")

    try:
        answer = agent.ask(question.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}

