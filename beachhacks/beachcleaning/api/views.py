import os
import cloudinary
import cloudinary.uploader
from rest_framework import generics
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import status
from rest_framework_jwt.settings import api_settings
from .models import Post

from rest_framework.response import Response
from .serializers import PostSerializer, TokenSerializer, UserSerializer

from dotenv import load_dotenv
load_dotenv()

from googleplaces import GooglePlaces, types, lang

API_KEY = os.environ['API_KEY']
google_places = GooglePlaces(API_KEY)

# JWT Settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class BeachesView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny, )

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


class BeachView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.AllowAny, )

    def get(self, request, id=None):
        try:
            posts = Post.objects.all().filter(beach_id=id)

            return Response(PostSerializer(posts, many=True).data)
        except Post.DoesNotExist:
            data = {}
            data['posts'] = None
            return Response(data)


class PostView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        caption = request.data.get("caption")
        beach_id = request.data.get("beach_id")
        username = request.user.username
        author = self.request.user

        result = cloudinary.uploader.upload(
            "https://residentialwastesystems.com/wp-content/uploads/2017/09/international-coastal-cleanup-day.jpg"
        )
        image = result['secure_url']
        imageId = result['public_id']
        post = Post.objects.create(caption=caption,
                                   image=image,
                                   imageId=imageId,
                                   beach_id=beach_id,
                                   author=author,
                                   author_username=username)
        return Response(data=PostSerializer(post).data,
                        status=status.HTTP_201_CREATED)


class LoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = TokenSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Save user ID in session
            # Also generate and send a token for future calls to the api
            login(request, user)
            serializer = TokenSerializer(
                data={'token': jwt_encode_handler(jwt_payload_handler(user))})
            serializer.is_valid()
            return Response(serializer.data)
        else:
            return Response(data={'message': 'Incorrect username or password'},
                            status=status.HTTP_404_NOT_FOUND)


class LogoutView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        logout(request)
        return Response(data={'message': 'Logged out'})


class RegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        if not username and not password and not email:
            return Response(
                data={'message': 'Username, password and email are required'},
                status=status.HTTP_400_BAD_REQUEST)
        new_user = User.objects.create_user(username=username,
                                            password=password,
                                            email=email)
        return Response(data=UserSerializer(new_user).data,
                        status=status.HTTP_201_CREATED)
