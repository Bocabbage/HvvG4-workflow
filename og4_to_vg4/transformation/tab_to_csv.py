#!usr/bin/env python
# -*- coding: utf-8 -*-


import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', help="Input TAB file.")
parser.add_argument('-o', help="Output CSV file.", default="./sample.csv")

args = parser.parse_args()

with open(args.i, 'r') as ifile:
    with open(args.o, 'w+') as ofile:
        for i in range(3):
            ifile.readline()
        for line in ifile.readlines():
            ofile.write(line)