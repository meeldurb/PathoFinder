#!usr/bin/env python

"""
Author: Melanie van den Bosch
Script for calculating oligo properties
lala
"""

# import statements
from __future__ import division
import math

# functions are below

# probably the input sequence is read as a string  
## class OligoProperties(self):
## i can probably make a class of this one
def count_aminoacids(DNA_seq):
    """Returns a tuple of the number of each amino acid

    Keyword Arguments:
        DNA_seq -- string, a DNA sequence
    """ 
    A = sequence.count("A")
    C = sequence.count("C")
    G = sequence.count("G")
    T = sequence.count("C")
    return A, C, G, T

def molecular_weight(DNA_seq):
    """ Returns the molecular weight in Da of a sequence

    Keyword Arguments:
        DNA_seq -- string, a DNA sequence
    """
    # weight constants for aminoacids
    A_WEIGHT = 313.21
    C_WEIGHT = 289.18
    G_WEIGHT = 329.21
    T_WEIGHT = 304.2
    # counting the aminoacids
    A, C, G, T = count_aminoacids(sequence)
    # calculate total weight of sequence
    # This is the Anhydros Mol Weight as retrieved from 
    # http://biotools.nubic.northwestern.edu/OligoCalc.html
    seq_weight = A * A_WEIGHT + C * C_WEIGHT + G * G_WEIGHT + \
                 T * T_WEIGHT - 61.95
    return seq_weight

def GC_content(DNA_seq):
    """ Returns the GC content in % of a sequence

    Keyword Arguments:
        DNA_seq -- string, a DNA sequence
    """
    # counting the aminoacids
    A, C, G, T = count_aminoacids(sequence)
    # dividing frequency GC by total amino acids    
    GC_percentage = (G+C)/(length(sequence))
    return GC_percentage
    
def length(DNA_seq):
    """ Returns the length in integers of a sequence

    Keyword Arguments:
        DNA_seq -- string, a DNA sequence
    """
    result = len(sequence)
    return result

def melting_temp(DNA_seq, Na_conc=None):
    # needs some work still
    """ Returns the melting temperature(Tm) in float of a DNA sequence

    Keyword Arguments:
        DNA_seq -- string, a DNA sequence
        Na_conc -- float, the concentration of Na+(in mM) in solution
    """
    # counting the aminoacids
    A, C, G, T = count_aminoacids(sequence)
    # separate calculations for each length
    if Na_conc == None:
        if len(sequence) <= 13:
            Tm = (A+T)*2 + (G+C)*4
        else:
            Tm = 64.0 + 41*((G+C - 16.4)/(A+T+G+C))
    if Na_conc != None:
        if len(sequence) <= 13:
            Tm = (A+T)*2 + (G+C)*4 - (16.6*math.log(0.050) + \
                 16.6*math.log(Na_conc, 10))
        if len(sequence) >= 14:
            Tm = 100.5 + (41*(G+C)/(A+T+G+C) - (820/(A+T+G+C) + \
                      16.6*math.log(Na_conc, 10)))
    return Tm



if __name__== "__main__":
    # input DNA sequence
    sequence = "ACTGCCGTAGGCTACCCAGT"
    print "sequence is: ", sequence
    # Run and print functions
    count_seq = count_aminoacids(sequence)
    print "count of A, C, G, T respectively: ", count_seq
    mol_w_seq = molecular_weight(sequence)
    print "molecular weight of sequence: ", mol_w_seq
    length_seq = length(sequence)
    print "length of the sequence: ", length_seq
    GC_seq = GC_content(sequence)
    print "GC content of the sequence: ", GC_seq
    melt_seq_default = melting_temp(sequence)
    print "melting temp of the sequence(default): ", melt_seq_default
    melt_seq_na = melting_temp(sequence, 0.30)
    print "melting temp of the sequence(Na = 0.3 mM): ", melt_seq_na
    
