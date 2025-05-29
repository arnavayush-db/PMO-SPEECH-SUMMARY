import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import logging
from groq import Groq
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SpeechSummarizer:
    def __init__(self, db_path="backend/speeches.db"):
        """Initialize the summarizer with database path and Grok API key."""
        self.base_url = "https://www.pmindia.gov.in/en/tag/pmspeech/"
        self.db_path = db_path
        self.groq_client = Groq(api_key="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")
        self.setup_database()

    def setup_database(self):
        """Set up SQLite database and create speeches table if not exists."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS speeches (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        summary TEXT NOT NULL,
                        image_uri TEXT,
                        url TEXT UNIQUE
                    )
                """)
                conn.commit()
                logger.info("Database initialized successfully.")
        except sqlite3.Error as e:
            logger.error(f"Database setup error: {e}")
            raise

    def fetch_page(self, url):
        """Fetch HTML content from a URL."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None

    def extract_speech_links(self):
        """Extract speech links and image URIs from the main page."""
        html_content = self.fetch_page(self.base_url)
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, 'html.parser')
        news_images = soup.find_all('div', class_='news-image')
        speech_data = []

        for news_image in news_images:
            try:
                link = news_image.find('a')
                img = news_image.find('img')
                if link and img:
                    href = link.get('href')
                    image_uri = img.get('src')
                    title = link.get('title', 'No title')
                    if href and href.startswith('https://www.pmindia.gov.in'):
                        parent = news_image.find_parent()
                        date_span = parent.find('span', class_='date') if parent else None
                        date_str = date_span.get_text(strip=True) if date_span else None
                        formatted_date = None
                        if date_str:
                            try:
                                # Parse date from "MMM DD, YYYY" to "YYYY-MM-DD"
                                date_obj = datetime.strptime(date_str, '%b %d, %Y')
                                formatted_date = date_obj.strftime('%Y-%m-%d')
                            except ValueError as e:
                                logger.warning(f"Failed to parse date '{date_str}': {e}")
                        # Fallback to current date if parsing fails
                        formatted_date = formatted_date or datetime.now().strftime('%Y-%m-%d')
                        speech_data.append({
                            'url': href,
                            'image_uri': image_uri,
                            'title': title,
                            'date': formatted_date
                        })
            except AttributeError as e:
                logger.warning(f"Error parsing news-image div: {e}")
                continue

        logger.info(f"Found {len(speech_data)} speech links.")
        return speech_data

    def extract_speech_content(self, speech_url):
        """Extract paragraph content from a speech page."""
        html_content = self.fetch_page(speech_url)
        if not html_content:
            return None

        soup = BeautifulSoup(html_content, 'html.parser')
        paragraphs = soup.find_all('p')
        content = ' '.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
        return content if content else None

    def generate_summary(self, content):
        """Generate a summary using Grok API."""
        if not content:
            return None

        try:
            prompt = (
                "Summarize the following speech content in 100-200 words, capturing the key points and main themes. "
                "Do not include reasoning, explanations, or intermediate thoughts. Output only the final summary, suitable for public display:\n\n" + content[:10000]
            )
            completion = self.groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a summarization assistant. Provide accurate and concise summaries of speeches."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_completion_tokens=4096,
                top_p=0.95,
                stream=False,
                stop=None
            )
            summary = completion.choices[0].message.content.strip()
            return summary if summary else None
        except Exception as e:
            logger.error(f"Failed to generate summary: {e}")
            return None

    def is_duplicate(self, url):
        """Check if a speech URL already exists in the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM speeches WHERE url = ?", (url,))
                return cursor.fetchone() is not None
        except sqlite3.Error as e:
            logger.error(f"Database duplicate check error: {e}")
            return False

    def save_speech(self, date, title, content, summary, image_uri, url):
        """Save speech data to the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO speeches (date, title, content, summary, image_uri, url)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (date, title, content, summary, image_uri, url))
                conn.commit()
                logger.info(f"Saved speech: {url}")
        except sqlite3.IntegrityError:
            logger.warning(f"Duplicate speech skipped: {url}")
        except sqlite3.Error as e:
            logger.error(f"Database save error: {e}")

    def scrape_and_summarize(self):
        """Main method to scrape speeches and generate summaries."""
        speech_data = self.extract_speech_links()

        for data in speech_data:
            title = data['title']
            current_date = data['date']
            if not current_date:
                logger.warning("No date found for speech link.")
                continue
            if not title:
                logger.warning("No title found for speech link.")
                continue
            url = data['url']
            image_uri = data['image_uri']

            if self.is_duplicate(url):
                logger.info(f"Skipping duplicate speech: {url}")
                continue

            content = self.extract_speech_content(url)
            if not content:
                logger.warning(f"No content found for {url}")
                continue

            summary = self.generate_summary(content)
            # Wait to avoid RateLimitError
            time.sleep(5)
            if not summary:
                logger.warning(f"No summary generated for {url}")
                summary = content[:497] + '...' if len(content) > 500 else content

            self.save_speech(current_date, title, content, summary, image_uri, url)