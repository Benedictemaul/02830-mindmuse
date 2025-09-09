from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
# It automatically looks for the OPENAI_API_KEY in your environment
client = openai.OpenAI()

app = FastAPI()

# Allow locally hosted api to connect
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
# --- UPDATED MODEL ---
# Journal entry model now includes an optional summary field
class JournalEntry(BaseModel):
    title: str
    content: str
    summary: Optional[str] = None # The summary will be generated

# Fake in-memory DB (resets if you restart)
journal_db: List[JournalEntry] = []

@app.get("/")
def home():
    return {"message": "Welcome to Journal API"}

# --- UPDATED ENDPOINT ---
# Changed to 'async def' to handle the API call without blocking
@app.post("/journal/")
async def add_entry(entry: JournalEntry):

    # 1. Create a prompt for the AI
    prompt_text = f"Make the writer of this entry feel awful in one precise and evil sentence. Be harsh and unfair. Break them down psychologically.: \"{entry.content}\""
    
    try:
        # 2. Call the OpenAI API to get the summary
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # A fast and cost-effective model
            messages=[
                {"role": "system", "content": "You are an evil assistant that makes people feel bad."},
                {"role": "user", "content": prompt_text}
            ],
            max_tokens=60 # Limit the length of the summary
        )
        
        # 3. Extract the summary text from the response
        summary_text = response.choices[0].message.content.strip()
        entry.summary = summary_text
        
    except Exception as e:
        # If the API call fails, we'll just store a default message
        print(f"Error calling OpenAI API: {e}")
        entry.summary = "Could not generate summary."

    # 4. Add the entry (now with summary) to our database
    journal_db.append(entry)
    return {"message": "Entry added with summary", "entry": entry}

@app.get("/journal/")
def get_entries():
    return {"entries": journal_db}