import pytest

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserGet(BaseCase):
    def test_get_user_not_details_not_auth(self):
        response = MyRequests.get('/user/2')

        print('\n', response.text)

        Assertions.assert_json_has_key(response, 'username')
        Assertions.assert_json_has_not_key(response, 'email')
        Assertions.assert_json_has_not_key(response, 'firstName')
        Assertions.assert_json_has_not_key(response, 'lastName')

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post('/user/login', data=data)

        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(response1, 'user_id')

        response2 = MyRequests.get(
            f"/user/{user_id_from_auth_method}",
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )

        expected_field = ['username', 'email', 'firstName', 'lastName']
        Assertions.assert_json_has_keys(response2, expected_field)

    def test_get_user_details_auth_as_other_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response = MyRequests.post('/user/', data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')
        user_id = self.get_json_value(response, 'id')

        # test get user details auth as other user
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post('/user/login', data=data)

        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(response1, 'user_id')

        print(f'\ncurrent test with user_id = {user_id}')
        print(f'current login with user_id = {user_id_from_auth_method}')

        response2 = MyRequests.get(
            f"/user/{user_id}",
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )

        if user_id == user_id_from_auth_method:
            print(f'user_id == user_id_from_auth_method: {user_id_from_auth_method}')
            expected_field = ['username', 'email', 'firstName', 'lastName']
            Assertions.assert_json_has_keys(response2, expected_field)
        else:
            Assertions.assert_json_has_key(response2, 'username')
            Assertions.assert_json_has_not_key(response2, 'email')
            Assertions.assert_json_has_not_key(response2, 'firstName')
            Assertions.assert_json_has_not_key(response2, 'lastName')
