import time
from galleryapp.models import Album, Photo


def createPhotosFromJSONData(data):
    message = ""
    for ph in data:
        title = ph.get("title")
        url = ph.get("url")
        album_id = ph.get("albumId")

        if not Album.objects.filter(id=album_id).exists():
            album_title = "Album #" + str(int(time.time()))
            Album.objects.create(id=album_id, title=album_title)
        if not Photo.objects.filter(title=title, album_id=album_id).exists():
            photo = Photo.addPhoto(title=title, url=url, album_id=album_id)
            if isinstance(photo, dict):
                message += f"{photo['message']}>^"
        else:
            message += f"Photo with title {title} and album_id {album_id} already exist." \
                       f" Change title/album_id or delete existing photo^"
    if message:
        messages = message[:-1].split("^")
        error_keys = ["error_" + str(err_num) for err_num in range(1, len(messages) + 1)]
        msg_dict = dict(zip(error_keys, messages))
        res = {"result": {"error": "Some photos have not been added", "errors_occurred": msg_dict}}
    else:
        res = {"result": "success"}

    return res
