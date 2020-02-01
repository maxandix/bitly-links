import argparse
from bitly_links import shorten_link, count_clicks, InvalidUrl
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("BITLY_TOKEN")


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
