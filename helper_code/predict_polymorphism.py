#!/usr/bin/env python
from sys import argv
from Bio import SeqIO

usage = """
RA, 6/12/2017
predict_polymorphism
V1
=========================================
Defines a basic predictor object:
Given a fasta file, a dataframe of model parameters, and SNP count
Calculate the poisson binomial parameters and report p count
=========================================
USEAGE: predict_polymorphism.py INCLUDE.bed PARAMS.txt PRIV COUNT
"""

def main():
    if len(argv) == 1:
        print usage
        print "No arguements specified.  Exiting!"
        exit(0)

    print "Reading in model parameters from " + argv[2]
    pred = Predictor(argv[2], bool(int(argv[3])))

    print "Calculating parameters for regions in " + argv[1]
    pred.getParams(argv[1])



"""
	Predictor Object:
	Counts mutations in a private file by sequence context
	Class variables:
        - prob (dict, str:float) mapping from context to mutation probability
        - chrom (str) name of chromosome for bed line we are currently reading
        - ref_genome_chr (str) fasta sequence of self.chrom from hg19
        - compliments (dict) maps complimentary bases to each other
        - priv (bool) if true, consider private mutation model; else cosmo
        - params (list of floats) running list of params for poibin dist
		- flank (int) number of flanking bases of sequence context to consider
"""
class Predictor(object):
    def __init__(self, modelfile, priv):
        self.prob = {}
        self.chrom = ''
        self.ref_genome_chr = ''
        self.compliments = {"A":"T", "T":"A", "G":"C", "C":"G"}
        self.priv = priv
        self.params = []
        self.mean = 0

        self.readProb(modelfile) # build self.prob
        self.flank = (len(self.prob.keys()[0])-1)/2

    # initialize self.prob and self.flank from prob file
    def readProb(self, modelfile):
        with open(modelfile, 'r') as m:
            m.next() #skip header
            for line in m:
                self.parserow(line.split('\t'))


    # given a row of a modelfile, add to self.prob
    def parserow(self, row):
        if self.priv:
        	self.prob[row[0]] = sum([float(n) for n in row[4:7]])
        else:
            self.prob[row[0]] = sum([float(n) for n in row[1:4]])

    # calculate parameters for sequence
    def getParams(self, bedfile):
        with open(bedfile, 'r') as b:
            for line in b:
                print line
                row = line.split('\t')
                print row
                if not line.startswith("chr"): # skip comment line
                    continue
                elif row[0][3:] != self.chrom:
                    print row[0]
                    self.switchChrom(row[0][3:])
                self.parseBedLine(row)

    # load new chrom file
    def switchChrom(self, chrom):
        print "Loading new chromosome sequence."
        self.ref_genome_chr = SeqIO.read('/project/voight_datasets/hg19/chr'+chrom+'.fa', "fasta")
        self.chrom = chrom

    # given position, get context
    def get_context(self, pos):
        return str(self.ref_genome_chr.seq)[pos-(self.flank+1):pos+self.flank].upper()

    # given a sequence, return reverse compliment
    def reverse_comp(self, sequence):
        sequence_rc = ''
        for char in sequence:
            sequence_rc = self.compliments[char] + sequence_rc

        return sequence_rc

    # read through a line of a bed file and add parameters for each position
    def parseBedLine(self, row):
        start = int(row[1])
        stop = int(row[2])
        for i in range(start+1, stop+1):
            seq = self.get_context(i)
            if "N" in seq:
                print seq
                continue
            elif seq in self.prob:
                p = self.prob[seq]
                self.params.append(p)
                self.mean += p
            else:
                p = self.prob[self.reverse_comp(seq)]
                self.params.append(p)
                self.mean += p
        print self.mean

if __name__ == '__main__':
    main()