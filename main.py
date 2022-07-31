import logging
import os
from urllib.parse import urlparse

import requests

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv('BITLY_TOKEN')


def shorten_link(url, token):
    headers = {'Authorization': f'Bearer {token}',
               'Content-Type': 'application/json'}
    json = {"long_url": url}
    try:
        response = requests.post('https://api-ssl.bitly.com/v4/bitlinks', headers=headers, json=json).json()
        if response.get('message') == 'INVALID_ARG_LONG_URL':
            return response.get('description')
        return response.get('link')
    except Exception as ex:
        logging.error(f'error {ex}')


def get_clicks(bitlink, token):
    headers = {'Authorization': f'Bearer {token}',
               'Content-Type': 'application/json'}
    params = {'unit': 'day',
              'units': '-1'}
    parsed = urlparse(bitlink)
    bitlink = parsed.netloc + parsed.path
    try:
        response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary',
                                headers=headers,
                                params=params).json()
        return f'Clicks: {response.get("total_clicks")}'
    except Exception as ex:
        logging.error(f'error {ex}')


def url_is_bitlink(url):
    parsed = urlparse(url)
    if parsed.netloc == 'bit.ly':
        return True
    else:
        return False


def main(token):
    url = input('Please Enter the link: ')
    if url_is_bitlink(url):
        print(get_clicks(url, token))
    else:
        print(shorten_link(url, token))


if __name__ == '__main__':
    main(TOKEN)
