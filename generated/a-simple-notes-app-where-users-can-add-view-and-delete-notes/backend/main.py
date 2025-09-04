# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

origins = ["*"] #For production, replace with specific origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

notes = []

class Note(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(..., min_length=3, max_length=50)
    content: str = Field(..., min_length=10)

@app.get("/")
async def root():
    return {"message": "Welcome to the Simple Notes API"}

@app.post("/notes/", response_model=Note, status_code=201)
async def create_note(note: Note):
    if any(n.id == note.id for n in notes):
        raise HTTPException(status_code=409, detail="Note with this ID already exists")
    notes.append(note)
    return note

@app.get("/notes/", response_model=List[Note])
async def get_notes():
    return notes

@app.delete("/notes/{note_id}", status_code=204)
async def delete_note(note_id: int):
    for i, note in enumerate(notes):
        if note.id == note_id:
            del notes[i]
            return
    raise HTTPException(status_code=404, detail="Note not found")