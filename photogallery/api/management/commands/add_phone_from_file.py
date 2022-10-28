import json
import os

import requests
from django.core.management.base import BaseCommand

from api.utils import createPhotosFromJSONData

import sys


class Command(BaseCommand):
    help = 'reading data from api request and add it to db'

    def add_arguments(self, parser):
        parser.add_argument('api_request', nargs='+', type=str)

    def handle(self, *args, **options):

        file_path = str(sys.argv[2])

        if not file_path:
            return {"error": "File need to be given"}
        if os.path.exists(file_path):
            with open(file_path, 'r') as jsonfile:
                try:
                    content = jsonfile.read()
                    json_data = json.loads(content)
                    res = createPhotosFromJSONData(json_data)
                    return {"result": res}
                except:
                    return {"error": "Can not read file content. Make sure it's '.json' file"}

        return {"result": "File does not exist"}
