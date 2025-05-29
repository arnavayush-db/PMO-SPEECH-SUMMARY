from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from typing import List
from models import Speech
from scrap_speeches import SpeechSummarizer
import uvicorn

app = FastAPI()

# Enable CORS for Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
def get_db():
    conn = sqlite3.connect("backend/speeches.db")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

@app.on_event("startup")
def run_scraper():
    scraper = SpeechSummarizer(db_path="backend/speeches.db")
    scraper.scrape_and_summarize()
    print("Speech scraping completed on startup.")

@app.get("/api/speeches", response_model=List[Speech])
async def get_speeches():
    try:
        conn = sqlite3.connect("backend/speeches.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM speeches ORDER BY date DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
