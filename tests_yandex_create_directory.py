import yandex_create_directory
import time
import datetime
import requests
import unittest.mock as mock

YANDEX_DISK_TOKEN = '...'
URL = 'https://cloud-api.yandex.net/v1/disk/resources'
HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'OAuth {}'.format(YANDEX_DISK_TOKEN)
}

# создать папку и проверить ответ
# создать папку с существующим именем папки
# создать папку без имени папки
# создать папку без авторизации

class TestYaDiskMakeDir:

    # Создадим папку и проверить ответ 200. Удалим созданную папку.
    def test_make_new_dir(self):
        directory_name = str(datetime.datetime.fromtimestamp(int(time.time()))).replace(':', '-')
        dir_replaced = directory_name.replace(' ', '+')
        with mock.patch('yandex_create_directory.input', return_value=directory_name):
            assert yandex_create_directory.YaDiskMakeDir(YANDEX_DISK_TOKEN).make_directory() == (201, {'href': f'https://cloud-api.yandex.net/v1/disk/resources?path=disk%3A%2F{dir_replaced}','method': 'GET', 'templated': False})
        url = URL
        headers = HEADERS
        params = {'path': directory_name}
        requests.delete(url, headers=headers, params=params)

    # Проверим, что папка с уже существующим именем не создается
    def test_make_same_dir(self):
        directory_name = str(datetime.datetime.fromtimestamp(int(time.time()))).replace(':', '-')
        dir_replaced = directory_name.replace(' ', '+')
        with mock.patch('yandex_create_directory.input', return_value=directory_name):
            assert yandex_create_directory.YaDiskMakeDir(YANDEX_DISK_TOKEN).make_directory() == \
                   (201, {'href': f'https://cloud-api.yandex.net/v1/disk/resources?path=disk%3A%2F{dir_replaced}','method': 'GET', 'templated': False})
        with mock.patch('yandex_create_directory.input', return_value=directory_name):
            assert yandex_create_directory.YaDiskMakeDir(YANDEX_DISK_TOKEN).make_directory() == \
                   (409, {'message': f'По указанному пути \"{directory_name}\" уже существует папка с таким именем.','description': f'Specified path \"{directory_name}\" points to existent directory.','error': 'DiskPathPointsToExistentDirectoryError'})

    # Проверим, что папка без имени не создается
    def test_make_no_name_dir(self):
        with mock.patch('yandex_create_directory.input', return_value=''):
            assert yandex_create_directory.YaDiskMakeDir(YANDEX_DISK_TOKEN).make_directory() == \
                   (400, {'message': 'Ошибка проверки поля "path": Это поле является обязательным.', 'description': 'Error validating field "path": This field is required.', 'error': 'FieldValidationError'})

    # Проверим, что без авторизации папка не создается
    def test_make_dir_anonym(self):
        directory_name = str(datetime.datetime.fromtimestamp(int(time.time()))).replace(':', '-')
        with mock.patch('yandex_create_directory.input', return_value=directory_name):
            assert yandex_create_directory.YaDiskMakeDir('').make_directory() == (401, {'message': 'Не авторизован.', 'description': 'Unauthorized', 'error': 'UnauthorizedError'})