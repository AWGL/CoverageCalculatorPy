# CoverageCalculatorPy

Given i) a tabix indexed per-base 'depth of coverage' file (similar to generated in GATK3) and , ii) a bed file CoverageCalculatorPy will generate four text reports:

 - *.coverage* file containing the mean depth of coverage across each interval in the bedfile, and the percentage of bases which meet a given depth (default is 100x) across each interval.
 - *.totalcoverage* file containing the the same metrics above summerised over all intervals in the given bedfile. Summeries of adittional subsets of the input bedfile can be included using --groups (see below)
 - *.gaps* file contains intervals which do not meet the given depth of coverage threshold
 - *.missing* file contains intervals which do not have a corresponding coordinate in the 'depth of coverage' file, and therefore cannot be evaluated.
 
### Input Arguments

-D/--depthfile  
path to tabix indexed depth-of-coverage file
    
-B/--bedfile  
path to bedfile. Chromosomes must not be prefixed with 'chr'
    
-d/--depth  
  depth threshold for precentage horizontal coverage calculation (default: 100)
    
-o/--outname  
output name to prefix on text reports (default: output)
    
-O/--outdir  
directory to save output files to (default: current)
    
-g/--groupfile  
path to groupfile (see below)


### Tabix indexing a GATK3 DepthOfCoverage file

The 'depth of coverage' file must be tabix indexed. The first three columns of the depthfile must be; chromosome, coordinate and depth. A file generated in GATK3 can be indexed as follows:

```
sed 's/:/\t/g' <GATK depthOfCoverage file> | grep -v 'Locus' | sort -k1,1 -k2,2n | bgzip > <filename.gz>

tabix -b 2 -e 2 -s 1 <filename.gz> 
```
### Adding a groupfile

The groupfile is a way of generating combined metrics across a number of intervals (i.e. combined across all exons in a gene). These metrics will appear in the *.totalcoverage* file. The groupfile must have a header (this will be included in the output), be a single column containing the same number of rows as the bedfile it will be analysed with.
