from atproto import Client
from data_manager import DataManager
import time
from datetime import datetime, timedelta
import config
import re
import emoji
from models import BlueskyPost

SEARCH_TERMS = ["tornado", "hurricane", "earthquake", "flood", "wildfire", "blizzard", "haze", "meteor"]
MAX_DOWNLOADS = 10

def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = emoji.replace_emoji(text, replace='')
    return text.strip()

class BlueskyFetcher:
    def __init__(self, data_manager: DataManager):
        print("Logging into Bluesky API")
        self.client = Client()
        self.login()
        self.data_manager = data_manager

    def login(self):
        try:

            self.client.login(config.USERNAME, config.PASSWORD)
            print("Bluesky login successful!")
        except Exception as e:
            print(f"Bluesky login failed: {e}")
            exit()

    def search_bluesky_posts(self, cursor, query):
        try:
            response = self.client.app.bsky.feed.search_posts({
                'q': query,
                'lang': 'en',
                'limit': 10, #
                'cursor': cursor
            })

            if not response or not response.posts:
                print(f"No results found for {query}")
                return [], None

            print(f"Found {len(response.posts)} posts for {query}")
            results = []

            for post in response.posts:
                cleaned_text = clean_text(post.record.text)

                formatted_post = BlueskyPost(
                    user=post.author.handle,
                    text=cleaned_text,
                    query=query,
                    timestamp=(datetime.fromisoformat(post.record.created_at.replace("Z", "+00:00")) - timedelta(hours=5)).isoformat(),
                    location=[],
                    latitude=None,
                    longitude=None
                )

                if not self.data_manager.is_duplicate(formatted_post):
                    results.append(formatted_post)

            next_cursor = response.cursor if hasattr(response, 'cursor') else None
            return results, next_cursor

        except Exception as e:
            print(f"Error searching posts: {e}")
            return [], None

    def fetch_posts(self):
        self.data_manager.delete_old_posts()
        all_posts = []
        for query in SEARCH_TERMS:
            downloaded_count = 0
            cursor = None
            while downloaded_count < MAX_DOWNLOADS:
                print(f"Searching posts for {query} at index {downloaded_count}")
                posts, cursor = self.search_bluesky_posts(cursor, query)
                if not posts:
                    break
                all_posts.extend(posts)     ##
                downloaded_count += len(posts)
                if downloaded_count >= MAX_DOWNLOADS or not cursor:
                    break
        return all_posts
