import os
import shutil

from django.db import models

from .utils import download_img, get_image_size, get_image_color


class Album(models.Model):
    title = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.title


class Photo(models.Model):
    title = models.CharField(max_length=100)
    width = models.IntegerField()
    height = models.IntegerField()
    color = models.CharField(max_length=30)
    url = models.CharField(max_length=100)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    extension = models.CharField(max_length=10)

    class Meta:
        unique_together = ('title', 'url')

    def __str__(self):
        return f"""title = {self.title},
        url = {self.url},
        color = {self.color},
        width = {self.width},
        height = {self.height},
        album_id = {self.album.id},
        extension = {self.extension}
        """

    @classmethod
    def createPhotoInDir(cls, title, imgURL, album_id):

        if Photo.objects.filter(title=title, album__id=album_id).count() > 0:
            album = Album.objects.get(id=album_id)
            return {"result": "error", "message": f"Photo with title {title} already exists in album {album.title}!"}
        if not (imgURL.lower().endswith(('.png', '.jpg', '.jpeg'))):
            imgURL += ".jpg"

        dest = os.path.abspath(os.curdir) + f"/photos/{album_id}/"
        isExist = os.path.exists(dest)
        if not isExist:
            os.makedirs(dest)

        path_to_img = download_img(imgURL, dest, title)
        return path_to_img

    @classmethod
    def addPhoto(cls, title, url, album_id):
        path_to_img = Photo.createPhotoInDir(title, url, album_id)
        if isinstance(path_to_img, dict):
            return {"message": path_to_img["message"]}
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

            return photo

    @classmethod
    def updatePhoto(cls, old_data, new_data, photo_id):
        new_title = new_data.get("new_title")
        new_url = new_data.get("new_url")
        new_album_id = new_data.get("new_album_id")
        new_album = new_data.get("new_album")

        old_title = old_data.get("old_title")
        old_url = old_data.get("old_url")
        old_album = old_data.get("old_album")

        if Photo.objects.filter(title=new_title, album__id=new_album_id).exists() \
                and new_url == old_url:
            return {"message": "A photo with this name already exists in the album."}
        if Photo.objects.filter(title=new_title, url=new_url).exists() and new_album_id == old_album.id:
            return {
                "message": "A photo with this name and url already exists."
                           " Change url (to locally store a file) or change title of photo if you want to store"
                           " it in directory shown below"
            }

        if new_title != old_title or old_album.id != new_album_id or new_url != old_url:

            photo = Photo.objects.get(id=photo_id)
            if new_title != old_title:
                os.rename(old_url + old_title + photo.extension, old_url + new_title + photo.extension)
                old_title = new_title

            if new_url != old_url:
                if new_url[-1] != "/":
                    new_url += "/"
                if not os.path.exists(new_url):
                    os.makedirs(new_url)
                new_path = new_url + new_title + photo.extension
                f = open(new_path, 'w')
                f.close()

                shutil.move(old_url + old_title + photo.extension, new_path)

        Photo.objects.filter(id=photo_id).update(
            title=new_title, url=new_url, album=new_album
        )
        updated_photo = Photo.objects.get(id=photo_id)
        return updated_photo
