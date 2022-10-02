from requests import Response


class Assertions:

    @staticmethod
    def assert_cookie_value_by_name(response: Response, name_of_cookie, expected_value, error_message):
        response_as_dict = dict(response.cookies)

        assert name_of_cookie in response_as_dict, f"Cookie from response doesn't have key '{name_of_cookie}'"
        assert response_as_dict[name_of_cookie] == expected_value, error_message

    @staticmethod
    def assert_header_value_by_name(response: Response, name_of_header, expected_value, error_message):
        response_as_dict = dict(response.headers)

        assert name_of_header in response_as_dict, f"Header from response doesn't have key '{name_of_header}'"
        assert response_as_dict[name_of_header] == expected_value, error_message

    @staticmethod
    def assert_user_agent_value_by_name(response: Response, name_of_user_agent, expected_value, error_message):
        response_as_dict = dict(response.json())

        assert name_of_user_agent in response_as_dict, f"User Agent from response doesn't have key '{name_of_user_agent}'"
        assert response_as_dict[name_of_user_agent] == expected_value, error_message
