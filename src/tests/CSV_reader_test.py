import unittest
from csv_reader import CSVReader


class TestCSVReader(unittest.TestCase):
    def setUp(self):
        self.csv = CSVReader()
        self.return_dict = self.csv.read_csv_to_dict('sample.csv')

    def test_read_csv_to_dict_method_returns_a_dict(self):

        self.assertTrue(isinstance(self.return_dict, dict))

    def test_read_csv_to_dict_return_values_are_correct(self):

        pass
