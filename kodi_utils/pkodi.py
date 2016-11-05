#!/usr/bin/python3
import requests
import argparse
import re
import logging
from urllib.parse import urlparse, urljoin, urlencode, ParseResult


logger = logging.getLogger('fsto_dataloader')
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    args = parser.parse_args()

    fs_id = get_fs_id(args.url)
    data = get_fs_data(fs_id, 8938363)

    files = data['actionsData']['files']

    for file in files:
        print(file['file_name'])
        print(file['url'])

main()
