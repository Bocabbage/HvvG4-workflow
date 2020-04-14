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
        header = ''
        for i in range(1,21):
            header += "\"V{}\",".format(i)
        header =  header[:-1] + "\n"
        ofile.write(header)

        for line in ifile.readlines():
            line = line.replace("nan", "0.0")
            line = line.replace("\t", ",")
            ofile.write(line)
