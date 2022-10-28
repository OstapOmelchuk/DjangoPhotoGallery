from django.forms import ModelForm
from .models import Album, Photo


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'url', 'album']


class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = '__all__'
