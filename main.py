import os

import requests
import os.path as op


TOKEN_PATH = op.join(os.getcwd(), 'token')


def get_token():
    try:
        with open(TOKEN_PATH, 'r') as f:
            token = f.readline()
    except FileNotFoundError:
        print("File not found")
    return token


HEADERS = {'Authorization': 'OAuth ' + get_token()}


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def upload(self, file_path: str):
        """Метод загруджает файл file_path на яндекс диск"""

        response = requests.get(
            url='https://cloud-api.yandex.net/v1/disk/resources/upload',
            params={'path': op.basename(file_path), 'overwrite': 'true'},
            headers=HEADERS
        )
        response.raise_for_status()

        data = response.json()
        href = data['href']

        # try:
        with open(file_path, 'rb') as f:
            response = requests.put(href, files={'file': f})
            response.raise_for_status()  # TODO узнать какие ошибки возникают
        # except:
        #     print()

        return 'Вернуть ответ об успешной загрузке'


if __name__ == '__main__':
    uploader = YaUploader(TOKEN_PATH)
    result = uploader.upload('C:\\Users\\Nikita\\Desktop\\1.txt')
