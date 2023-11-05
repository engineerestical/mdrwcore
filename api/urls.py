from django.urls import path
from . import views
from .views import ReviewList

urlpatterns = [
    path('reviews/', ReviewList.as_view(), name='review-list'),
    path('get-google-reviews/', views.get_google_reviews, name='get_google_reviews'),
]