"""
CoverageCalculatorPy.py

Calculates coverage statistics from depth of coverage file

Aurthor: Christopher Medway
Created: 11th November 2018
Version: 0.0.1
Updated: 11th November 2018
"""

import argparse
import tabix
import os
import logging


def get_args():
    """
    uses argparse package to extract command line arguments
    """

    # argparse object
    parser = argparse.ArgumentParser(
        description='accepts a bedfile and GATK depthOfCoverage file and generates coverage metrics')

    parser.add_argument('-B', '--bedfile', help='path to bedfile', required=True)
    parser.add_argument('-D', '--depthfile', help='path to depth file', required=True)
    parser.add_argument('-p', '--padding', help='basepair padding', required=False, default=0)
    parser.add_argument('-d', '--depth', help='coverage threshold', required=False, default=100)
    parser.add_argument('-o', "--outname", help="output file name", required=False, default="output")
    parser.add_argument('-O', '--outdir', help="output file directory", required=False, default="./")
    parser.add_argument('-g', '--groupfile', help="file of annotations to group bed intervals", required=False)

    args = parser.parse_args()
    return args


def main(args):
    """
    main function iterates over intervals in given bedfile
    """

    # setup logger
    logger = logging.getLogger('CoverageCalculatorPy')
    logger.setLevel(logging.WARNING)
    handler = logging.StreamHandler()
    handler.setLevel(logging.WARNING)
    formatter = logging.Formatter(
        '%(levelname)s\t%(asctime)s\t%(name)s\t%(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info('running CoverageCalculatorPy.py...')


    # make output directory if it doesn't exist
    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    # file handel for coverage output file
    covr_outfile = args.outdir + args.outname + ".coverage"
    logger.info('coverage information for each interval in given bedfile will be written to: ' + str(covr_outfile))

    # remove file if exists
    if os.path.exists(covr_outfile):
        os.remove(covr_outfile)

    # open coverage output file & write header
    covfile = open(covr_outfile, 'a+')
    covfile.write(
        "CHR" +
        "\t" +
        "START" +
        "\t" +
        "END" +
        "\t" +
        "META" +
        "\t" +
        "AVG_DEPTH" +
        "\t" +
        "PERC_COVERAGE@" + str(args.depth) + "\n"
    )

    # variables to store running totals of depth / coverage
    # over all intervals in file 
    mem_depth = 0
    mem_meets_depth = 0
    mem_length = 0

    # setup groups / features variables if this file has been included --groupsfile
    if args.groupfile is not None:
        logger.info('group file included: ' + str(args.groupfile))
        # initialise variables to store depth / coverage over feature
        feature = []
        feature_length = 0
        feature_depth = 0
        feature_meets_depth = 0
        last_feature = 0
 	
        # features made into list
        for line in open(args.groupfile):
            feature.append(line.rstrip())
            
        # check bedfile and groups are same length - throw error if different    
        num_ln_grp = len(feature) - 1  # minus one because grp file has a header
        num_ln_bed = sum(1 for line in open(args.bedfile))

        if num_ln_bed != num_ln_grp:
            logger.error('bedfile and groupfile do not have the same number of entries! Groupfile must have a header')

            
    # prepare output file for merged data - this always includes a data for all intervals in .bed
    # but can also include groups if the file is given as an argument
    mrg_outfile = args.outdir + args.outname + ".totalCoverage"
    logger.info('coverage information across all intervals in bedfile will be written to: ' + str(mrg_outfile))

    # remove merged file if exists
    if os.path.exists(mrg_outfile):
        os.remove(mrg_outfile)

    # open coverage output file & write header
    mrgfile = open(mrg_outfile, 'a+')

    mrgfile.write(
        "FEATURE" +
        "\t" +
        "AVG_DEPTH" +
        "\t" +
        "PERC_COVERAGE@" + str(args.depth) + "\n"
    )

   
    # prepare output file for gaps
    # file handel
    gaps_outfile = args.outdir + args.outname + ".gaps"
    logger.info('gaps - intervals not covered at a minimum of ' + str(args.depth) + ' will be written to: ' + str(gaps_outfile))

    # remove file if exists
    if os.path.exists(gaps_outfile):
        os.remove(gaps_outfile)

    # open gaps output file & write header
    gapsfile = open(gaps_outfile, 'a+')
    gapsfile.write("##DEPTH_THRESHOLD=" + str(args.depth) + "\n")

    #prepare missing file outfile
    # file handel
    missing_outfile = args.outdir + args.outname + ".missing"
    logger.info('intervals which do not a corresponding depth in ' + args.depthfile + ' will be written to: ' + str(missing_outfile))

    # is exists, remove file
    if os.path.exists(missing_outfile):
        os.remove(missing_outfile)

    # open gaps output file & write header
    missingfile = open(missing_outfile, 'a+')


    # iterate over each line of the bed file 
    with open(args.bedfile) as bed:

        # counter used to access element of the features list that correpondes
        # to a bedfile entry. Start on element 1 because 0 contains features header
        cnt_bed_ln = 1

        for line in bed:
            bedlist = line.split()
            chr = bedlist[0]
            start = int(bedlist[1])
            end = int(bedlist[2])
            
           # does bedfile contain 4th column of metadata
            if len(bedlist) > 3:
                meta = str(bedlist[3])
            else:
                meta = ""
            
            # function prints coverage for given interval, but also returns stats for aggregation across intervals 
            depth, meets_depth, length = get_avg_depth(covfile, chr, start, end, meta, args.depthfile, int(args.depth))
            
            # storing coverage info across all intervals in given bedfile
            mem_depth = mem_depth + depth
            mem_meets_depth = mem_meets_depth + meets_depth
            mem_length = mem_length + length
            
            # storing coverage info across features if --groupfile argument included 
            if args.groupfile is not None:
                current_feature = feature[cnt_bed_ln]

                if cnt_bed_ln == 1:
                    last_feature = current_feature

                if current_feature != last_feature:
                    mrgfile.write(
                        str(args.outname + '_' + feature[cnt_bed_ln - 1] + '_' + feature[0]) +
                        "\t" +
                        str(round(feature_depth / feature_length, 0)) +
                        "\t" +
                        str(round((feature_meets_depth / feature_length)*100, 1)) + "\n")

                    feature_depth = 0
                    feature_meets_depth = 0
                    feature_length = 0

                feature_depth = feature_depth + depth
                feature_meets_depth = feature_meets_depth + meets_depth
                feature_length = feature_length + length
                last_feature = current_feature
            
            # reports gaps for given feature and appends to gaps file
            get_gaps(gapsfile, chr, start, end, meta, args.depthfile, int(args.depth))
            
            # reports coordinates which are unavilable (i.e in bed but not in depthfile) and appends to file
            report_missing_regions(missingfile, chr, start, end, meta, args.depthfile)

            cnt_bed_ln = cnt_bed_ln + 1

    # if --groups has been used, last interval in bed will always be the end of a feature - so print
    if args.groupfile is not None:
        mrgfile.write(
            str(args.outname + '_' + feature[cnt_bed_ln - 1] + '_' + feature[0]) +
            "\t" +
            str(round(feature_depth / feature_length, 0)) +
            "\t" +
            str(round((feature_meets_depth / feature_length)*100, 1)) + "\n")
    
    # print accumated depth / coverage across entire bedfile
    mrgfile.write(
        args.outname +
        "\t" +
        str(round(mem_depth / mem_length, 0)) +
        "\t" +
        str(round((mem_meets_depth / mem_length) * 100, 1)) + "\n"
    )
    
    covfile.close()
    

    

def get_bed_lines(depthfile, chr, start, end):
    """
    given a genomic interval, extract entries from tabix indexed depth of coverage file
    depth of coverage file is generated using GATK3

    :param depthfile: depth of coverage file generated in GATK3 and manually tabix indexed (see documentation)
    :param chr: chromosome
    :param start: start coordinate 0-based
    :param end: end coordinate 0-based
    :return: records: object containing bed intervals
    """
    tb = tabix.open(depthfile)
    records = tb.query(chr, start, end)
    return records


def get_avg_depth(covfile, chr, start, end, meta, depthfile, depth_threshold):
    """
    function to iterate over interval and calculate average coverage & percent of bases meeting given
    depth threshold
    :param covfile: coverage output filehandle
    :param chr: chromosome
    :param start: start coordinate 0-based
    :param end: end coordinate 0-based
    :param meta: meta information from bedfile 4th column
    :param depthfile: depth of coverage file generated in GATK3 and manually tabix indexed (see documentation)
    :param depth_threshold: minimum depth of coverage for PASS
    """

    # get depthfile entry for interval
    records = get_bed_lines(depthfile, chr, start, end)

    # intialise variables used in forloop
    tot_depth = 0 
    meets_depth = 0  # counts the number of bases meeting min depth requirement
    length = (end - start)

    for record in records:
        depth = int(record[2])
        tot_depth = tot_depth + depth # accumaulated depth
        if depth >= depth_threshold:
            meets_depth = int(meets_depth) + 1
    avg_depth = round(tot_depth / length, 0)
    perc_coverage = round((meets_depth / length) * 100, 1)

    covfile.write(
        str(chr) +
        "\t" +
        str(start) +
        "\t" +
        str(end) +
        "\t" +
        str(meta) +
        "\t" +
        str(avg_depth) +
        "\t" +
        str(perc_coverage) +
        "\n"
    )
    return tot_depth, meets_depth, length


def get_gaps(gapsfile, chr, start, end, meta, depthfile, depth_threshold):
    """
    identifies and prints coordinates, within the given bed interval, that fall below the given
    depth threshold
    """
    # get depthfile entry for interval
    records = get_bed_lines(depthfile, chr, start, end)

    # initialise variables used in loop
    first_entry = 1
    coord = 0
    gap_start = 0

    for record in records:

        coord = int(record[1])
        depth = int(record[2])

        if first_entry == 1:
            gap_start = coord
            first_entry = 0

        if depth >= depth_threshold:
            if coord != gap_start:
                # this is the end of a gap and should be printed
                gapsfile.write(str(chr) + "\t" + str(gap_start - 1) + "\t" + str(coord - 1)+ "\t" + str(meta)+ "\n")
                gap_start = coord + 1
            else:
                # this is not the end of a gap
                gap_start = gap_start + 1

    # if entire interval is missing
    if coord == 0:
        print("")
    # if interval ended on a gap, print final row
    elif coord != gap_start - 1:
        gapsfile.write(str(chr) + "\t" + str(gap_start - 1) + "\t" + str(coord)+ "\t" + str(meta) + "\n")


def report_missing_regions(missingfile, chr, start, end, meta, depthfile):
    """
    identifies and reports coordinates which are given in the bedfile, but are not included
    in the depth of coverage file
    """
    # get depthfile entry for interval
    records = get_bed_lines(depthfile, chr, start, end)

    # initialse variables used in loop
    coords_in_depthfile = []

    for record in records:
        coords_in_depthfile.append(int(record[1]))

    coords_in_bed = list(range(start+1, end+1))
    missing = sorted(list(set(coords_in_bed) - set(coords_in_depthfile)))

    i = 0
    while i < len(missing):
        if i == 0:
            start = missing[i]
        else:
            if missing[i] - 1 != missing[i - 1]:
                missingfile.write(str(chr) + "\t" + str(start - 1) + "\t" + str(missing[i]) + "\t" + str(meta) + "\n")
                start = missing[i] + 1
            elif i + 1 == len(missing):
                missingfile.write(str(chr) + "\t" + str(start - 1) + "\t" + str(missing[i]) + "\t" + str(meta) + "\n")

        i = i + 1


if __name__ == '__main__':
    args = get_args()
    main(args)
