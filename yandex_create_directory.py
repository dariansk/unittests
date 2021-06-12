import requests


class YaDiskMakeDir:
    def __init__(self, token):
        self.token = token
        if self.token == '':
            print('Не указан токен.')

    def get_headers(self):
        return {'Content-Type': 'application/json',
                'Authorization': 'OAuth {}'.format(self.token)
                }

    def make_directory(self):
        ya_disk_directory = input('Имя папки: ')
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': ya_disk_directory}
        response = requests.put(upload_url, headers=headers, params=params)
        return response.status_code, response.json()