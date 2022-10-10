import allure
import pytest

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime


class TestUserDelete(BaseCase):

    def setup(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response_auth = MyRequests.post('/user/login', data=data)

        self.auth_sid = self.get_cookie(response_auth, 'auth_sid')
        self.token = self.get_header(response_auth, 'x-csrf-token')
        self.user_id_from_auth_method = self.get_json_value(response_auth, 'user_id')

    @allure.description("TRIVIAL: Trying delete superuser with id = 2")
    @allure.severity(allure.severity_level.TRIVIAL)
    def test_delete_superuser(self):
        # Попытка удалить пользователя по ID 2
        id_of_superuser = '2'
        response_delete_superuser = MyRequests.delete(
            '/user/' + id_of_superuser,
            headers={'x-csrf-token': self.token},
            cookies={'auth_sid': self.auth_sid})

        Assertions.assert_code_status(response_delete_superuser, 400)
        assert response_delete_superuser.content.decode('utf-8') == f"Please, do not delete test users with ID " \
                                                                    f"1, 2, 3, 4 or 5.", \
            f"Response content: {response_delete_superuser.content.decode('utf-8')}"

    @allure.description("NORMAL: Trying delete new user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_new_user(self):
        # Создать пользователя, авторизоваться из-под него, удалить,
        # затем попробовать получить его данные по ID и убедиться, что пользователь действительно удален.

        # Создать пользователя
        register_data1 = self.prepare_registration_data()
        response1_register = MyRequests.post('/user/', data=register_data1)

        Assertions.assert_code_status(response1_register, 200)
        Assertions.assert_json_has_key(response1_register, 'id')

        # Авторизовывать созданным пользователем
        login_data1 = {
            'email': register_data1['email'],
            'password': register_data1['password']
        }
        response1_login = MyRequests.post('/user/login', data=login_data1)

        Assertions.assert_code_status(response1_login, 200)
        Assertions.assert_json_has_key(response1_login, 'user_id')

        user_id1 = self.get_json_value(response1_register, 'id')
        auth_sid1 = self.get_cookie(response1_login, 'auth_sid')
        token1 = self.get_header(response1_login, 'x-csrf-token')

        # Удалить созданного пользователя, из-под которого авторизованы
        response1_delete_new_user = MyRequests.delete(
            '/user/' + user_id1,
            headers={'x-csrf-token': token1},
            cookies={'auth_sid': auth_sid1}
        )

        Assertions.assert_code_status(response1_delete_new_user, 200)

        # Убедиться, что пользователь действительно удален
        response1_get_data_of_deleted_user = MyRequests.get(
            f'/user/{user_id1}',
            headers={'x-csrf-token': token1},
            cookies={'auth_sid': auth_sid1}
        )

        Assertions.assert_code_status(response1_get_data_of_deleted_user, 404)
        assert response1_get_data_of_deleted_user.content.decode('utf-8') == f"User not found", \
            f"Response content: {response1_get_data_of_deleted_user.content.decode('utf-8')}"

    @allure.description("CRITICAL: Trying delete new user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_user_when_login_other_user(self):
        # Удалить пользователя, будучи авторизованными другим пользователем
        # Создать пользователя 1
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

        # Авторизоваться созданным пользователем 1
        login_data1 = {
            'email': register_data1['email'],
            'password': register_data1['password']
        }
        response1_login = MyRequests.post('/user/login', data=login_data1)

        Assertions.assert_code_status(response1_login, 200)
        Assertions.assert_json_has_key(response1_login, 'user_id')

        user_id1 = self.get_json_value(response1_register, 'id')
        auth_sid1 = self.get_cookie(response1_login, 'auth_sid')
        token1 = self.get_header(response1_login, 'x-csrf-token')

        # Создать пользователя 2
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

        # Авторизоваться созданным пользователем 2
        login_data2 = {
            'email': register_data2['email'],
            'password': register_data2['password']
        }

        response2_login = MyRequests.post('/user/login', data=login_data2)

        Assertions.assert_code_status(response2_login, 200)
        Assertions.assert_json_has_key(response2_login, 'user_id')

        user_id2 = self.get_json_value(response2_register, 'id')
        auth_sid2 = self.get_cookie(response2_login, 'auth_sid')
        token2 = self.get_header(response2_login, 'x-csrf-token')

        # Удалить созданного пользователя 1, будучи авторизованными пользователем 2
        response2_delete_new_user = MyRequests.delete(
            '/user/' + user_id1,
            headers={'x-csrf-token': token2},
            cookies={'auth_sid': auth_sid2}
        )

        Assertions.assert_code_status(response2_delete_new_user, 200)

        # Проверить, что данные пользователя 1 не изменились
        response1_get_new_data = MyRequests.get(
            f'/user/{user_id1}',
            headers={'x-csrf-token': token1},
            cookies={'auth_sid': auth_sid1}
        )

        expected_field = ['id', 'username', 'email', 'firstName', 'lastName']
        Assertions.assert_code_status(response1_get_new_data, 200)
        Assertions.assert_json_has_keys(response1_get_new_data, expected_field)

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

        # Проверить, что данные пользователя 2 не изменились
        response2_get_new_data = MyRequests.get(
            f'/user/{user_id2}',
            headers={'x-csrf-token': token2},
            cookies={'auth_sid': auth_sid2}
        )

        Assertions.assert_code_status(response2_get_new_data, 200)
        Assertions.assert_json_has_keys(response2_get_new_data, expected_field)

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
