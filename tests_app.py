import app as app
import pytest
import unittest.mock


DOC_TYPE = 'passport'
DOC_NUMBER = 'test-1111'
OWNER_NAME = 'test-owner-2222'
SHELF_NUMBER = '111'


class TestApp:

    # перед запуском тестов очистим список документов и полок:
    def setup(self):
        app.directories = {}
        app.documents = []

    # check_document_existance: проверим что документа с таким номером нет:
    def test_check_doc_not_exists(self):
        assert app.check_document_existance('00000') is False

    # check_document_existance: создадим полку и документ, и проверим его наличие:
    def test_check_doc_exists(self):
        app.documents = [{"type": DOC_TYPE, "number": DOC_NUMBER, "name": OWNER_NAME}]
        app.directories = {SHELF_NUMBER: [DOC_NUMBER]}
        assert app.check_document_existance(DOC_NUMBER) is True

    # get_doc_owner_name: проверим, что имя владельца возвращается корректно:
    @pytest.mark.parametrize('doc_number, return_value', [(DOC_NUMBER, OWNER_NAME), ('0000', None)])
    def test_get_doc_owner_name(self, doc_number, return_value):
        app.documents = [{"type": DOC_TYPE, "number": DOC_NUMBER, "name": OWNER_NAME}]
        app.directories = {SHELF_NUMBER: [DOC_NUMBER]}
        with unittest.mock.patch('app.input', return_value=doc_number):
            assert app.get_doc_owner_name() == return_value

    # remove_doc_from_shelf: проверим, что удаленного документа нет на полке:
    def test_remove_doc_from_shelf(self):
        app.documents = [{"type": DOC_TYPE, "number": DOC_NUMBER, "name": OWNER_NAME}]
        app.directories = {SHELF_NUMBER: [DOC_NUMBER]}
        assert app.remove_doc_from_shelf(DOC_NUMBER) is None
        assert app.directories.get(SHELF_NUMBER) == []

    # add_new_shelf: проверим, что создается новая полка (а с существующим номером не создается):
    @pytest.mark.parametrize('shelf_num, return_value', [(SHELF_NUMBER, (SHELF_NUMBER, False)), ('12', ('12', True))])
    def test_add_new_shelf(self, shelf_num, return_value):
        app.documents = [{"type": DOC_TYPE, "number": DOC_NUMBER, "name": OWNER_NAME}]
        app.directories = {SHELF_NUMBER: []}
        with unittest.mock.patch('app.input', return_value=return_value):
            assert app.add_new_shelf(shelf_num) == return_value

    # append_doc_to_shelf: проверим добавление нового документа:
    @pytest.mark.parametrize('doc_num, shelf_num', [(DOC_NUMBER, SHELF_NUMBER)])
    def test_append_new_doc_to_shelf(self,doc_num, shelf_num):
        app.append_doc_to_shelf(doc_num, shelf_num)
        assert app.directories.get(shelf_num) == [doc_num]

    # append_doc_to_shelf: проверим добавление уже существующего документа:
    @pytest.mark.parametrize('doc_num, shelf_num', [(DOC_NUMBER, SHELF_NUMBER)])
    def test_append_new_doc_to_shelf(self,doc_num, shelf_num):
        app.documents = [{"type": DOC_TYPE, "number": DOC_NUMBER, "name": OWNER_NAME}]
        app.directories = {SHELF_NUMBER: [DOC_NUMBER]}
        app.append_doc_to_shelf(doc_num, shelf_num)
        assert app.directories.get(shelf_num) == [doc_num, doc_num]

    # delete_doc: проверим удаление существующего документа:
    @pytest.mark.parametrize('return_value, return_boolean', [(DOC_NUMBER, True)])
    def test_delete_doc(self, return_value, return_boolean):
        app.documents = [{"type": DOC_TYPE, "number": DOC_NUMBER, "name": OWNER_NAME}]
        app.directories = {SHELF_NUMBER: [DOC_NUMBER]}
        with unittest.mock.patch('app.input', return_value=return_value):
            assert app.delete_doc() == (return_value, return_boolean)
            assert {"type": DOC_TYPE, "number": DOC_NUMBER, "name": OWNER_NAME} not in app.documents

    # delete_doc: проверим удаление несуществующего документа:
    @pytest.mark.parametrize('return_value, return_none', [(DOC_NUMBER, None)])
    def test_delete_not_existed_doc(self, return_value, return_none):
        with unittest.mock.patch('app.input', return_value=return_value):
            assert app.delete_doc() == return_none

    # get_doc_shelf: проверим, что возвращается правильный номер полки:
    @pytest.mark.parametrize('doc_num, shelf_num', [(DOC_NUMBER, SHELF_NUMBER), ('999', None)])
    def test_get_doc_shelf(self, doc_num, shelf_num):
        app.documents = [{"type": DOC_TYPE, "number": DOC_NUMBER, "name": OWNER_NAME}]
        app.directories = {SHELF_NUMBER: [DOC_NUMBER]}
        with unittest.mock.patch('app.input', return_value=doc_num):
            assert app.get_doc_shelf() == shelf_num

    # move_doc_to_shelf: проверим, что документ перемещен на полку + проверим сообщение об успехе:
    @pytest.mark.parametrize('mock_args', [(DOC_NUMBER, SHELF_NUMBER)])
    @unittest.mock.patch('app.print')
    @unittest.mock.patch('app.input', create=True)
    def test_move_doc_to_shelf(self, mock_input, mock_print, mock_args):
        app.documents = [{"type": DOC_TYPE, "number": DOC_NUMBER, "name": OWNER_NAME}]
        app.directories = {SHELF_NUMBER: [DOC_NUMBER]}
        mock_input.side_effect = [mock_args[0], mock_args[1]]
        app.move_doc_to_shelf()
        mock_print.assert_called_with(f'Документ номер "{mock_args[0]}" был перемещен на полку '
                                          f'номер "{mock_args[1]}"')
        assert app.directories.get(mock_args[1]) == [mock_args[0]]


    # show_all_docs_info: проверим корректность отображения инфо обо всех документах:
    @pytest.mark.parametrize('mock_args', [[DOC_TYPE, DOC_NUMBER, OWNER_NAME]])
    @unittest.mock.patch('app.print')
    def test_show_all_docs_info(self, mock_print, mock_args):
        app.documents = [{"type": DOC_TYPE, "number": DOC_NUMBER, "name": OWNER_NAME}]
        app.directories = {SHELF_NUMBER: [DOC_NUMBER]}
        app.show_all_docs_info()
        mock_print.assert_called_with(f'{mock_args[0]} "{mock_args[1]}" "{mock_args[2]}"')

    # add_new_doc: проверим, что документ добавлен и метод вернул номер полки:
    @pytest.mark.parametrize('directories', [{SHELF_NUMBER: []}, {}])
    def test_add_new_doc(self, directories):
        app.directories = directories
        mock_args = [DOC_NUMBER, DOC_TYPE, OWNER_NAME, SHELF_NUMBER]
        with unittest.mock.patch('app.input') as mocked_input:
            mocked_input.side_effect = mock_args
            assert app.add_new_doc() == SHELF_NUMBER
        assert app.directories.get(SHELF_NUMBER) == [DOC_NUMBER]
        assert {"type": DOC_TYPE, "number": DOC_NUMBER, "name": OWNER_NAME} in app.documents

    def teardown(self):
        # Перед завершением теста очистим документы и полки:
        app.directories = {}
        app.documents = []