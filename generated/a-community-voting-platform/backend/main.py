from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="A Community Voting Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to A Community Voting Platform API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/items")
async def get_items():
    return {"items": ["Item 1", "Item 2", "Item 3"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
