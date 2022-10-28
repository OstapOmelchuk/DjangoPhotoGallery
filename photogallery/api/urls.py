from django.urls import path, include
from .views import AlbumViewSet, PhotoViewSet, ImportPhotosFromAPI, ImportPhotosFromJSONView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'album', AlbumViewSet, basename='album')


urlpatterns = [
    path('', include(router.urls)),
    path('photos/', PhotoViewSet.as_view()),    # create photo
    path('photos/<int:photo_id>/', PhotoViewSet.as_view()),  # get/delete/update a photo by id
    path('album/<int:album_id>/photos/', PhotoViewSet.as_view()),   # get photos of album
    path('import-api-photo/', ImportPhotosFromAPI.as_view()),   # import photos from external API
    path('import-json-file-photo/', ImportPhotosFromJSONView.as_view()),   # import photos external JSON file
]
