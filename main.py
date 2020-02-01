import argparse
from dotenv import load_dotenv
import os
import requests

load_dotenv()
TOKEN = os.getenv("BITLY_TOKEN")


class InvalidUrl(Exception):
    pass


def shorten_link(token, url):
    headers = {'Authorization': f'Bearer {token}'}
    params = {"long_url": url}
    response = requests.post('https://api-ssl.bitly.com/v4/bitlinks', headers=headers, json=params)
    if response.status_code == 400 and response.json()['message'] == 'INVALID_ARG_LONG_URL':
        raise InvalidUrl()
    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, bitlink):
    url = bitlink.replace('http://', '')
    headers = {'Authorization': f'Bearer {token}'}
    params = {"unit": "day", "units": -1}
    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{url}/clicks/summary', headers=headers,
                            params=params)
    if response.status_code == 404:
        raise InvalidUrl
    response.raise_for_status()

    return response.json()['total_clicks']


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', nargs='?')
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    if not args.url:
        print('Введите ссылку: ', end='')
        url = input().strip()
    else:
        url = args.url

    try:
        if url.startswith('http://bit.ly/'):
            count = count_clicks(TOKEN, url)
            print('Количество переходов по ссылке', count)
        else:
            link = shorten_link(TOKEN, url)
            print('Битлинк', link)
    except InvalidUrl:
        print('Вы ввели не действительную ссылку. Запустите программу еще раз и введите ссылку правильно.')


if __name__ == '__main__':
    main()
