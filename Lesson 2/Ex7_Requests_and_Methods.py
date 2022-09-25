import time
import requests
from functools import wraps



def func_of_marking(func):
    """
    Декоратор, который печатает начало и конец выполнения функции.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f'------------------{func.__name__}. BEGIN----------------------\n')
        result = func(*args, **kwargs)
        print(f'------------------{func.__name__}. END ----------------------\n')
        return result

    return wrapper


def do_request(url: str, types_requests: list) -> dict:
    result = {}
    try:
        for type_request in types_requests:
            response = requests.request(url=url, method=type_request)
            result.update({type_request: {'Response': response.text,
                                          'Status Code': response.status_code}})
    except Exception as e:
        print(f'Произошла ошибка при отправке запроса. e = {e}')
    return result


def print_result(result_dict: dict) -> None:
    for key, value in result_dict.items():
        print(f'{key}:')
        for k, v in value.items():
            print(f'"{k}": {v}')
        print()


def print_result_of_task4_ex7(result_dict: dict) -> None:
    """
    Функция, которая выводит на экран содержимое словаря для task4_ex7.

    Пример словаря:
    {
        type_request:
            {
                new_type_request:
                    {
                        'Response': response.text,
                        'Status Code': response.status_code,
                        'params["method"]': new_type_request,
                        'bug': True or False
                    }
            }
    }
    """
    for type_request, new_type_request in result_dict.items():
        for key, value in new_type_request.items():
            print(f'{type_request}. Значение параметра method: {key}')
            for k, v in value.items():
                print(f'"{k}": {v}')
            print()
        print()


@func_of_marking
def task1_ex7(url: str, types_requests: list) -> None:
    print('1. Делает http-запрос любого типа без параметра method, описать что будет выводиться в этом случае.')
    result = do_request(url, types_requests)
    print_result(result)


@func_of_marking
def task2_ex7(url: str, types_requests: list) -> None:
    print('2. Делает http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае.')
    result = do_request(url, types_requests)
    print_result(result)


@func_of_marking
def task3_ex7(url: str, types_requests: list) -> None:
    print('3. Делает запрос с правильным значением method. Описать что будет выводиться в этом случае.')
    result = {}
    for type_request in types_requests:
        if type_request != 'GET':
            response = requests.request(url=url, method=type_request, data={'method': type_request})
            result.update({type_request: {'Response': response.text,
                                          'Status Code': response.status_code}})
        else:
            response = requests.request(url=url, method=type_request, params={'method': type_request})
            result.update({type_request: {'Response': response.text,
                                          'Status Code': response.status_code}})

    print_result(result)


@func_of_marking
def task4_ex7(url: str, types_requests: list) -> None:
    print('4. С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method.\n'
          'Например с GET-запросом передает значения параметра method равное ‘GET’, затем ‘POST’, ‘PUT’, ‘DELETE’\n'
          'и так далее. И так для всех типов запроса. Найти такое сочетание, когда реальный тип запроса не совпадает\n'
          'со значением параметра, но сервер отвечает так, словно все ок. Или же наоборот, когда типы совпадают,\n'
          'но сервер считает, что это не так.\n')
    result = {}
    for type_request in types_requests:
        for new_type_request in types_requests:
            result.update(
                {
                    type_request:
                        {
                            new_type_request: {}
                        }
                }
            )

    # types_requests = ['POST', 'GET', 'PUT', 'DELETE']
    for type_request in types_requests:
        for new_type_request in types_requests:
            if type_request != 'GET':
                response = requests.request(url=url, method=type_request, data={'method': new_type_request})
                result[type_request].update(
                    {
                        new_type_request: {'Response': response.text,
                                           'Status Code': response.status_code,
                                           'data["method"]': new_type_request,
                                           'bug': True if type_request != new_type_request and
                                           response.status_code == 200 and
                                           response.text not in 'Wrong method provided'
                                           else False}
                    }
                )

            else:
                response = requests.request(url=url, method=type_request, params={'method': new_type_request})
                result[type_request].update(
                    {
                        new_type_request: {'Response': response.text,
                                           'Status Code': response.status_code,
                                           'params["method"]': new_type_request,
                                           'bug': True if type_request != new_type_request and
                                           response.status_code == 200 and
                                           response.text not in 'Wrong method provided'
                                           else False}
                    }
                )

    print_result_of_task4_ex7(result)


@func_of_marking
def ex7():
    url = 'https://playground.learnqa.ru/ajax/api/compare_query_type'

    types_requests = ['POST', 'GET', 'PUT', 'DELETE']
    task1_ex7(url, types_requests)

    other_types_requests = ['HEAD', 'OPTIONS', 'PATCH', 'TRACE', 'CONNECT']
    task2_ex7(url, other_types_requests)

    task3_ex7(url, types_requests)

    task4_ex7(url, types_requests)


if __name__ == '__main__':
    time_begin = time.time()
    ex7()
    print(f'Время выполнения программы: {time.time() - time_begin}')
