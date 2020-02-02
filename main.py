import argparse
from bitly_links import shorten_link, count_clicks, InvalidUrl
from dotenv import load_dotenv
import os


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    return parser


def main():
    load_dotenv()
    token = os.getenv("BITLY_TOKEN")
    url = create_parser().parse_args().url

    try:
        if url.startswith('http://bit.ly/'):
            count = count_clicks(token, url)
            print('Количество переходов по ссылке', count)
        else:
            link = shorten_link(token, url)
            print('Битлинк', link)
    except InvalidUrl:
        print('Вы ввели не действительную ссылку. Запустите программу еще раз и введите ссылку правильно.')


if __name__ == '__main__':
    main()
