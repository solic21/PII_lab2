import unittest
import csv

import model
import t2_mandani_inference


class TestAll(unittest.TestCase):

    def test_all(self):
        with open('data.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                crisp = list(map(lambda x:float(x), row[:-1]))
                word_expected = row[-1]
                with self.subTest(crisp = crisp, word_expected=word_expected):
                    result, _ = t2_mandani_inference.process(model.input_lvs, model.output_lv, model.rule_base, crisp)
                    self.assertEqual(result[1], word_expected)
