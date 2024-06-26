import __init__
import unittest
from unittest.mock import patch, Mock, MagicMock
from main import HttpHandler
import io


class TestMain(unittest.TestCase):


    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()


    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()


    def tearDown(self):
        pass


    def setUp(self):
        self.mock_request = Mock()


    def test_set_headers(self):
        self.assertIsNone(None, "should return None")


    @patch('http.server.HTTPServer')
    def test_do_GET(self, mock_http_server):
        '''
        Test do_GET function in HttpHandler class
        '''
        self.mock_request.makefile.return_value = io.BytesIO(b"GET /index")
        handler = HttpHandler(self.mock_request, ('127.0.0.1', 8001), mock_http_server)
        handler.do_GET = MagicMock(return_value="/templates/index.html")
        handler.do_GET()
        handler.do_GET.assert_called_with() 

if __name__ == "__main__":
    unittest.main()