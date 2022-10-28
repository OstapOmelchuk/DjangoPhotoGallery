# Project description

### The PhotoGallery project consists of two parts (Web and API).
### Web part for convenient display of functionality:
- Adding an album, updating and deleting an album (with all its photos both from the database and from the local storage where photos are stored in folders)
- Adding a photo (through the URL address), deleting and updating (changing the name, belonging to the album and changing the location of the photo in the local storage, i.e. moving the photo to a another folder)
### API part:
- API has ALL the same functionality as mentioned above, and also the ability to import photos from external API (at 'https://jsonplaceholder.typicode.com/photos') and Import photos from JSON file via both
REST API and a CLI script (instructions on how to do this are at the end of the file)

___
# Change directory to source folder

    cd DjangoPhotoGallery/photogallery/
___
# Environment variables

in source directory create .env file and add the correct data in the middle of the '<>' :

    POSTGRES_HOST=<host_name> 

    POSTGRES_DB='<db_name>'

    POSTGRES_USER='<postgres_user>'

    POSTGRES_PASSWORD='<postgres_password>'

<br>

___
# Installation of necessary packages


To install all the packages activate your virtualenv and run the following command in your terminal:
    
    pip install -r requirements.txt

<br>

---
# Creating a database

To create DB - type in your terminal:

    createdb -h <host_name> -p <postgres_port> -U <postgres_user> <db_name>

for example:

    createdb -h localhost -p 5432 -U postgres PhotoGallery

<br>

___

# Migrations

Type in your terminal:

    python manage.py makemigrations

then:
    
    python manage.py migrate


# Start app

    python manage.py runserver

___

# Some PhotoGallery API requests (add photos from external API and JSON file):

___

### import photos from external API: 

    method: POST 
    ur: http://127.0.0.1:8000/api/v1/import-api-photo/
    
### request data for import:

    {
        "api_request_url": "https://jsonplaceholder.typicode.com/photos"
    }
---

### import photos from JSON:

    method: POST 
    ur: http://127.0.0.1:8000/api/v1/import-json-file-photo/
    
### request data for import:

In the source directory of this project I created test json file - photos_data.json, so we can test this request.

    {
        "absolute_filepath": "/home/ostap/Django/DjangoPhotoGallery/photogallery/photos_data.json"
    }
---

# PhotoGallery CLI (add photos from external API and JSON file):

___

### To run import photos from external API script run:
    
    python manage.py add_phone_from_api https://jsonplaceholder.typicode.com/photos
---
### To run import photos from JSON file script run:
    
    python manage.py add_phone_from_file /home/ostap/Django/DjangoPhotoGallery/photogallery/photos_data.json
---

### Tests in development...

---