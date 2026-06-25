import csv
import random
import requests

import requests
response = requests.get(
  'https://api.restcountries.com/countries/v5',
  headers={'Authorization': 'Bearer rc_live_1f64fe2bc2a74e9883cefae4f96d0c6f'}
)
response.raise_for_status()  # Raise an error for bad responses

countries_data = response.json()
countries = []

objects = countries_data["data"]["objects"]

for country in objects:
    country_name = country["names"]["common"]
    countries.append(country_name)

print(f"Retrieved {len(countries)} countries.")

books = []
with open("books_data.csv", "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        row["Publisher Country"] = random.choice(countries)
        books.append(row)

fieldnames = [
    "Title", 
    "Price", 
    "Availability", 
    "Product URL", 
    "Star rating",
    "Publisher Country"
]

with open("books_with_countries.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(books)

print(f"Saved {len(books)} books with publisher countries to 'books_with_countries.csv'.")