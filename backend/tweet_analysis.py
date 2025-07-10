from bluesky_fetcher import BlueskyFetcher
from add_locations import update_post_locations_on_list
from data_manager import DataManager
from predict_disaster import DisasterPredictor


def runscripts():
    predictor = DisasterPredictor()

    print("Starting tweet analysis pipeline")
    data_manager = DataManager()
    fetcher = BlueskyFetcher(data_manager)

    print("Fetching posts from Bluesky")
    posts = fetcher.fetch_posts()
    print(f"Fetched {len(posts)} posts from Bluesky.")

    posts = update_post_locations_on_list(posts)

    posts = predictor.predict_disasters_on_list(posts)

    data_manager.add_bluesky_posts(posts)

    print("Tweet analysis pipeline complete.")
