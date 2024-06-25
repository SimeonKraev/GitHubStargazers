import unittest
import main
import sys

class TestMainURL(unittest.TestCase):
    def test_url_starless(self):
        test_url = "https://github.com/SimeonKraev/UnInspired"
        sys.argv = ['main.py', test_url, True]

        with self.assertRaises(Exception) as context:
            main.main()
        
        # Assert that the exception message is "No stars"
        self.assertEqual(str(context.exception), "No stars")
    
    #TODO Add more tests

if __name__ == '__main__':
    unittest.main()