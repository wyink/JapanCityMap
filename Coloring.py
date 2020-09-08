import sys
import re

def cases_data_read(infile):
    for l in open(infile,"r",encoding='UTF-8'):
        l = l.rstrip()
        