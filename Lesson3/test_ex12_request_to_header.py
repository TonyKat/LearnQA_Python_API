import datetime

import pytest
import requests
from Lesson3.lib.base_case import BaseCase
from Lesson3.lib.assertions import Assertions


class TestRequestToHeader(BaseCase):

    current_datetime = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
    exclude_params = [
        ('Date', current_datetime),
        ('Content-Type', 'application/json'),
        ('Content-Length', '15'),
        ('Connection', 'keep-alive'),
        ('Keep-Alive', 'timeout=10'),
        ('Server', 'Apache'),
        ('x-secret-homework-header', 'Some secret value'),
        ('Cache-Control', 'max-age=0'),
        ('Expires', current_datetime)
    ]

    @pytest.mark.parametrize('expected_headers', exclude_params)
    def test_request_to_header(self, expected_headers):
        print('\n--------- BEGIN: print_headers ---------')
        print(f'current exclude_params = {expected_headers}\n')
        response = requests.get('https://playground.learnqa.ru/api/homework_header')

        # получить заголовки из response.headers
        headers = response.headers
        headers_to_dict = dict(headers)
        for key, value in headers_to_dict.items():
            print(f'headers_to_dict[{key}] = {value}')
        print('--------- END: print_headers -----------\n')

        Assertions.assert_header_value_by_name(
            response,
            expected_headers[0],
            expected_headers[1],
            f"header from response is not equal my test_data['{expected_headers[0]}']={expected_headers[1]}"
        )
