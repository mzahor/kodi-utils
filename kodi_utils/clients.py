import re
import requests

class FsToLink():
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


class FsToClient():
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36',
    }

    def build_url(self, fstolink):
        url = 'http://fs.to/video/{content_type}/view_iframe/{id}?play&isStartRequest=true&file={file}'.format(
            content_type=fstolink.content_type,
            id=fstolink.id,
            file=fstolink.file
        )
        return url

    def load_data(self, fstolink):
        url = self.build_url(fstolink)
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception('Unable to load data from FS.TO', response)
        json = response.json()
        return json
