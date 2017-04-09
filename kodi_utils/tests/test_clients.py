import unittest
import json

from unittest.mock import patch

from .sample_fsto_response import sample_fsto_response
from ..clients import FsToLink, FsToClient, FsToContent
from .. import clients


# Can be changed as fs.life server regenerates them (I'm not sure about this)
VALID_FS_LIFE_LINK = 'http://fs.life/video/serials/view/i4ELKIFfC0foVMg0jCV3kdi?play&file=8932523'
INVALID_FS_LIFE_LINK1 = 'http://fs.life/video/serials/view/i4ELKIFfC0foVMg0jCV3kdi'
INVALID_FS_LIFE_LINK2 = 'http://fs.life/video/serials/i4ELKIFfC0foVMg0jCV3kdi'
INVALID_FS_LIFE_LINK3 = 'http://fs.life/video/serials/i4ELKIFfC0foVMg0jCV3kdi'
VALID_FS_TO_URL = 'http://fs.life/video/serials/view_iframe/i4ELKIFfC0foVMg0jCV3kdi?play&isStartRequest=true&file=8932523'


class TestFsToLink(unittest.TestCase):
    def get_link(self):
        client = FsToLink(VALID_FS_LIFE_LINK)
        return client

    def test_ctor_valid(self):
        client = self.get_link()
        self.assertIsNotNone(client)

    def test_ctor_not_valid(self):
        with self.assertRaises(Exception) as cm:
            client = FsToLink(INVALID_FS_LIFE_LINK1)

        with self.assertRaises(Exception) as cm:
            client = FsToLink(INVALID_FS_LIFE_LINK2)

        with self.assertRaises(Exception) as cm:
            client = FsToLink(INVALID_FS_LIFE_LINK3)

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
        self.link = FsToLink(VALID_FS_LIFE_LINK)

    def test_build_url(self):
        url = self.client.build_url(self.link)
        self.assertEqual(url, VALID_FS_TO_URL)

    @patch.object(clients, 'requests')
    def test_load_data(self, requests_mock):
        requests_mock.get.return_value.status_code = 200
        data = self.client.load_data(self.link)
        self.assertIsNotNone(data)

    @patch.object(clients, 'requests')
    def test_load_data_error(self, requests_mock):
        requests_mock.get.return_value.status_code = 404
        with self.assertRaises(Exception) as cm:
            data = self.client.load_data(self.link)

    @patch.object(clients, 'requests')
    def test_get_content(self, requests_mock):
        requests_mock.get.return_value.status_code = 200
        requests_mock.get.return_value.json.return_value = sample_fsto_response
        content = self.client.get_content(VALID_FS_LIFE_LINK)
        self.assertEqual(len(content.files), 3)

    @unittest.skip('api test')
    def test_fsto_api_response(self):
        # this test should fail when fs.life api changes
        data = self.client.load_data(self.link)
        self.assertTrue('actionsData' in data)
        self.assertTrue('file' in data['actionsData'])
        self.assertTrue('files' in data['actionsData'])
        self.assertTrue('file_name' in data['actionsData']['files'][0])
        self.assertTrue('url' in data['actionsData']['files'][0])
        self.assertTrue('languages' in data['actionsData'])
        self.assertTrue('coverData' in data)

    @unittest.skip('dev')
    def test_load_data_pretty(self):
        # use this test to debug fs.life api
        data = self.client.load_data(self.link)
        print(json.dumps(data, sort_keys=True, indent=4))


class TestFsToContent(unittest.TestCase):
    def setUp(self):
        self.content = FsToContent(sample_fsto_response)
    
    def test_files(self):
        self.assertEqual(len(self.content.files), 3)

    def test_files_file(self):
        file1 = self.content.files[0]
        file2 = self.content.files[1]
        
        self.assertEqual(file1.id, '8932523')
        self.assertEqual(file2.id, '8934414')

        self.assertEqual(file1.file_name, 'Aftermath.s01e01.HD1080p.WEB-DL.Rus.Eng.BaibaKo.mkv')
        self.assertEqual(file2.file_name, 'Aftermath.s01e02.HD1080p.WEB-DL.Rus.Eng.BaibaKo.mkv')

        self.assertEqual(file1.url, 'http://fs.life/get/playvideo/1bab2a0ljx4b04hw748lfiahzrci5bh9g15rkg.0.1765758616.974127405.1478358392.mp4')
        self.assertEqual(file2.url, 'http://fs.life/get/playvideo/1bab2a0ljx4b04hw748lwsh5grg8xopqwa5sy8.0.1765758616.974127405.1478358392.mp4')

        self.assertEqual(file1.hd_url, 'http://fs.life/get/playvideo/1bab2a0ljx4b04hw748lfiahzrci5bh9g15rkg.0.1765758616.974127405.1478358392_hd.mp4')
        self.assertEqual(file2.hd_url, 'http://fs.life/get/playvideo/1bab2a0ljx4b04hw748lwsh5grg8xopqwa5sy8.0.1765758616.974127405.1478358392_hd.mp4')
    
    def test_file(self):
        file = self.content.file
        self.assertEqual(file.id, '8932523')
        self.assertEqual(file.file_name, 'Aftermath.s01e01.HD1080p.WEB-DL.Rus.Eng.BaibaKo.mkv')
        self.assertEqual(file.url, 'http://fs.life/get/playvideo/1bab2a0ljx4b04hw748lfiahzrci5bh9g15rkg.0.1765758616.974127405.1478358392.mp4')
        self.assertEqual(file.hd_url, 'http://fs.life/get/playvideo/1bab2a0ljx4b04hw748lfiahzrci5bh9g15rkg.0.1765758616.974127405.1478358392_hd.mp4')

if __name__ == '__main__':
    unittest.main()
