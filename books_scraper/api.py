from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import csv

app = FastAPI()
CSV_FILE = "books_with_countries.csv"

class Book(BaseModel):
    Title: str
    Price: str
    Availability: str
    Product_URL: str
    Star_rating: int
    Publisher_Country: str  

def read_books_from_csv():
    books = []

    if not os.path.exists(CSV_FILE):
        return books
    
    with open(CSV_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            books.append(row)
    return books

def save_books_to_csv(books):
    if not books:
        return
    
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=books[0].keys())
        writer.writeheader()
        writer.writerows(books)

@app.get("/books")
def get_books(country: str | None = None):
    books = read_books_from_csv()
    if country:
        books = [
            book 
            for book in books 
            if book["Publisher_Country"].lower() == country.lower()
        ]
    return books

@app.post("/books")
def add_book(book: Book):
    books = read_books_from_csv()
    books.append({
        "Title": book.Title,
        "Price": book.Price,
        "Availability": book.Availability,
        "Product_URL": book.Product_URL,
        "Star_rating": book.Star_rating,
        "Publisher_Country": book.Publisher_Country
    })
    save_books_to_csv(books)
    return {"message": "Book added successfully."}

@app.delete("/books/{title}")
def delete_book(title: str):
    books = read_books_from_csv()
    books = [book for book in books if book["Title"].lower() != title.lower()]
    if len(books) == 0:
        raise HTTPException(status_code=404, detail="Book not found.")
    save_books_to_csv(books)
    return {"message": "Book deleted successfully."}