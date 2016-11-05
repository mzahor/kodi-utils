#!/usr/bin/python3
import logging
from flask import Flask, request


logger = logging.getLogger('fsto_dataloader')
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


app = Flask(__name__)


@app.route("/play", methods=['POST'])
def play():

    return


if __name__ == "__main__":
    app.run()
