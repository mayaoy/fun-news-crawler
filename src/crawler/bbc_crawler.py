import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, List, Optional
import time
import random

class BBCNewsCrawler:
    def __init__(self):
        self.base_url = "https://www.bbc.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

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

    def parse_article(self, url: str) -> Optional[Dict]:
        """
        Parse a single article page
        """
        html_content = self.fetch_page(url)
        if not html_content:
            return None

        soup = BeautifulSoup(html_content, 'lxml')
        
        try:
            # Get article title
            title = soup.find('h1').text.strip()
            
            # Get article content
            article_body = soup.find('article')
            if not article_body:
                return None
                
            content_paragraphs = article_body.find_all('p')
            content = '\n'.join([p.text.strip() for p in content_paragraphs if p.text.strip()])
            
            # Get publication date
            time_element = soup.find('time')
            published_date = datetime.now().isoformat() if not time_element else time_element.get('datetime')
            
            # Determine category from URL
            category = "World"  # default category
            for cat, cat_url in self.get_category_urls().items():
                if cat.lower() in url.lower():
                    category = cat
                    break

            return {
                'title': title,
                'url': url,
                'content': content,
                'category': category,
                'published_date': published_date
            }
        except Exception as e:
            print(f"Error parsing article {url}: {e}")
            return None

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

    def crawl_category(self, category: str) -> List[Dict]:
        """
        Crawl all articles from a specific category
        """
        category_urls = self.get_category_urls()
        if category not in category_urls:
            print(f"Invalid category: {category}")
            return []

        article_urls = self.get_article_urls(category_urls[category])
        articles = []

        for url in article_urls:
            article_data = self.parse_article(url)
            if article_data:
                articles.append(article_data)
            time.sleep(random.uniform(1, 3))  # Random delay between requests

        return articles

    def crawl_all_categories(self) -> List[Dict]:
        """
        Crawl articles from all categories
        """
        all_articles = []
        for category in self.get_category_urls().keys():
            print(f"Crawling {category} category...")
            articles = self.crawl_category(category)
            all_articles.extend(articles)
        return all_articles 