from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
#import googleapiclient

app = FastAPI()

# Allow locally hosted api to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        #"http://127.0.0.1:8000",
        "*"
          # Allows requests from your local machine
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Journal entry model
class JournalEntry(BaseModel):
    title: str
    content: str

# Fake in-memory DB (resets if you restart)
journal_db: List[JournalEntry] = []

@app.get("/")
def home():
    return {"message": "Welcome to Journal API"}

@app.post("/journal/")
def add_entry(entry: JournalEntry):
    journal_db.append(entry)
    return {"message": "Entry added", "entry": entry}

@app.get("/journal/")
def get_entries():
    return {"entries": journal_db}

