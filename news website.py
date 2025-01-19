import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

class CNNNewsScraper:
    """
    A class to scrape news articles from CNN's website.
    """

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }
    BASE_URL = "https://www.cnn.com"

    def __init__(self, news_url: str):
        self.news_url = news_url
        self.article_urls = []
        self.data = {
            "title": [],
            "date": [],
            "summary": [],
            "content": [],
            "article_url": []
        }

    def fetch_article_urls(self):
        """Fetches article URLs from the given CNN news page."""
        print(f"Fetching article URLs from {self.news_url}...")
        try:
            response = requests.get(self.news_url, headers=self.HEADERS)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            # Fetch all article links (Adjust selectors based on CNN's structure)
            article_links = soup.find_all("a", attrs={"href": True})
            self.article_urls = [
                self.BASE_URL + link.get("href") if link.get("href").startswith("/") else link.get("href")
                for link in article_links
                if "/articles/" in link.get("href") or "cnn.com" in link.get("href")
            ]
            print(f"Found {len(self.article_urls)} article URLs.")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching article URLs: {e}")

    def scrape_article_info(self, url):
        """Scrapes article details from a single CNN article page."""
        time.sleep(random.uniform(1, 3))  # Pause to avoid bot detection
        try:
            print(f"Scraping article: {url}")
            response = requests.get(url, headers=self.HEADERS)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract data from the article page
            title = soup.find("h1").text.strip() if soup.find("h1") else "No Title Found"
            date = soup.find("meta", attrs={"name": "pubdate"})
            date = date["content"] if date else "No Date Found"
            summary = soup.find("meta", attrs={"name": "description"})
            summary = summary["content"] if summary else "No Summary Available"
            content_paragraphs = soup.find_all("div", attrs={"class": "zn-body__paragraph"})
            content = " ".join(p.text.strip() for p in content_paragraphs)

            # Append data to the dictionary
            self.data["title"].append(title)
            self.data["date"].append(date)
            self.data["summary"].append(summary)
            self.data["content"].append(content)
            self.data["article_url"].append(url)

        except requests.exceptions.RequestException as e:
            print(f"Error scraping article: {e}")
            for key in self.data.keys():
                self.data[key].append("Error")

    def scrape_all_articles(self):
        """Scrapes all articles found on the CNN page."""
        if not self.article_urls:
            print("No articles found to scrape.")
            return

        print(f"Starting to scrape {len(self.article_urls)} articles...")
        for idx, url in enumerate(self.article_urls, start=1):
            print(f"Scraping article {idx}/{len(self.article_urls)}")
            self.scrape_article_info(url)

    def save_to_csv(self, filename="cnn_news.csv"):
        """Saves scraped data to a CSV file."""
        print(f"Saving data to {filename}...")
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

if __name__ == "__main__":
    news_url = input("Enter the CNN news page URL to scrape: ")
    scraper = CNNNewsScraper(news_url)
    scraper.fetch_article_urls()
    scraper.scrape_all_articles()
    scraper.save_to_csv()
