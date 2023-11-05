from django.db import models
from datetime import datetime

class Review(models.Model):
    author_name = models.CharField(max_length=255)
    rating = models.IntegerField()
    text = models.TextField()
    profile_photo_url = models.URLField(default="default_photo_url_here")  # Define your default URL
    review_date = models.DateTimeField(default=datetime(2023, 1, 1))
    def __str__(self):
        return self.author_name