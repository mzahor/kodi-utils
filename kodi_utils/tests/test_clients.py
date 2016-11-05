import unittest
import json
from ..clients import FsToLink, FsToClient
from . import sample_fsto_response

# Can be changed as fs.to server regenerates them (I'm not sure about this)
VALID_FS_TO_LINK = 'http://fs.to/video/serials/view/i4ELKIFfC0foVMg0jCV3kdi?play&file=8932523'
INVALID_FS_TO_LINK1 = 'http://fs.to/video/serials/view/i4ELKIFfC0foVMg0jCV3kdi'
INVALID_FS_TO_LINK2 = 'http://fs.to/video/serials/i4ELKIFfC0foVMg0jCV3kdi'
INVALID_FS_TO_LINK3 = 'http://fs.to/video/serials/i4ELKIFfC0foVMg0jCV3kdi'
VALID_FS_TO_URL = 'http://fs.to/video/serials/view_iframe/i4ELKIFfC0foVMg0jCV3kdi?play&isStartRequest=true&file=8932523'

class TestFsToLink(unittest.TestCase):
    def get_link(self):
        client = FsToLink(VALID_FS_TO_LINK)
        return client

    def test_ctor_valid(self):
        client = self.get_link()
        self.assertIsNotNone(client)

    def test_ctor_not_valid(self):
        with self.assertRaises(Exception) as cm:
            client = FsToLink(INVALID_FS_TO_LINK1)

        with self.assertRaises(Exception) as cm:
            client = FsToLink(INVALID_FS_TO_LINK2)

        with self.assertRaises(Exception) as cm:
            client = FsToLink(INVALID_FS_TO_LINK3)

    def test_id(self):
        client = self.get_link()
        self.assertEqual(client.id, 'i4ELKIFfC0foVMg0jCV3kdi')

    def test_file(self):
        client = self.get_link()
        self.assertEqual(client.file, '8932523')

    def test_content_type(self):
        client = self.get_link()
        self.assertEqual(client.content_type, 'serials')


class TestFsToClient(unittest.TestCase):
    def setUp(self):
        self.client = FsToClient()
        self.link = FsToLink(VALID_FS_TO_LINK)

    def test_build_url(self):
        url = self.client.build_url(self.link)
        self.assertEqual(url, VALID_FS_TO_URL)

    def test_load_data(self):
        data = self.client.load_data(self.link)
        self.assertIsNotNone(data)

    def test_fsto_response(self):
        # this test should fail when fs.to api changes
        data = self.client.load_data(self.link)
        self.assertTrue('actionsData' in data)
        self.assertTrue('file' in data['actionsData'])
        self.assertTrue('files' in data['actionsData'])
        self.assertTrue('file_name' in data['actionsData']['files'][0])
        self.assertTrue('url' in data['actionsData']['files'][0])
        self.assertTrue('languages' in data['actionsData'])
        self.assertTrue('coverData' in data)

    @unittest.skip("dev")
    def test_load_data_pretty(self):
        # use this test to debug fs.to api
        data = self.client.load_data(self.link)
        print(json.dumps(data, sort_keys=True, indent=4))


class TestFsToContent(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
