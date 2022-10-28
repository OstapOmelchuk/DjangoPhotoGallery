import os
import shutil

from django.forms import HiddenInput
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Album, Photo
from .forms import AlbumForm, PhotoForm
from .utils import get_image_size, get_image_color


def home(request):
    album = Album.objects.all()

    context = {"albums": album}
    return render(request, 'galleryapp/home.html', context)


def albumData(request, pk):
    album = Album.objects.get(id=pk)
    photos = Photo.objects.filter(album__id=pk)

    photos_count = photos.count()

    context = {"photos": photos, "photos_count": photos_count, "album": album}
    return render(request, 'galleryapp/album_photos.html', context)


def addPhoto(request, album_id):
    form = PhotoForm()
    form.fields['album'].widget = HiddenInput()

    album = Album.objects.get(id=album_id)

    if request.method == "POST":
        title = request.POST.get("title")
        imgURL = request.POST.get("url")

        photo = Photo.addPhoto(title=title, url=imgURL, album_id=album_id)
        if isinstance(photo, dict):
            return HttpResponse(photo['message'])
        return redirect('album', album_id)

    context = {"form": form, "album": album}
    return render(request, 'galleryapp/photo_form.html', context)


def updatePhoto(request, album_id, photo_id):
    album = Album.objects.get(id=album_id)
    photo = Photo.objects.get(id=photo_id)
    if not album or not photo:
        return HttpResponse("No photo to update (wrong photo_id or album_id)")
    form = PhotoForm(instance=photo)

    if request.method == "POST":
        old_data = {
            "old_title": photo.title,
            "old_album": photo.album,
            "old_url": photo.url
        }

        new_album_id = request.POST.get("album")
        new_data = {
            "new_title": request.POST.get("title"),
            "new_url": request.POST.get("url"),
            "new_album_id": new_album_id,
            "new_album": Album.objects.get(id=new_album_id)
        }

        updated_photo = Photo.updatePhoto(old_data, new_data, photo_id)
        if isinstance(updated_photo, dict):
            return HttpResponse(updated_photo["message"])
        return redirect('album', album_id)

    context = {"form": form, "album": album, "message": ""}
    return render(request, 'galleryapp/photo_form.html', context)


def deletePhoto(request, album_id, photo_id):
    photo = Photo.objects.get(id=photo_id)

    if request.method == "POST":
        os.remove(photo.url + photo.title + photo.extension)
        photo.delete()
        return redirect('album', album_id)

    context = {"obj": photo, "album_id": album_id}
    return render(request, 'galleryapp/delete_photo.html', context)


def createAlbum(request):
    form = AlbumForm()

    if request.method == "POST":
        album_title = request.POST.get("title")
        album, created = Album.objects.get_or_create(title=album_title)
        if created:
            return redirect('home')
        return HttpResponse("An album with this name already exists.")

    context = {"form": form}
    return render(request, 'galleryapp/album_form.html', context)


def updateAlbum(request, id):
    album = Album.objects.get(id=id)
    form = AlbumForm(instance=album)

    old_title = album.title

    if request.method == "POST":
        new_title = request.POST.get("title")
        if new_title != old_title:
            form = AlbumForm(request.POST, instance=album)
            if not form.is_valid() or Album.objects.filter(title=new_title).exists():
                return HttpResponse("An album with this name already exists.")
            form.save()
            return redirect('home')
        return HttpResponse("You have to change data to update it.")

    context = {"form": form}
    return render(request, 'galleryapp/album_form.html', context)


def deleteAlbum(request, id):
    album = Album.objects.get(id=id)

    if request.method == "POST":
        album_photos = Photo.objects.filter(album__id=id)

        for photo in album_photos:
            os.remove(photo.url + photo.title + photo.extension)
        album.delete()
        return redirect('home')

    return render(request, 'galleryapp/delete_album.html', {"obj": album})
