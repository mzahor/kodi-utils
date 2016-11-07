#!/usr/bin/python3
import os 
import sys
from argparse import ArgumentParser

from kodipydent import Kodi
from kodi_utils.clients import FsToClient


def main():
    parser = ArgumentParser()
    parser.add_argument('url')
    args = parser.parse_args()
    url = args.url

    # client = FsToClient()
    # content = client.get_content(url)
    # file_url = content.file.url

    file_url = url
    
    kodi = Kodi('192.168.0.105')
    resp = kodi.Player.Open(item={'file': file_url})
    print(resp)


if __name__ == '__main__':
    main()
