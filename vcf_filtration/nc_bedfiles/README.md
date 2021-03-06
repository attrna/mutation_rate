# Noncoding regions bedfiles

This directory contains bedfiles documenting the regions of the genome included in this analaysis.  They are reformatted versions of nc_regions, given to me by Varun Aggarwala in Spring 2016, and which was the bedfile I used 
with vcftools to filter the variants from the 1,000 genomes vcfs.  These are the regions of the genome which were included in his analysis from Aggarwala and Voight, 2016 in Nature Genetics.  Since then, I've changed by 
formatting conventions to be compatible with the UCSC-endorsed bed file format.  The original file from Aggarwala has been archived to avoid confusion, but the included regions are identical. When filtering the 1,000 genomes or SGDP vcfs with vcftools or bcftools, nc_regions_for_vcftools should be used, since this follows the chromosome naming conventions for those files.
