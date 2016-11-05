#!/usr/bin/python3
import requests
import argparse
from urllib.parse import urlparse, urljoin, urlencode, ParseResult
import re


def get_fs_id(url):
    match = re.search(r'video/\w+/([a-zA-Z0-9]+)\-', url)
    fs_id = match.group(1)
    return fs_id


def build_url(fs_id, folder_id=None):
    url = urljoin('http://fs.to/video/serials/view_iframe/', fs_id)
    url_builder = urlparse(url)
    query = {'isStartRequest': 'true'}

    if folder_id:
        query['file'] = str(folder_id)

    result = ParseResult(
        url_builder.scheme, url_builder.netloc, url_builder.path,
        url_builder.params, urlencode(query), url_builder.fragment
    ).geturl()

    return result


def get_fs_data(fs_id, folder_id=None):
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36',
    }

    url = build_url(fs_id, folder_id)

    resp = requests.get(url, headers=headers)
    print(resp)
    json = resp.json()
    return json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    args = parser.parse_args()

    fs_id = get_fs_id(args.url)
    data = get_fs_data(fs_id, 880836)

    print(data)

main()
