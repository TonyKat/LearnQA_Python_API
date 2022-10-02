import pytest

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):
    names = ['firstName', 'lastName']
    incorrect_users = [
        [
            {
                # 'password': '123',
                'username': 'learnqa',
                'firstName': 'learnqa',
                'lastName': 'learnqa',
                'email': 'vinkotov@example.com'
            },
            'password'
        ],
        [
            {
                'password': '123',
                # 'username': 'learnqa',
                'firstName': 'learnqa',
                'lastName': 'learnqa',
                'email': 'vinkotov@example.com'
            },
            'username'
        ],
        [
            {
                'password': '123',
                'username': 'learnqa',
                # 'firstName': 'learnqa',
                'lastName': 'learnqa',
                'email': 'vinkotov@example.com'
            },
            'firstName'
        ],
        [
            {
                'password': '123',
                'username': 'learnqa',
                'firstName': 'learnqa',
                # 'lastName': 'learnqa',
                'email': 'vinkotov@example.com'
            },
            'lastName'
        ],
        [
            {
                'password': '123',
                'username': 'learnqa',
                'firstName': 'learnqa',
                'lastName': 'learnqa',
                # 'email': 'vinkotov@example.com'
            },
            'email'
        ]
    ]

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    def test_create_user_with_not_correct_email(self):
        data = self.prepare_registration_data()
        data['email'] = data['email'].replace('@', '_')

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"Invalid email format", f"Response content {response.content}"

    @pytest.mark.parametrize('name', names)
    def test_create_user_with_short_name(self, name):
        data = self.prepare_registration_data()

        data[name] = 'a'

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"The value of '{name}' field is too short", \
            f"Response content {response.content}"

    @pytest.mark.parametrize('name', names)
    def test_create_user_with_long_name(self, name):
        data = self.prepare_registration_data()

        data[name] = 'long_name_long_name_long_name_long_name_long_name_long_name_long_name_long_name_long_name_' \
                     'long_name_long_name_long_name_long_name_long_name_long_name_long_name_long_name_long_name_' \
                     'long_name_long_name_long_name_long_name_long_name_long_name_long_name_!'

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"The value of '{name}' field is too long", \
            f"Response content {response.content}"

    @pytest.mark.parametrize('incorrect_user', incorrect_users)
    def test_create_user_without_filling_all_params(self, incorrect_user):
        response = MyRequests.post('/user/', data=incorrect_user[0])

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"The following required params are missed: {incorrect_user[1]}", \
            f"Response content {response.content}"
