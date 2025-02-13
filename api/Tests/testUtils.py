import unittest
from unittest.mock import patch
import os
from datetime import datetime

from ..modUtils import log

class TestLogFunction(unittest.TestCase):
    def setUp(self):
        self.test_filename = "./api/Tests/test-python-logs.txt"
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)
    
    def test_log_writes_to_file(self):
        message = "Test log message"
        log(message, filename=self.test_filename)
        
        with open(self.test_filename, "r") as file:
            content = file.read()
        
        self.assertIn(message, content)
        
    @patch('builtins.print')  # Mock the built-in print function
    def test_log_debug_prints_message(self, mock_print):
        # Call the function with a test message
        test_message = "Hello, world!"
        expected_output = f"[{datetime.now()}] {test_message}"
        
        log(test_message, self.test_filename, debug=True)

        # Assert that print was called with the correct message
        mock_print.assert_called_with(expected_output)
    
    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

if __name__ == '__main__':
    unittest.main()