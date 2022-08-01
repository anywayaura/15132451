import logging
import os
from urllib.parse import urlparse

import requests

logging.basicConfig(level=logging.INFO)


def shorten_link(url, token):
    headers = {'Authorization': f'Bearer {token}',
               'Content-Type': 'application/json'}
    data = {"long_url": url}
    response = requests.post('https://api-ssl.bitly.com/v4/bitlinks', headers=headers, json=data)
    if response.ok:
        return response.json().get('link')
    else:
        logging.error('shortening link failed')


def get_clicks(url, token):
    headers = {'Authorization': f'Bearer {token}',
               'Content-Type': 'application/json'}
    params = {'unit': 'day',
              'units': '-1'}
    parsed_url = urlparse(url)
    bitlink = f'{parsed_url.netloc}{parsed_url.path}'
    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary',
                            headers=headers,
                            params=params)
    if response.ok:
        return f'Clicks: {response.json().get("total_clicks")}'
    else:
        logging.error('getting clicks on bitlink failed')


def is_bitlink(url, token):
    parsed_url = urlparse(url)
    bitlink = f'{parsed_url.netloc}{parsed_url.path}'
    headers = {'Authorization': f'Bearer {token}',
               'Content-Type': 'application/json'}
    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}', headers=headers)
    if response.ok:
        return True
    else:
        return False


def main():
    TOKEN = os.getenv('BITLY_TOKEN')
    url = input('Please Enter the link: ')
    try:
        if is_bitlink(url, TOKEN):
            print(get_clicks(url, TOKEN))
        else:
            print(shorten_link(url, TOKEN))
    except Exception as ex:
        logging.error(f'error {ex}')


if __name__ == '__main__':
    main()
