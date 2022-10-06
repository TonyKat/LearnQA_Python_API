import pytest

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime


class TestUserEdit(BaseCase):
    user_data = ['username', 'firstName', 'lastName', 'email', 'password']

    def setup(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response_auth = MyRequests.post('/user/login', data=data)

        self.auth_sid = self.get_cookie(response_auth, 'auth_sid')
        self.token = self.get_header(response_auth, 'x-csrf-token')
        self.user_id_from_auth_method = self.get_json_value(response_auth, 'user_id')

    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post('/user/', data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        response3 = MyRequests.post('/user/login', data=login_data)

        auth_sid = self.get_cookie(response3, 'auth_sid')
        token = self.get_header(response3, 'x-csrf-token')

        # EDIT
        new_name = 'Changed Name'

        response4 = MyRequests.put(
            f'/user/{user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
            data={'firstName': new_name}
        )

        Assertions.assert_code_status(response4, 200)

        # GET

        response4 = MyRequests.get(
            f'/user/{user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            'firstName',
            new_name,
            f'Wrong name of user after edit')

    @pytest.mark.parametrize('data_of_user', user_data)
    def test_edit_user_without_authorization(self, data_of_user):
        # Попытаемся изменить данные пользователя, будучи неавторизованными
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post('/user/', data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        user_id = self.get_json_value(response1, 'id')

        # EDIT
        response3 = MyRequests.put(
            f'/user/{user_id}',
            data={data_of_user: 'new_' + data_of_user}
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode('utf-8') == f"Auth token not supplied", \
            f"Response content: {response3.content.decode('utf-8')}"

    @pytest.mark.parametrize('data_of_user', user_data)
    def test_edit_user_when_login_other_user(self, data_of_user):
        # Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
        # REGISTER 1
        register_data1 = {
            'password': '123',
            'username': 'username_1',
            'firstName': 'firstName_1',
            'lastName': 'lastName_1',
            'email': 'username_1' + datetime.now().strftime('%m%d%Y%H%M%S') + '@example.com'
        }
        response1_register = MyRequests.post('/user/', data=register_data1)

        Assertions.assert_code_status(response1_register, 200)
        Assertions.assert_json_has_key(response1_register, 'id')

        user_id1 = self.get_json_value(response1_register, 'id')

        # LOGIN 1
        login_data1 = {
            'email': register_data1['email'],
            'password': register_data1['password']
        }
        response1_login = MyRequests.post('/user/login', data=login_data1)

        auth_sid1 = self.get_cookie(response1_login, 'auth_sid')
        token1 = self.get_header(response1_login, 'x-csrf-token')

        # REGISTER 2
        register_data2 = {
            'password': '123',
            'username': 'username_2',
            'firstName': 'firstName_2',
            'lastName': 'lastName_2',
            'email': 'username_2' + datetime.now().strftime('%m%d%Y%H%M%S') + '@example.com'
        }
        response2_register = MyRequests.post('/user/', data=register_data2)

        Assertions.assert_code_status(response2_register, 200)
        Assertions.assert_json_has_key(response2_register, 'id')

        user_id2 = self.get_json_value(response2_register, 'id')

        # LOGIN 2
        login_data2 = {
            'email': register_data2['email'],
            'password': register_data2['password']
        }

        response2_login = MyRequests.post('/user/login', data=login_data2)

        auth_sid2 = self.get_cookie(response2_login, 'auth_sid')
        token2 = self.get_header(response2_login, 'x-csrf-token')

        # EDIT
        # Изменить данные {user_id1}, но передать 'x-csrf-token' и 'auth_sid' от {user_id2}
        response1_changed = MyRequests.put(
            f'/user/{user_id1}',
            headers={'x-csrf-token': token2},
            cookies={'auth_sid': auth_sid2},
            data={data_of_user: '!!!!!!!!!!!!new_!!!!!!!!!!!!!!_' + data_of_user}
        )

        Assertions.assert_code_status(response1_changed, 200)

        # GET 1 - проверить, что данные {user_id1} не изменились
        response1_get_new_data = MyRequests.get(
            f'/user/{user_id1}',
            headers={'x-csrf-token': token1},
            cookies={'auth_sid': auth_sid1}
        )

        expected_field = ['id', 'username', 'email', 'firstName', 'lastName']
        response1_get_new_data_in_dict = response1_get_new_data.json()
        Assertions.assert_json_has_keys(response1_get_new_data, expected_field)
        Assertions.assert_json_value_by_name(response1_get_new_data, 'id', user_id1,
                                             f"user_id1={user_id1} != "
                                             f"response1_get_new_data['id']={response1_get_new_data_in_dict['id']}")

        Assertions.assert_json_value_by_name(response1_get_new_data, 'username', register_data1['username'],
                                             f"register_data2['username']={register_data1['username']} != "
                                             f"response1_get_new_data['username']={response1_get_new_data_in_dict['username']}")

        Assertions.assert_json_value_by_name(response1_get_new_data, 'email', register_data1['email'],
                                             f"register_data2['email']={register_data1['email']} != "
                                             f"response1_get_new_data['email']={response1_get_new_data_in_dict['email']}")

        Assertions.assert_json_value_by_name(response1_get_new_data, 'firstName', register_data1['firstName'],
                                             f"register_data2['firstName']={register_data1['firstName']} != "
                                             f"response1_get_new_data['firstName']={response1_get_new_data_in_dict['firstName']}")

        Assertions.assert_json_value_by_name(response1_get_new_data, 'lastName', register_data1['lastName'],
                                             f"register_data2['lastName']={register_data1['lastName']} != "
                                             f"response1_get_new_data['lastName']={response1_get_new_data_in_dict['lastName']}")

        # GET 2 - проверить, что данные {user_id2} не изменились
        response2_get_new_data = MyRequests.get(
            f'/user/{user_id2}',
            headers={'x-csrf-token': token2},
            cookies={'auth_sid': auth_sid2}
        )
        response2_get_new_data_in_dict = response2_get_new_data.json()
        Assertions.assert_json_has_keys(response2_get_new_data, expected_field)
        Assertions.assert_json_value_by_name(response2_get_new_data, 'id', user_id2,
                                             f"user_id2={user_id2} != "
                                             f"response2_get_new_data['id']={response2_get_new_data_in_dict['id']}")

        Assertions.assert_json_value_by_name(response2_get_new_data, 'username', register_data2['username'],
                                             f"register_data2['username']={register_data2['username']} != "
                                             f"response2_get_new_data['username']={response2_get_new_data_in_dict['username']}")

        Assertions.assert_json_value_by_name(response2_get_new_data, 'email', register_data2['email'],
                                             f"register_data2['email']={register_data2['email']} != "
                                             f"response2_get_new_data['email']={response2_get_new_data_in_dict['email']}")

        Assertions.assert_json_value_by_name(response2_get_new_data, 'firstName', register_data2['firstName'],
                                             f"register_data2['firstName']={register_data2['firstName']} != "
                                             f"response2_get_new_data['firstName']={response2_get_new_data_in_dict['firstName']}")

        Assertions.assert_json_value_by_name(response2_get_new_data, 'lastName', register_data2['lastName'],
                                             f"register_data2['lastName']={register_data2['lastName']} != "
                                             f"response2_get_new_data['lastName']={response2_get_new_data_in_dict['lastName']}")

    def test_edit_email_of_user_to_incorrect_when_login_current_user(self):
        # Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @
        # REGISTER 1
        register_data1 = self.prepare_registration_data()
        response1_register = MyRequests.post('/user/', data=register_data1)

        Assertions.assert_code_status(response1_register, 200)
        Assertions.assert_json_has_key(response1_register, 'id')

        user_id1 = self.get_json_value(response1_register, 'id')

        # LOGIN 1
        login_data1 = {
            'email': register_data1['email'],
            'password': register_data1['password']
        }
        response1_login = MyRequests.post('/user/login', data=login_data1)

        auth_sid1 = self.get_cookie(response1_login, 'auth_sid')
        token1 = self.get_header(response1_login, 'x-csrf-token')

        # EDIT
        # Изменить данные email на новый email без символа @
        # передать 'x-csrf-token' и 'auth_sid' от {user_id1}
        response1_changed = MyRequests.put(
            f'/user/{user_id1}',
            headers={'x-csrf-token': token1},
            cookies={'auth_sid': auth_sid1},
            data={'email': register_data1['email'].replace('@', '_')}
        )

        Assertions.assert_code_status(response1_changed, 400)
        assert response1_changed.content.decode('utf-8') == f"Invalid email format", \
            f"Successfully registered email without @: {register_data1['email'].replace('@', '_')}"

    def test_edit_first_name_of_user_to_incorrect_when_login_current_user(self):
        # Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем,
        # на очень короткое значение в один символ
        # REGISTER 1
        register_data1 = self.prepare_registration_data()
        response1_register = MyRequests.post('/user/', data=register_data1)

        Assertions.assert_code_status(response1_register, 200)
        Assertions.assert_json_has_key(response1_register, 'id')

        user_id1 = self.get_json_value(response1_register, 'id')

        # LOGIN 1
        login_data1 = {
            'email': register_data1['email'],
            'password': register_data1['password']
        }
        response1_login = MyRequests.post('/user/login', data=login_data1)

        auth_sid1 = self.get_cookie(response1_login, 'auth_sid')
        token1 = self.get_header(response1_login, 'x-csrf-token')

        # EDIT
        # Изменить данные firstName на очень короткое значение в один символ
        # передать 'x-csrf-token' и 'auth_sid' от {user_id1}
        incorrect_first_name = 'a'
        response1_changed = MyRequests.put(
            f'/user/{user_id1}',
            headers={'x-csrf-token': token1},
            cookies={'auth_sid': auth_sid1},
            data={'firstName': incorrect_first_name}
        )
        response1_changed_to_dict = response1_changed.json()

        Assertions.assert_code_status(response1_changed, 400)
        assert response1_changed_to_dict['error'] == f"Too short value for field firstName", \
            f"Successfully registered short firstName = {incorrect_first_name}"
