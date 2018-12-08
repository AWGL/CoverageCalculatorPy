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
from CoverageCalculatorPy import get_gaps
from CoverageCalculatorPy import report_missing_regions


class TestCalcCov(unittest.TestCase):

    # test calculation of average depth
    # instance where entire interval as a depth
    def test_avg_depth(self):

        if os.path.exists('./test.coverage'):
            os.remove('./test.coverage')

        filehandel = open("./test.coverage", 'a+')
        depthfile = "test.gz"
        get_avg_depth(filehandel, "1", 115252142, 115252148, "NONE", depthfile, 180)
        filehandel.close()

        with open("./test.coverage") as f:
            for line in f:
                avg_depth = float(line.split("\t")[4])
                perc_coverage = float(line.split("\t")[5])
                self.assertEqual(avg_depth, 901.0)
                self.assertEqual(perc_coverage, 16.7)

    # instance where end of interval does not have depth
    def test_avg_depth_endofinterval(self):

        if os.path.exists('./test.coverage'):
            os.remove('./test.coverage')

        filehandel = open("./test.coverage", 'a+')
        depthfile = "test.gz"
        get_avg_depth(filehandel, "1", 115258827, 115258834, "NONE", depthfile, 180)
        filehandel.close()

        with open("./test.coverage") as f:
            for line in f:
                avg_depth = float(line.split("\t")[4])
                perc_coverage = float(line.split("\t")[5])
                self.assertEqual(avg_depth, 119.0)
                self.assertEqual(perc_coverage, 28.6)

    # instance where start of interval does not have depth
    def test_avg_depth_startofinterval(self):

        if os.path.exists('./test.coverage'):
            os.remove('./test.coverage')

        filehandel = open("./test.coverage", 'a+')
        depthfile = "test.gz"
        get_avg_depth(filehandel, "1", 160786640, 160786649, "NONE", depthfile, 180)
        filehandel.close()

        with open("./test.coverage") as f:
            for line in f:
                avg_depth = float(line.split("\t")[4])
                perc_coverage = float(line.split("\t")[5])
                self.assertEqual(avg_depth, 5455.0)
                self.assertEqual(perc_coverage, 33.3)

    # test calculation of missing
    def test_missing_endofinterval(self):

        if os.path.exists('./test.missing'):
            os.remove('./test.missing')

        filehandel = open("./test.missing", 'a+')
        depthfile = "test.gz"
        report_missing_regions(filehandel, "1", 115258827, 115258834, "NONE", depthfile)
        filehandel.close()

        with open("./test.missing") as f:
            for line in f:
                self.assertEqual(line, "1\t115258830\t115258834\tNONE\n")

    # test calculation of gaps
    def test_gaps(self):

        if os.path.exists('./test.gaps'):
            os.remove('./test.gaps')

        filehandel = open("./test.gaps", 'a+')
        depthfile = "test.gz"
        get_gaps(filehandel, "1", 115252142, 115252155, "NONE", depthfile, 180)
        filehandel.close()

        with open("./test.gaps") as f:
            for line in f:
                self.assertEqual(line, "1\t115252142\t115252147\n")

    # test calculation of gaps
    def test_gaps(self):

        if os.path.exists('./test.gaps'):
            os.remove('./test.gaps')

        filehandel = open("./test.gaps", 'a+')
        depthfile = "test.gz"
        get_gaps(filehandel, "1", 115252142, 115252155, "NONE", depthfile, 4910)
        filehandel.close()

        with open("./test.gaps") as f:
            cnt = 1
            for line in f:
                if cnt == "1":
                    self.assertEqual(line, "1\t115252142\t115252147\n")
                    cnt = cnt + 1
                if cnt == "2":
                    self.assertEqual(line, "1\t115252149\t115252155\n")

if __name__ == '__main__':
    unittest.main()