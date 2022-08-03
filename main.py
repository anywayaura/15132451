import logging
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
import argparse

import requests


logging.basicConfig(level=logging.INFO)

def shorten_link(url, token):
    headers = {'Authorization': f'Bearer {token}'}
    long_url = {"long_url": url}
    response = requests.post('https://api-ssl.bitly.com/v4/bitlinks', headers=headers, json=long_url)
    response.raise_for_status()
    return response.json().get('link')


def get_clicks(url, token):
    headers = {'Authorization': f'Bearer {token}'}
    parsed_url = urlparse(url)
    bitlink = f'{parsed_url.netloc}{parsed_url.path}'
    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary',
                            headers=headers)
    response.raise_for_status()
    return response.json().get("total_clicks")


def is_bitlink(url, token):
    parsed_url = urlparse(url)
    bitlink = f'{parsed_url.netloc}{parsed_url.path}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}', headers=headers)
    return response.ok




def main():
    load_dotenv()
    token = os.getenv('BITLY_TOKEN')
    parser = argparse.ArgumentParser(description='Script creates short bitlinks for long urls, and gets clicks on existing bitlinks')
    parser.add_argument('url', help='long url or bitlink')
    url = parser.parse_args().url
    if urlparse(url).netloc:
        try:
            if is_bitlink(url, token):
                print(f'Clicks: {get_clicks(url, token)}')
            else:
                print(f'Bitlink: {shorten_link(url, token)}')
        except ConnectionError as ex:
            logging.error(f'Internet Problems: {ex}')
        except requests.exceptions.HTTPError:
            logging.error(f'What you are looking for cannot be found.')
    else:
        logging.error(f'Bad Link')


if __name__ == '__main__':
    main()
