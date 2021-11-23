from pathlib import Path

import requests

from constants import API_KEY


class YaUploader:
    def __init__(self, api_token):
        self.token = api_token

    def _get_headers(self):
        return {
            'Accept': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    @staticmethod
    def _get_params(file_path):
        return {
            'path': Path(file_path),
            'overwrite': 'true'
        }

    def upload(self, file_path):
        headers = self._get_headers()
        params = self._get_params(file_path)
        response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload', params=params,
                                headers=headers)
        upload_link = response.json().get('href')
        with open(file_path, 'rb') as file:
            uploading = requests.put(upload_link, data=file)
        if uploading.status_code == 201:
            print('File uploaded')
        else:
            print('Error! File not uploaded')


if __name__ == '__main__':
    path_to_file = "../json_xml/3.1.formats.json.xml/newsafr.json"
    token = API_KEY
    uploader = YaUploader(token)
    result = uploader.upload(path_to_file)
