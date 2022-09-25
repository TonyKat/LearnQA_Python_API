import requests

url = 'https://playground.learnqa.ru/api/long_redirect'
response = requests.get(url)

print(f'От изначальной до итоговой точки назначения происходит редиктов в количестве: {len(response.history)}')
print(f'Итоговый URL: {response.url}')
