from typing import Union, List, Annotated
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text: str
    questions: List[ChoiceBase]
    
def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()

@app.post("/questions/")
async def create_questions(question: QuestionBase, db: Session = Depends(get_db)):
    
    db_question = models.Questions(question_text = question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    
    for choice in question.choices:
        db_choice = models.Choices(choice_text=choice.choice_text, is_correct = choice.is_correct, question_id=db_question.id)
        db.add(db_choice)

    db.commit()