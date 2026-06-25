# Books Scraper and FastAPI REST API. Interview Assignment for Cennext.

## Project Overview

This project demonstrates:

1. Web scraping using Python, Requests, and BeautifulSoup.
2. Data collection from the Books to Scrape website.
3. API consumption using the REST Countries API.
4. Data processing and CSV file generation.
5. Development of a REST API using FastAPI.

---

## Features

### Web Scraping

The scraper extracts the following information for each book:

* Title
* Price
* Availability
* Product Link
* Star Rating (1–5)

Data is saved to:

```text
books.csv
```

Additionally, the raw HTML of every product page is saved in:

```text
html_backup/
```

for debugging and backup purposes.

---

### Country Data Integration

Country information is retrieved from the REST Countries API.

Each book is assigned a random:

```text
Publisher_Country
```

The updated dataset is saved to:

```text
books_with_country.csv
```

---

### FastAPI REST API

The project provides the following endpoints:

#### Get All Books

```http
GET /books
```

Returns all books stored in `books_with_country.csv`.

---

#### Get Books by Country

```http
GET /books?country=Canada
```

Returns all books published in the specified country.

---

#### Add a Book

```http
POST /books
```

Adds a new book to the dataset.

Example request body:

```json
{
  "Title": "FastAPI Book",
  "Price": "$19.99",
  "Availability": "In Stock",
  "Product_Link": "https://example.com/book",
  "Star_Rating": 5,
  "Publisher_Country": "Canada"
}
```

---

#### Delete a Book

```http
DELETE /books/{title}
```

Deletes a book by title.

Example:

```http
DELETE /books/FastAPI Book
```

---


---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd books_scraper
```

### Create Virtual Environment

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

or

```bash
pip install requests beautifulsoup4 fastapi uvicorn
```

---

## Running the Scraper

Execute:

```bash
python scraper.py
```

This generates:

```text
books.csv
```

and stores product page backups in:

```text
html_backup/
```

---

## Adding Publisher Countries

Execute:

```bash
python add_countries.py
```

This generates:

```text
books_with_country.csv
```

---

## Running the FastAPI Server

Start the server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

## API Documentation

FastAPI automatically generates interactive documentation.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---


