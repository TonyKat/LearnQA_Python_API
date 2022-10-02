import datetime

import pytest
import requests
from Lesson3.lib.base_case import BaseCase
from Lesson3.lib.assertions import Assertions


class TestUserAgent(BaseCase):
    exclude_params = [
        {
            'user_agent': 'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
            'platform': 'Mobile',
            'browser': 'No',
            'device': 'Android'

        },
        {
            'user_agent': 'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
            'platform': 'Mobile',
            'browser': 'Chrome',
            'device': 'iOS'
        },
        {
            'user_agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'platform': 'Googlebot',
            'browser': 'Unknown',
            'device': 'Unknown'
        },
        {
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0',
            'platform': 'Web',
            'browser': 'Chrome',
            'device': 'No'
        },
        {
            'user_agent': 'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'platform': 'Mobile',
            'browser': 'No',
            'device': 'iPhone'
        }
    ]

    @pytest.mark.parametrize('user_agents', exclude_params)
    def test_user_agent(self, user_agents):

        response = requests.get('https://playground.learnqa.ru/ajax/api/user_agent_check',
                                headers={'User-Agent': user_agents['user_agent']})

        response_as_dict = dict(response.json())

        print('\n--------- BEGIN: print_user_agents ---------')
        for key, value in user_agents.items():
            print(f"user_agents['{key}'] = {value}")
            print(f"response_as_dict['{key}'] = {response_as_dict[key]}")
            print(f"It's a bug: {False if value == response_as_dict[key] else True}")
        print('--------- END: print_user_agents -----------\n')

        for key, value in user_agents.items():
            Assertions.assert_user_agent_value_by_name(
                response,
                key,
                value,
                f"{key} from response is not equal my "
                f"user_agents['{key}']={value}"
            )
