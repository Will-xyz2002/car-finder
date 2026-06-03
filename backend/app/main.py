from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import listings

app = FastAPI(title="Car Finder CA API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(listings.router, prefix="/listings", tags=["listings"])


@app.get("/health")
def health_check():
    return {"status": "ok"}
