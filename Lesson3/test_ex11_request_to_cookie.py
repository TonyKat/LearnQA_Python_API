import pytest
import requests
from Lesson3.lib.base_case import BaseCase
from Lesson3.lib.assertions import Assertions


class TestRequestToCookie(BaseCase):

    exclude_params = [
        ('HomeWork', 'hw_value'),
        ('fake_key', 'fake_value')
    ]

    @pytest.mark.parametrize('expected_cookies', exclude_params)
    def test_request_to_cookie(self, expected_cookies):
        print('\n--------- BEGIN: print_cookies ---------')
        print(f'current exclude_params = {expected_cookies}\n')
        response = requests.get('https://playground.learnqa.ru/api/homework_cookie')

        # получить куку из response.cookies
        cookies_from_cookies = response.cookies
        cookies_to_dict = dict(cookies_from_cookies)
        for key, value in cookies_to_dict.items():
            print(f'cookies_to_dict[{key}] = {value}')
        print('--------- END: print_cookies -----------\n')

        Assertions.assert_cookie_value_by_name(
            response,
            expected_cookies[0],
            expected_cookies[1],
            f"cookie from response is not equal my test_data['{expected_cookies[0]}']={expected_cookies[1]}"
        )
