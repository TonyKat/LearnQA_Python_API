import requests

payload = {"login": "secret_login", "password": "secret_pass2"}
response1 = requests.post('https://playground.learnqa.ru/api/get_auth_cookie', data=payload)

cookie_value = response1.cookies.get('auth_cookie')

cookies = {}
if cookie_value is not None:
    cookies.update({'auth_cookie': cookie_value})

response2 = requests.post('https://playground.learnqa.ru/api/check_auth_cookie', cookies=cookies)

print(f'response1.text = {response1.text}')
print(f'response1.status_code = {response1.status_code}')
print(f'dict(response1.cookies) = {dict(response1.cookies)}')

print(f'response2.text = {response2.text}')
print(f'response2.status_code = {response2.status_code}')
print(f'dict(response2.cookies) = {dict(response2.cookies)}')



