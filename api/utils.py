import googlemaps
from googletrans import Translator
from .models import Review


def fetch_and_insert_reviews(place_id, api_key):
    gmaps = googlemaps.Client(key=api_key)
    place = gmaps.place(place_id)

    if 'reviews' in place:
        reviews_data = place['reviews']
        for review_data in reviews_data:
            Review.objects.create(
                place_id=place_id,
                text=review_data.get('text', ''),
                rating=review_data.get('rating', 0),
                author_name=review_data.get('author_name', '')
                # Add other fields as needed
            )
def translate_to_english(text):
    translator = Translator()
    translation = translator.translate(text, src='auto', dest='en')
    return translation.text

