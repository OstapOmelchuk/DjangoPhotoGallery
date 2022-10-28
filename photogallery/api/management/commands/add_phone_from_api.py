import json

import requests
from django.core.management.base import BaseCommand, CommandError

from api.utils import createPhotosFromJSONData
from galleryapp.models import Photo, Album

import sys


class Command(BaseCommand):
    help = 'reading data from api request and add it to db'

    def add_arguments(self, parser):
        parser.add_argument('api_request', nargs='+', type=str)

    def handle(self, *args, **options):
        api_request = str(sys.argv[2])

        if api_request:
            r = requests.get(api_request, auth=('user', 'pass'))
            r_status = r.status_code

            if r_status == 200:
                data = json.loads(r.content)
                res = createPhotosFromJSONData(data)
                return res
            return r_status
        return {"error": "api_request_url key required"}
