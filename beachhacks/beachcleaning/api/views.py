import os
from rest_framework import generics
from .serializers import Post
from .models import Post

from rest_framework.response import Response

from dotenv import load_dotenv
load_dotenv()

from googleplaces import GooglePlaces, types, lang

API_KEY = os.environ['API_KEY']
google_places = GooglePlaces(API_KEY)


class BeachesView(generics.CreateAPIView):
    def post(self, request):
        location = request.data.get('location')

        query_result = google_places.nearby_search(
            location=location,
            keyword='beach',
            rankby='distance',
            types=[types.TYPE_NATURAL_FEATURE])

        beaches = []

        for place in query_result.places:
            beach = {}

            beach['name'] = place.name
            beach['place_id'] = place.place_id

            place.get_details()
            beach['address'] = place.formatted_address
            photos = []

            for photo in place.photos:
                photo.get(maxheight=500, maxwidth=500)
                photos.append(photo.url)

            beach['photos'] = photos

            beaches.append(beach)


        return Response(beaches)
