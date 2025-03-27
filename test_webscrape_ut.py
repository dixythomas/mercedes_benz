import unittest
from unittest import mock
from web_scraper import Web_users

class web_code_ut(unittest.TestCase):
    @mock.patch('requests.get')
    def test_is_return_code(self, m_req):
        #mocking the requests librar
        m_req.return_value = mock.MagicMock(status_code=500)
        win = Web_users('https://lol.in')
        ret = win.get_url()
        self.assertFalse(ret)

    @mock.patch('requests.get')
    def test_is_json(self, m_req):
        m_req.return_value = mock.MagicMock(status_code=200)
        win = Web_users('https://lol.in')
        ret = win.get_url()
        self.assertTrue(ret)

    @mock.patch('requests.get')
    def test_print_data_fail(self, m_req):
        m_req.return_value = mock.MagicMock(status_code=200, json=lambda:{"id": "test"})
        win = Web_users('https://lol.in')
        win.get_url()
        ret = win.print_data(param='data')
        self.assertFalse(ret)

    @mock.patch('requests.get')
    def test_print_data_true(self, m_req):
        m_req.return_value = mock.MagicMock(status_code=200, json=lambda:{"data":[{"first_name":"George","last_name":"Bluth"},{"first_name":"Janet","last_name":"Weaver"}]})
        win = Web_users('https://lol.in')
        win.get_url()
        ret = win.print_data(param='data')
        self.assertTrue(ret)

    @mock.patch('os.path.isdir')
    @mock.patch('shutil.rmtree')
    @mock.patch('os.mkdir')
    @mock.patch('requests.get')
    @mock.patch('shutil.copyfileobj')
    @mock.patch('fpdf.FPDF.image')
    @mock.patch('fpdf.FPDF.output')
    def test_create_file_success(self,m_out,m_image,m_copy,m_req,m_dir,m_shutil,m_isdir):
        m_req.return_value = mock.MagicMock(status_code=200, json=lambda:{"data":[{"first_name":"George","last_name":"Bluth","email":"Bluth@gmail.com","avatar":"https://reqr.in/img/laces/6-image.jpg"}]})
        m_isdir.return_value = True
        m_shutil.return_value = True
        m_dir.return_value = 'pdf_document'
        m_copy.return_value = True
        m_image.return_value = True
        m_out.return_value = 'new_file.pdf'
        win = Web_users('https://lol.in')
        win.get_url()
        win.print_data(param='data')
        ret = win.create_file()
        self.assertTrue(ret)

    @mock.patch('os.path.isdir')
    @mock.patch('shutil.rmtree')
    @mock.patch('os.mkdir')
    @mock.patch('requests.get')
    @mock.patch('shutil.copyfileobj')
    @mock.patch('fpdf.FPDF.image')
    def test_create_file_dir_fail(self,m_image,m_copy,m_req,m_dir,m_shutil,m_isdir):
        m_req.return_value = mock.MagicMock(status_code=200, json=lambda:{"data":[{"first_name":"George","last_name":"Bluth","email":"Bluth@gmail.com","avatar":"https://req.in/img/aces/6-image.jpg"}]})
        m_isdir.return_value = True
        m_shutil.return_value = True
        m_dir.side_effect = OSError
        m_copy.return_value = True
        m_image.return_value = True
        win = Web_users('https://lol.in')
        win.get_url()
        win.print_data(param='data')
        ret = win.create_file()
        self.assertFalse(ret)

    @mock.patch('os.path.isdir')
    @mock.patch('shutil.rmtree')
    @mock.patch('os.mkdir')
    @mock.patch('requests.get')
    @mock.patch('shutil.copyfileobj')
    def test_create_file_status_code_fail(self,m_copy,m_req,m_dir,m_shutil,m_isdir):
        m_req.return_value = mock.MagicMock(status_code=200, json=lambda:{"data":[{"first_name":"George","last_name":"Bluth","email":"Bluth@gmail.com","avatar":"https://re.in/img/aces/6-image.jpg"}]})
        m_isdir.return_value = True
        m_shutil.return_value = True
        m_dir.side_effect = OSError
        m_copy.return_value = True
        win = Web_users('https://lol.in')
        win.get_url()
        win.print_data(param='data')
        m_req.return_value = mock.MagicMock(status_code=100, json=lambda:{"data":[{"first_name":"George","last_name":"Bluth","email":"Bluth@gmail.com","avatar":"https://re.in/img/ces/6-image.jpg"}]})
        ret = win.create_file()
        self.assertFalse(ret)

    @mock.patch('os.path.isdir')
    @mock.patch('fpdf.FPDF.add_page')
    def test_create_pdf_fail(self,m_pdf,m_isdir):
        m_isdir.return_value = False
        m_pdf.side_effect = RuntimeError
        win = Web_users('https://lol.in')
        ret = win.create_file()
        self.assertFalse(ret)

    @mock.patch('web_scraper.Web_users.get_url')
    def test_main_url_fail(self, m_url):
        m_url.return_value = False
        win = Web_users('https://lol.in')
        ret = win.main()
        self.assertEqual(ret,1)

    @mock.patch('web_scraper.Web_users.get_url')
    @mock.patch('web_scraper.Web_users.print_data')
    def test_main_print_fail(self,m_data, m_url):
        m_url.return_value = True
        m_data.return_value =False
        win = Web_users('https://lol.in')
        ret = win.main()
        self.assertEqual(ret,1)

    @mock.patch('web_scraper.Web_users.get_url')
    @mock.patch('web_scraper.Web_users.print_data')
    @mock.patch('web_scraper.Web_users.create_file')
    def test_main_create_file_fail(self,m_create,m_data, m_url):
        m_url.return_value = True
        m_data.return_value =True
        m_create.return_value = False
        win = Web_users('https://lol.in')
        ret = win.main()
        self.assertEqual(ret,1)

    @mock.patch('web_scraper.Web_users.get_url')
    @mock.patch('web_scraper.Web_users.print_data')
    @mock.patch('web_scraper.Web_users.create_file')
    def test_main_success(self,m_create, m_data, m_url):
        m_url.return_value = True
        m_data.return_value = True
        m_create.return_value = True
        win = Web_users('https://lol.in')
        ret = win.main()
        self.assertEqual(ret,0)

if __name__ == '__main__':
    unittest.main()
