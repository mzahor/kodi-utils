#!/usr/bin/python3
import logging
import configparser
from flask import Flask, request, jsonify
from kodi_utils.clients import FsToClient
from kodipydent import Kodi

logger = logging.getLogger('fsto_dataloader')
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

config = configparser.ConfigParser()
config.read('settings.ini')
auth = config['auth']
connection = config['connection']

app = Flask(__name__)

@app.route('/player', methods=['POST'])
def play():
    params = request.get_json()
    url = params['url']
    client = FsToClient()
    content = client.get_content(url)
    file_url = content.file.hd_url
    kodi = Kodi(connection['server'], username=auth['username'], password=auth['password'])
    resp = kodi.Player.Open(item={'file': file_url})


@app.route('/', methods=['GET'])
@app.route('/health', methods=['GET'])
def health():
    return jsonify(status='running')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
