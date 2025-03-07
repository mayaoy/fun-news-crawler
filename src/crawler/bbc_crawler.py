import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, List, Optional
import time
import random
from database.db_operations import NewsDatabase

class BBCNewsCrawler:
    def __init__(self):
        self.base_url = "https://www.bbc.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.db = NewsDatabase()

    def get_category_urls(self) -> Dict[str, str]:
        """
        Returns a dictionary of category names and their URLs.
        Based on BBC's main navigation and news sub-navigation structure.
        """
        # Main categories
        main_categories = {
            "Home": f"{self.base_url}",
            "News": f"{self.base_url}/news",
            "Sport": f"{self.base_url}/sport",
            "Business": f"{self.base_url}/business",
            "Innovation": f"{self.base_url}/innovation",
            "Culture": f"{self.base_url}/culture",
            "Travel": f"{self.base_url}/travel",
            "Earth": f"{self.base_url}/future-planet"
        }

        # News sub-categories
        news_categories = {
            "Israel-Gaza War": f"{self.base_url}/news/topics/c2vdnvdg6xxt",
            "War in Ukraine": f"{self.base_url}/news/war-in-ukraine",
            "US & Canada": f"{self.base_url}/news/us-canada",
            "UK": f"{self.base_url}/news/uk",
            "Africa": f"{self.base_url}/news/world/africa",
            "Asia": f"{self.base_url}/news/world/asia",
            "Australia": f"{self.base_url}/news/world/australia",
            "Europe": f"{self.base_url}/news/world/europe",
            "Latin America": f"{self.base_url}/news/world/latin_america",
            "Middle East": f"{self.base_url}/news/world/middle_east",
            "BBC InDepth": f"{self.base_url}/news/bbcindepth",
            "BBC Verify": f"{self.base_url}/news/bbcverify"
        }

        # Combine all categories
        return {**main_categories, **news_categories}

    def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch the HTML content of a page
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def parse_and_save_article(self, url: str, category: str) -> bool:
        """
        Parse a single article page and save it to database immediately
        Returns True if article was successfully saved, False otherwise
        """
        # Check if URL already exists in database
        if self.db.url_exists(url):
            print(f"Skipping already crawled article: {url}")
            return False

        html_content = self.fetch_page(url)
        if not html_content:
            return False

        soup = BeautifulSoup(html_content, 'lxml')
        
        try:
            # Get article title
            title = soup.find('h1')
            if not title:
                return False
            title = title.text.strip()
            
            # Get article content
            article_body = soup.find('article')
            if not article_body:
                return False
                
            content_paragraphs = article_body.find_all('p')
            content = '\n'.join([p.text.strip() for p in content_paragraphs if p.text.strip()])
            
            # Get publication date
            time_element = soup.find('time')
            published_date = datetime.now().isoformat() if not time_element else time_element.get('datetime')

            # Create article data
            article_data = {
                'title': title,
                'url': url,
                'content': content,
                'category': category,
                'published_date': published_date
            }

            # Save to database immediately
            return self.db.save_news(article_data)

        except Exception as e:
            print(f"Error parsing article {url}: {e}")
            return False

    def get_article_urls(self, category_url: str) -> List[str]:
        """
        Get all article URLs from a category page
        """
        html_content = self.fetch_page(category_url)
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, 'lxml')
        articles = []
        
        # Find all article links
        for link in soup.find_all('a', href=True):
            href = link['href']
            if '/news/' in href and href.count('/') >= 3:  # Usually article URLs have at least 3 slashes
                if not href.startswith('http'):
                    href = f"https://www.bbc.com{href}"
                articles.append(href)

        return list(set(articles))  # Remove duplicates

    def crawl_category(self, category: str) -> Dict[str, int]:
        """
        Crawl all articles from a specific category
        Returns statistics about the crawl
        """
        category_urls = self.get_category_urls()
        if category not in category_urls:
            print(f"Invalid category: {category}")
            return {"total": 0, "saved": 0, "skipped": 0}

        article_urls = self.get_article_urls(category_urls[category])
        saved_count = 0
        skipped_count = 0

        for url in article_urls:
            if self.parse_and_save_article(url, category):
                saved_count += 1
                print(f"Saved article: {url}")
            else:
                skipped_count += 1
            time.sleep(random.uniform(1, 3))  # Random delay between requests

        stats = {
            "total": len(article_urls),
            "saved": saved_count,
            "skipped": skipped_count
        }
        
        print(f"Category {category}: Found {stats['total']} articles, "
              f"Saved {stats['saved']} new articles, Skipped {stats['skipped']} articles")
        
        return stats 