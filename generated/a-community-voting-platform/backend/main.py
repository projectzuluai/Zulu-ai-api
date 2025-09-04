# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI()

origins = ["*"] #Production: Replace with specific origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Vote(BaseModel):
    option: str = Field(..., min_length=1, max_length=100)

votes = {}

@app.get("/")
async def root():
    return {"message": "Welcome to the Community Voting Platform!"}

@app.get("/votes")
async def get_votes():
    return votes

@app.post("/votes")
async def post_vote(vote: Vote):
    if vote.option not in votes:
        votes[vote.option] = 0
    votes[vote.option] += 1
    return {"message": f"Vote for '{vote.option}' recorded successfully."}

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {"detail": exc.detail, "status_code": exc.status_code}