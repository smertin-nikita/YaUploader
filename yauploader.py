import os

import requests
import os.path as op


TOKEN_PATH = op.join(os.getcwd(), 'token')


def get_token(path):
    try:
        with open(path, 'r') as f:
            token = f.readline()
    except FileNotFoundError:
        print("File not found")
    return token


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def upload(self, file_path: str):
        """Метод загруджает файл file_path на яндекс диск"""

        try:
            response = requests.get(
                url='https://cloud-api.yandex.net/v1/disk/resources/upload',
                params={'path': op.basename(file_path), 'overwrite': 'true'},
                headers={'Authorization': 'OAuth ' + self.token}
            )
            response.raise_for_status()
        except requests.RequestException as e:
            print(e.response.status_code)
            return False

        data = response.json()
        href = data['href']

        try:
            with open(file_path, 'rb') as f:
                response = requests.put(href, files={'file': f})
                response.raise_for_status()
                return True
        except FileNotFoundError:
            print('Файл не найден')
            return False
        except requests.RequestException as e:
            print(e.response.status_code)
            return False

    def create_folder(self, file_path: str):
        response = requests.put(
            url='https://cloud-api.yandex.net/v1/disk/resources/',
            params={'path': op.basename(file_path), 'overwrite': 'true'},
            headers={'Authorization': 'OAuth ' + self.token}
        )
        response.raise_for_status()
        return response.status_code

    def get_resource_info(self, file_path: str):
        response = requests.get(
            url='https://cloud-api.yandex.net/v1/disk/resources/',
            params={'path': op.basename(file_path)},
            headers={'Authorization': 'OAuth ' + self.token}
        )
        response.raise_for_status()

        data = response.json()

        return data


if __name__ == '__main__':
    uploader = YaUploader(get_token(TOKEN_PATH))
    result = uploader.get_resource_info('new folder')['name']
    print(result)
