import logging
import os
from urllib.parse import urlparse

import requests

TOKEN = os.getenv('BITLY_TOKEN')
logging.basicConfig(level=logging.INFO)

def shorten_link(url, token):
    headers = {'Authorization': f'Bearer {token}'}
    long_url = {"long_url": url}
    response = requests.post('https://api-ssl.bitly.com/v4/bitlinks', headers=headers, json=long_url)
    if response.ok:
        return response.json().get('link')
    else:
        logging.error('shortening link failed. ')
        return


def get_clicks(url, token):
    headers = {'Authorization': f'Bearer {token}'}
    parsed_url = urlparse(url)
    bitlink = f'{parsed_url.netloc}{parsed_url.path}'
    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary',
                            headers=headers)
    if response.ok:
        return response.json().get("total_clicks")
    else:
        logging.error('getting clicks on bitlink failed')
        return


def is_bitlink(url, token):
    parsed_url = urlparse(url)
    bitlink = f'{parsed_url.netloc}{parsed_url.path}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}', headers=headers)
    return response.ok


def main(token):
    url = input('Please Enter the link: ')
    if urlparse(url).netloc:
        try:
            if is_bitlink(url, token):
                print(f'Clicks: {get_clicks(url, token)}')
            else:
                print(f'Bitlink: {shorten_link(url, token)}')
        except ConnectionError as ex:
            logging.error(f'Internet Problems: {ex}')

    else:
        logging.error(f'Bad Link')



if __name__ == '__main__':
    main(TOKEN)
