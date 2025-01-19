import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import random
import sys
from typing import List, Dict

class AmazonScraper:
    """
    A class to scrape product details from Amazon search pages.
    """

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }
    BASE_URL = "https://www.amazon.com"

    def __init__(self, search_url: str):
        self.search_url = search_url
        self.product_urls: List[str] = []
        self.data_structure: Dict[str, List[str]] = {
            "product_name": [], "product_price": [], "product_rating": [], "review_count": [],
            "stock_status": [], "description": [], "image_link": [], "manufacturer": []
        }

    def fetch_product_urls(self) -> None:
        """Fetches product URLs from the given search URL."""
        print("Fetching product URLs from the search page...")
        try:
            response = requests.get(self.search_url, headers=self.HEADERS)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            product_links = soup.find_all("a", attrs={'class': 'a-link-normal s-no-outline'})
            self.product_urls = [link.get('href') for link in product_links if link.get('href')]
            print(f"Found {len(self.product_urls)} product URLs.")
        except requests.exceptions.RequestException as error:
            print(f"Error fetching product URLs: {error}")

    def scrape_product_info(self, url: str) -> None:
        """Scrapes product information from an individual product page."""
        time.sleep(random.uniform(2, 5))  # Pause to avoid bot detection
        try:
            full_url = url if url.startswith('http') else self.BASE_URL + url
            print(f"Scraping product details from: {full_url}")
            product_response = requests.get(full_url, headers=self.HEADERS)
            product_response.raise_for_status()
            product_soup = BeautifulSoup(product_response.content, "html.parser")

            product_name = product_soup.find("span", attrs={"id": "productTitle"}).text.strip() if product_soup.find("span", attrs={"id": "productTitle"}) else "No Product Name Found"
            price = product_soup.find("span", attrs={"id": "priceblock_ourprice"}) or product_soup.find("span", attrs={"id": "priceblock_dealprice"}) or product_soup.find("span", attrs={"class": "a-price-whole"})
            product_price = price.text.strip() if price else "Price Unavailable"
            product_rating = product_soup.find("span", attrs={"class": "a-icon-alt"}).text.strip() if product_soup.find("span", attrs={"class": "a-icon-alt"}) else "No Rating Found"
            review_count = product_soup.find("span", attrs={"id": "acrCustomerReviewText"}).text.strip() if product_soup.find("span", attrs={"id": "acrCustomerReviewText"}) else "No Reviews Found"
            availability = product_soup.find("div", attrs={"id": "availability"})
            stock_status = availability.find("span").text.strip() if availability else "Stock Status Unknown"
            description = product_soup.find("div", attrs={"id": "productDescription"})
            description_text = description.get_text(separator=" ", strip=True) if description else "No Description Available"
            image_tag = product_soup.find("img", attrs={"id": "landingImage"})
            image_link = image_tag['src'] if image_tag else "No Image Available"
            brand = product_soup.find("a", attrs={"id": "bylineInfo"})
            manufacturer = brand.text.strip() if brand else "No Brand Information"

            self.data_structure["product_name"].append(product_name)
            self.data_structure["product_price"].append(product_price)
            self.data_structure["product_rating"].append(product_rating)
            self.data_structure["review_count"].append(review_count)
            self.data_structure["stock_status"].append(stock_status)
            self.data_structure["description"].append(description_text)
            self.data_structure["image_link"].append(image_link)
            self.data_structure["manufacturer"].append(manufacturer)

        except requests.exceptions.RequestException as error:
            print(f"Error fetching product info for {url}: {error}")
            for field in self.data_structure.keys():
                self.data_structure[field].append("Error")

    def scrape_all_products(self) -> None:
        """Scrapes information for all product URLs fetched from the search page."""
        if not self.product_urls:
            print("No product URLs to scrape. Please check the search URL.")
            return

        print(f"Starting to scrape {len(self.product_urls)} products...")
        for idx, url in enumerate(self.product_urls, start=1):
            print(f"Processing product {idx}/{len(self.product_urls)}")
            self.scrape_product_info(url)

    def save_to_csv(self, filename: str = "amazon_scraped_data.csv") -> None:
        """Saves the scraped data to a CSV file."""
        print(f"Saving data to {filename}...")
        results_df = pd.DataFrame.from_dict(self.data_structure)
        results_df.replace('', np.nan, inplace=True)
        results_df.dropna(subset=['product_name'], inplace=True)
        results_df.to_csv(filename, index=False)
        print(f"Data saved to '{filename}'.")

if __name__ == "__main__":
    user_input_url = input("Enter the Amazon search page URL to scrape products from: ")

    if not user_input_url.startswith("https://"):
        print("Invalid URL. Ensure it starts with 'https://'. Exiting.")
        sys.exit(1)

    scraper = AmazonScraper(user_input_url)
    scraper.fetch_product_urls()
    scraper.scrape_all_products()
    scraper.save_to_csv()
