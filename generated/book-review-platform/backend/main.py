# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(title="Book Review Platform")

origins = ["*"] #For development only; restrict in production

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Book(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(..., min_length=1, max_length=100)
    author: str = Field(..., min_length=1, max_length=100)
    isbn: str = Field(..., min_length=10, max_length=13)
    review: Optional[str] = Field(None, max_length=500)

book_data = {
    1: {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "isbn": "978-0618002255", "review": "A classic fantasy epic"},
    2: {"title": "To Kill a Mockingbird", "author": "Harper Lee", "isbn": "978-0061120084", "review": "A powerful story of justice and injustice"}
}


@app.get("/")
async def root():
    return {"message": "Welcome to the Book Review Platform!"}

@app.get("/books/", response_model=List[Book])
async def get_books():
    return [Book(**book) for book in book_data.values()]

@app.post("/books/", response_model=Book, status_code=201)
async def create_book(book: Book):
    if book.id in book_data:
        raise HTTPException(status_code=409, detail="Book with this ID already exists")
    book_data[book.id] = book.model_dump()
    return book

@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    book = book_data.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return Book(**book)

@app.delete("/books/{book_id}", status_code=204)
async def delete_book(book_id: int):
    if book_id not in book_data:
        raise HTTPException(status_code=404, detail="Book not found")
    del book_data[book_id]

@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, updated_book: Book):
    if book_id != updated_book.id:
        raise HTTPException(status_code=400, detail="Book ID mismatch")
    if book_id not in book_data:
        raise HTTPException(status_code=404, detail="Book not found")
    book_data[book_id] = updated_book.model_dump()
    return updated_book