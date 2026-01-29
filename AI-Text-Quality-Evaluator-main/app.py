from fastapi import FastAPI
from pydantic import BaseModel
from evaluator import evaluate_text

app = FastAPI(title="AI Text Quality Evaluator")


class TextRequest(BaseModel):
    text: str


@app.post("/evaluate")
def evaluate(req: TextRequest):
    return evaluate_text(req.text)
