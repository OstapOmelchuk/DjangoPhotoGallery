from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('album/<int:pk>/', views.albumData, name="album"),
    path('create-album/', views.createAlbum, name="create-album"),
    path('update-album/<int:id>', views.updateAlbum, name="update-album"),
    path('delete-album/<int:id>', views.deleteAlbum, name="delete-album"),

    path('album/<int:album_id>/add-photo/', views.addPhoto, name="add-photo"),
    path('album/<int:album_id>/update-photo/<int:photo_id>', views.updatePhoto, name="update-photo"),
    path('album/<int:album_id>/delete-photo/<int:photo_id>', views.deletePhoto, name="delete-photo"),
]

