# CoverageCalculatorPy
Calculated coverage metrics from a GATK3 Depth Of Coverage file and a bedfile  

#### Tabix indexing a GATK3 DepthOfCoverage file

```
sed 's/:/\t/g' <GATK depthOfCoverage file> | grep -v 'Locus' | sort -k1,1 -k2,2n | bgzip > <filename.gz>

tabix -b 2 -e 2 -s 1 <filename.gz> 
```

--groupfile must have header
