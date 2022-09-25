from requests import Response


class BaseCase:

    @staticmethod
    def get_cookie(response: Response, cookie_name):
        assert cookie_name in response.cookies, f'Cannot find cookie with name {cookie_name} in the last response'
        return response.cookies[cookie_name]
