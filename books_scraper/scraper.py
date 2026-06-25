import os
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "http://books.toscrape.com/"
CATALOGUE_URL = [
    "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
    "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
    "https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html"
]

# Create backup folder
os.makedirs("html_backup", exist_ok=True)

# Convert rating text to number
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

books_data = []

# Scrape first 3 pages
for cat_url in CATALOGUE_URL:
    print(f"Scraping category: {cat_url}")
    response = requests.get(cat_url)
    response.raise_for_status()  # Raise an error for bad responses

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.select("article.product_pod")

    for book in books:
        # Title
        title = book.h3.a["title"]
        # Relative product link
        relative_url = book.h3.a["href"]
        # Absolute product link
        product_url = urljoin(cat_url, relative_url)
        # Product Price
        price = book.select_one("p.price_color").text.strip()
        # Availability
        availability = book.select_one(".availability").text.strip()
        # Rating
        rating_class = book.select_one("p.star-rating")["class"]
        # Default to 0 if not found
        rating = RATING_MAP.get(rating_class[1], 0) 

        # Download product page
        try:
            product_response = requests.get(product_url)
            product_response.raise_for_status()

            product_html = product_response.text
            safe_title = "".join(
                c if c.isalnum() or c in " ._-" else "_" for c in title
            ) [:100]
            backup_file_path = os.path.join("html_backup", f"{safe_title}.html")
            with open(backup_file_path, "w", encoding="utf-8") as f:
                f.write(product_html)
        except Exception as e:
            print(f"Failed to download product page for '{title}': {e}")

        books_data.append({
            "Title": title,
            "Price": price,
            "Availability": availability,
            "Product URL": product_url,
            "Star rating": rating
        })

# Save data to CSV
csv_file = "books_data.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f, 
        fieldnames=[
            "Title", 
            "Price", 
            "Availability", 
            "Product URL", 
            "Star rating"]
    )
    writer.writeheader()
    writer.writerows(books_data)

print(f"\nScraping completed. Saved {len(books_data)} saved to {csv_file}.")
print("HTML backups saved in html_backup/.")