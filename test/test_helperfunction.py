import unittest
import __init__
from helperfunction import processing_front_data


class TestHelperFunction(unittest.TestCase):


    def test_processing_front_data(self):
        """
        Test processing front data in helperfunction
        :return: ok
        """
        bytestr = "username=mohammad&email=mohammadhoseinajorloo@gmail.com&password=12345678".encode("utf-8")
        guss_result = {"username" : "mohammad", "email" : "mohammadhoseinajorloo@gmail.com", "password" : "12345678"}
        result = processing_front_data(bytestr)
        self.assertEqual(guss_result, result)  # add assertion here


if __name__ == '__main__':
    unittest.main()
