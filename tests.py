"""
tests.py

unit tests for CoverageCalculatorPy.py

Aurthor: Christopher Medway
Created: 11th November 2018
Version: 0.0.1
Updated: 11th November 2018
"""

import unittest
import os
from CoverageCalculatorPy import get_avg_depth

class TestCalcCov(unittest.TestCase):

    def test_avg_depth(self):

        if os.path.exists('./test.coverage'):
            os.remove('./test.coverage')

        filehandel = open("./test.coverage", 'a+')
        depthfile = "test.gz"
        get_avg_depth(filehandel, "1", 115252142, 115252148, "NONE", depthfile, 180)
        filehandel.close()

        with open("./test.coverage") as f:
            for line in f:
                if line.startswith("1\t115252142\t115252148"):
                    avg_depth = float(line.split("\t")[4])
                    self.assertEqual(avg_depth, 901.0)


    def test_perc_coverage(self):

        if os.path.exists('./test.coverage'):
            os.remove('./test.coverage')

        filehandel = open("./test.coverage", 'a+')
        depthfile = "test.gz"
        get_avg_depth(filehandel, "1", 115252142, 115252148, "NONE", depthfile, 180)
        filehandel.close()

        with open("./test.coverage") as f:
            for line in f:
                if line.startswith("1\t115252142\t115252148"):
                    perc_coverage = float(line.split("\t")[5])
                    self.assertEqual(perc_coverage, 16.7)


if __name__ == '__main__':
    unittest.main()