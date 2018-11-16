"""
tests.py

unit tests for coverageCalculator2.py

Aurthor: Christopher Medway
Created: 11th November 2018
Version: 0.0.1
Updated: 11th November 2018
"""

import unittest
import os
from coverageCalculator2 import get_avg_depth

class TestCalcCov(unittest.TestCase):

    def test_avg_depth(self):

        if os.path.exists('./test.coverage'):
            os.remove('./test.coverage')

        filehandel = open("./test.coverage", 'a+')
        depthfile = "180803_NB551319_0005_AH53YYAFXY_17M18299_DepthOfCoverage.gz"
        get_avg_depth(filehandel, "1", 836814, 836900, "NONE", depthfile, 180)
        filehandel.close()

        with open("./test.coverage") as f:
            for line in f:
                if line.startswith("1\t836814\t836900"):
                    avg_depth = float(line.split("\t")[4])
                    self.assertEqual(avg_depth, 174.0)


    def test_perc_coverage(self):

        if os.path.exists('./test.coverage'):
            os.remove('./test.coverage')

        filehandel = open("./test.coverage", 'a+')
        depthfile = "180803_NB551319_0005_AH53YYAFXY_17M18299_DepthOfCoverage.gz"
        get_avg_depth(filehandel, "1", 836814, 836900, "NONE", depthfile, 180)
        filehandel.close()

        with open("./test.coverage") as f:
            for line in f:
                if line.startswith("1\t836814\t836900"):
                    perc_coverage = float(line.split("\t")[5])
                    self.assertEqual(perc_coverage, 82.6)


if __name__ == '__main__':
    unittest.main()