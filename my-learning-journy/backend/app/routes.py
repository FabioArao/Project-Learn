import traceback
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.scrape import scrape_books_from_page

router = APIRouter()

class BookRequest(BaseModel):
    subject: str
    url: str

@router.post("/api/books")
async def get_books(request: BookRequest):
    try:
        # Scrape book information from the provided URL
        top_books = scrape_books_from_page(request.url)
        
        if top_books.empty:
            raise HTTPException(status_code=404, detail="No books found.")
        
        # Return the top 50 books
        return {"books": top_books.to_dict(orient='records')}
    except Exception as e:
        print(f"An error occurred: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))
