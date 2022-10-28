import json
import os

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
import requests

from galleryapp.models import Album, Photo
from galleryapp.utils import get_image_size, get_image_color
from .serializers import AlbumSerializer, PhotoSerializer
from .utils import createPhotosFromJSONData


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    # @action(methods=["DELETE"], detail=False)
    def destroy(self, request, *args, **kwargs):
        album_id = kwargs.get("pk", None)
        if not album_id:
            return Response({"error": "Method DELETE is not allowed"})
        album = Album.objects.get(id=album_id)
        album_photos = Photo.objects.filter(album__id=album_id)

        for photo in album_photos:
            os.remove(photo.url + photo.title + photo.extension)
        album.delete()
        return Response({"result": "Album is deleted."})


class PhotoViewSet(APIView):
    def get(self, request, *args, **kwargs):
        album_id = kwargs.get("album_id", None)
        photo_id = kwargs.get("photo_id", None)
        if album_id:
            photos = Photo.objects.filter(album__id=album_id)
        elif photo_id:
            photos = Photo.objects.filter(id=photo_id)
        else:
            return Response({"error": "Method GET is not allowed"})

        return Response({"photos": PhotoSerializer(photos, many=True).data})

    def post(self, request):
        serializer = PhotoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = request.data
        title = data.get("title")
        url = data.get("url")
        album_id = data.get("album")

        path_to_img = Photo.createPhotoInDir(title, url, album_id)
        if isinstance(path_to_img, dict):
            return Response({"error": path_to_img["message"]})
        else:
            height, width = get_image_size(path_to_img)
            color = get_image_color(path_to_img)

            img_path = path_to_img.split(".")
            ext = "." + img_path[1]
            folder_path = img_path[0]

            album = Album.objects.get(id=album_id)

            photo = Photo.objects.create(
                title=title,
                width=width,
                height=height,
                color="#" + color,
                url=folder_path[0:folder_path.rfind("/") + 1:],
                album=album,
                extension=ext
            )

        return Response({"photo": PhotoSerializer(photo).data})

    def put(self, request, *args, **kwargs):
        photo_id = kwargs.get("photo_id", None)

        serializer = PhotoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not Photo.objects.filter(id=photo_id).count():
            return Response({"error": f"Photo with id {photo_id} does not exist"})

        photo = Photo.objects.get(id=photo_id)
        old_data = {
            "old_title": photo.title,
            "old_album": photo.album,
            "old_url": photo.url
        }

        new_album_id = request.data.get("album")
        new_data = {
            "new_title": request.data.get("title"),
            "new_url": request.data.get("url"),
            "new_album_id": new_album_id,
            "new_album": Album.objects.get(id=new_album_id)
        }

        updated_photo = Photo.updatePhoto(old_data, new_data, photo_id)
        if isinstance(updated_photo, dict):
            return Response({"error": updated_photo["message"]})
        return Response({"photo": PhotoSerializer(updated_photo).data})

    def delete(self, request, *args, **kwargs):
        photo_id = kwargs.get("photo_id", None)

        if not photo_id:
            return Response({"error": "Method DELETE is not allowed"})

        photo = Photo.objects.get(id=photo_id)
        os.remove(photo.url + photo.title + photo.extension)
        photo.delete()
        return Response({"message": "Photo is deleted"})


class ImportPhotosFromAPI(APIView):
    def post(self, request, *args, **kwargs):

        api_request = request.data.get("api_request_url")
        if api_request:
            r = requests.get(api_request, auth=('user', 'pass'))
            r_status = r.status_code

            if r_status == 200:
                data = json.loads(r.content)
                res = createPhotosFromJSONData(data)
                return Response({"result": res})
            return Response({"error": f"requests to API status {r_status}"})
        return Response({"error": "api_request_url key required"})


class ImportPhotosFromJSONView(APIView):
    def post(self, request):
        file_path = request.data.get("absolute_filepath", None)

        if not file_path:
            return Response({"error": "File need to be given"})
        if os.path.exists(file_path):
            with open(file_path, 'r') as jsonfile:
                try:
                    content = jsonfile.read()
                    json_data = json.loads(content)
                    res = createPhotosFromJSONData(json_data)
                    return Response({"result": res})
                except:
                    return Response({"error": "Can not read file content. Make sure it's '.json' file"})

        return Response({"result": "File does not exist"})
