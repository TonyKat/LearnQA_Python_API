import time
import json
import requests


def do_request(url: str, token: str) -> str:
    result = ''
    try:
        if token:
            response = requests.request(url=url, method='GET', params={'token': token})
            result = response.text
        else:
            response = requests.request(url=url, method='GET')
            result = response.text
    except Exception as e:
        print(f'Произошла ошибка при отправке запроса. e = {e}')
    return result


def check_status(result_dict: dict) -> None:
    """Функция, которая выводит на экран статус задачи, в зависимости от status.
    Если задача готова, то будет надпись 'Job is ready'.
    Если задача не готова, то будет надпись 'Job is NOT ready'."""
    if result_dict['status'] == 'Job is ready':
        print(f'Поле status = {result_dict["status"]}')
    elif result_dict['status'] == 'Job is NOT ready':
        print(f'Поле status = {result_dict["status"]}')
    else:
        print('Неизвестный статус')


def check_result(result_dict: dict) -> None:
    """Функция, которая выводит на экран результат задачи, в зависимости от result.
    Если result существует, то будет надпись: 'result существует и равен: {result}'.
    Если result не существует, то будет надпись: 'result не существует'."""

    try:
        print(f'Поле result = {result_dict["result"]}')
    except KeyError as e:
        print(f'{e}: Поля result не существует в данном ответе.')


def ex8():
    url = 'https://playground.learnqa.ru/ajax/api/longtime_job'

    print('1. Создать задачу')
    result_of_creating_task = do_request(url=url, token='')
    time_of_creation_task = time.time()
    result_of_creating_task = json.loads(result_of_creating_task)
    print(f'Результат создания задачи: {result_of_creating_task}')

    print('\n2. Сделать запрос с token ДО того, как задача готова. Убеждаемся в правильности поля status.')
    print(f'(нужно успеть выполнить запрос в течение {result_of_creating_task["seconds"]} секунд)')
    if time.time() - time_of_creation_task < result_of_creating_task['seconds']:
        result_before_finished_task = do_request(url=url, token=result_of_creating_task['token'])
        print(f'Результат выполнения запроса ДО выполнения задачи: {result_before_finished_task}')
        result_before_finished_task = json.loads(result_before_finished_task)
        check_status(result_before_finished_task)
    else:
        print('Не успели сделать запрос до выполнения задачи!')

    print(f'\n3. Ждать секунд: {result_of_creating_task["seconds"]}.')
    time.sleep(result_of_creating_task["seconds"])

    print(f'\n4. Сделать запрос с token={result_of_creating_task["token"]} после выполнения задачи.'
          f'\nУбеждаемся в правильности поля status и наличии поля result.')

    result_after_finished_task = do_request(url=url, token=result_of_creating_task['token'])
    result_after_finished_task = json.loads(result_after_finished_task)
    check_status(result_after_finished_task)
    check_result(result_after_finished_task)


if __name__ == '__main__':
    time_begin = time.time()
    ex8()
    print(f'Время выполнения программы: {time.time() - time_begin}')
