#!/usr/bin/python3
import logging
from flask import Flask, request
from kodi_utils.clients import FsToClient
from kodipydent import Kodi

logger = logging.getLogger('fsto_dataloader')
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
app = Flask(__name__)

@app.route('/player', methods=['POST'])
def play():
    params = request.get_json()
    url = params['url']
    client = FsToClient()
    content = client.get_content(url)
    file_url = content.file.hd_url
    kodi = Kodi('192.168.0.105')
    resp = kodi.Player.Open(item={'file': file_url})


if __name__ == '__main__':
    app.run()
