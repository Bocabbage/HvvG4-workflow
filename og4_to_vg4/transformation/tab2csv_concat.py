#! usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--iatac', help="Input ATAC-tab file.")
parser.add_argument('--ibs', help="Input BS-tab file.")
parser.add_argument('-o', help="Output CSV file.", default="./sample.csv")

args = parser.parse_args()

with open(args.iatac, 'r') as iatacFile:
    with open(args.ibs, 'r') as ibsFile:
        with open(args.o, 'w+') as ofile:
            for i in range(3):
                iatacFile.readline()
                ibsFile.readline()
            header = ''
            for i in range(1, 41):
                header += "\"V{}\",".format(i)
            header =  header[:-1] + "\n"
            ofile.write(header)

            for atacLine in iatacFile.readlines():
                bsLine = ibsFile.readline()
                Line = atacLine.strip().replace("nan", "0.0").replace("\t", ",") + \
                    ',' + bsLine.strip().replace("nan", "0.0").replace("\t", ",") + "\n"
                ofile.write(Line)