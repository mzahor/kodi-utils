#!/usr/bin/env python3
import os 
import sys
from argparse import ArgumentParser

from kodipydent import Kodi
from kodi_utils.clients import FsToClient


def main():
    parser = ArgumentParser()
    parser.add_argument('--hd', metavar='N', type=bool, default=True, help='Play in HD quality. True by default.')
    parser.add_argument('-d', metavar='N', dest='direct' type=bool, default=False, help='Play direct url. Dont parse.')
    parser.add_argument('url')
    args = parser.parse_args()
    
    file_url = ''

    if (!args.direct):
        client = FsToClient()
        content = client.get_content(args.url)
        file_url = content.file.hd_url if args.hd else content.file.url
    else:
        file_url = args.url
    
    kodi = Kodi('192.168.0.105', username='mzahor', password='takingoverme')
    resp = kodi.Player.Open(item={'file': file_url})
    print(resp)


if __name__ == '__main__':
    main()
