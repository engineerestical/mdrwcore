# your_app/management/commands/fetch_reviews.py
from django.core.management.base import BaseCommand
from api.utils import fetch_and_insert_reviews

class Command(BaseCommand):
    help = 'Fetch Google reviews and insert into the database'

    def handle(self, *args, **kwargs):
        place_id = 'ChIJmWNJqCWLK4gR2vQE8FZUCAI'  # Replace with your actual Place ID
        api_key = 'AIzaSyDux9WMAVR-ugFSAJKJsFOj7mRAkGmhsTg'  # Replace with your actual Google API Key

        fetch_and_insert_reviews(place_id, api_key)
        self.stdout.write(self.style.SUCCESS('Reviews have been fetched and inserted into the database.'))