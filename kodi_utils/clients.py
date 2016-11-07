import re
import os
from urllib.parse import urlparse

import requests


FSTO_HOST = 'http://fs.to'


class FsToLink:
    regex_pattern = \
        r'http\:\/\/fs\.to\/video\/(?P<content_type>(films)|(serials))\/view\/(?P<id>[a-zA-Z0-9]+)\?play\&file=(?P<file>\d+)\s*$'
    url_regex = re.compile(regex_pattern)

    def __init__(self, url):
        self.url = url
        if not self.url_is_valid(url):
            raise Exception('Not valid fs.to url: ' + url)
        match  = self.url_regex.match(self.url)
        self.id = match.group('id')
        self.file = match.group('file')
        self.content_type = match.group('content_type')

    def url_is_valid(self, url):
        return self.url_regex.match(url) is not None


class FsToFile:
    def __init__(self, data):
        self.id = data['id']
        self.url = FSTO_HOST + data['url']
        self.hd_url = FSTO_HOST + self.get_hd_url(self.url)
        self.file_name = data['file_name']
        self.quality = data['quality']
        self.language = data['language']

    def get_hd_url(self, url):
        path = urlparse(url).path
        name, ext = os.path.splitext(path)
        return '{name}_hd{ext}'.format(**locals())


class FsToContent:
    '''
    Fs.To response wrapper
    '''
    def __init__(self, data):
        actionsData = data['actionsData']
        files = actionsData['files']
        file = actionsData['file']
        self.files = [FsToFile(f) for f in files]
        try:
            self.file = next(filter(lambda x: x.id == file['id'], self.files))
        except StopIteration:
            raise Exception('No main file found in files collection.', file, files)


class FsToClient:
    '''
    Link in method params should be an instance of FsToLink
    '''
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36',
    }

    def build_url(self, link):
        url = 'http://fs.to/video/{content_type}/view_iframe/{id}?play&isStartRequest=true&file={file}'.format(
            content_type=link.content_type,
            id=link.id,
            file=link.file
        )
        return url

    def load_data(self, link):
        url = self.build_url(link)
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception('Unable to load data from FS.TO', response)
        data = response.json()
        return data

    def get_content(self, url):
        link = FsToLink(url)
        data = self.load_data(link)
        return FsToContent(data)