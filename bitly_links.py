import requests


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
