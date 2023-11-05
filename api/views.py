from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Review
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Review
from .serializers import ReviewSerializer
from .utils import fetch_and_insert_reviews, translate_to_english
from .serializers import ReviewSerializer
# views.py
import json
import requests
from django.http import JsonResponse
from .models import Review
from datetime import datetime


import requests
from django.http import JsonResponse
from .models import Review

def get_google_reviews(request):
    place_id = "ChIJmWNJqCWLK4gR2vQE8FZUCAI"
    api_key = "AIzaSyDux9WMAVR-ugFSAJKJsFOj7mRAkGmhsTg"  # Replace with your Google API Key

    # Make the API call to get place details
    place_details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,rating,reviews",
        "key": api_key,
        "sort": "newest",
    }
    response = requests.get(place_details_url, params=params)
    place_details = response.json()

    if "error_message" in place_details:
        return JsonResponse({"error": place_details["error_message"]}, status=400)

    # Save place details in your Django model
    place_name = place_details["result"]["name"]
    place_rating = place_details["result"]["rating"]
    reviews = place_details["result"].get("reviews", [])

    # Filter the 5-star reviews
    five_star_reviews = [review_data for review_data in reviews if review_data["rating"] == 5]

    # Retrieve the last 5 five-star reviews
    last_five_five_star_reviews = five_star_reviews[-5:]

    # Save the place details in your Django model
    review_objects = []
    for review_data in last_five_five_star_reviews:
        # Check if a review from the same author already exists
        existing_review = Review.objects.filter(author_name=review_data["author_name"]).first()

        if existing_review is None:
            review_date = datetime.fromtimestamp(review_data["time"])
            review = Review(
                author_name=review_data["author_name"],
                rating=review_data["rating"],
                text=translate_to_english(review_data["text"]),
                profile_photo_url=review_data.get("profile_photo_url", ""), 
                review_date=review_date,
            )
            review_objects.append(review)

    # Bulk insert only the new reviews (those without an existing author name)
    Review.objects.bulk_create(review_objects)

    return JsonResponse({"message": "Last 5 five-star reviews saved successfully."})



class ReviewList(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class UpdateReviews(APIView):
    def post(self, request):
        place_id = 'ChIJmWNJqCWLK4gR2vQE8FZUCAI'  # Get the place ID from the request
        api_key = 'AIzaSyDux9WMAVR-ugFSAJKJsFOj7mRAkGmhsTg'  # Replace with your Google API key

        reviews = fetch_and_insert_reviews(place_id, api_key)
        
        for review_data in reviews:
            review_text = review_data.get('text', '')
            if review_data.get('language') != 'en':
                review_text = translate_to_english(review_text)

            # Create or update a review record in your database
            Review.objects.update_or_create(
                place_id=place_id,
                text=review_text,
                rating=review_data.get('rating', 0),
                author_name=review_data.get('author_name', ''),
                review_date=review_date,
                # Add other fields as needed
            )

        return JsonResponse({'message': 'Reviews updated successfully'})

