# -*- coding:utf-8 -*-
import argparse
import re
from Bio import SeqIO

parser = argparse.ArgumentParser()
parser.add_argument('--fa',type=str)
parser.add_argument('--bed',type=str)
parser.add_argument('--mode',default="cannon",type=str)
parser.add_argument('-o',type=str)

args = parser.parse_args()

if args.mode == 'cannon':
    posSeqPattern = re.compile(r'([gG]{3,5}\w{1,7}){3}[gG]{3,5}')
    negSeqPattern = re.compile(r'([cC]{3,5}\w{1,7}){3}[cC]{3,5}')
elif args.mode == 'longloop':
    posSeqPattern = re.compile(r'([gG]{3,5}\w{1,12}){3}[gG]{3,5}')
    negSeqPattern = re.compile(r'([cC]{3,5}\w{1,12}){3}[cC]{3,5}')

with open(args.fa, 'r') as faFile:
    with open(args.bed, 'r') as ibedFile:
        with open(args.o, 'w+') as obedFile:
            for record in SeqIO.parse(faFile, 'fasta'):
                bedLine = ibedFile.readline().strip()
                seq = str(record.seq)
                seqStart = int(bedLine.split("\t")[1])
                match_list = []
                for m in posSeqPattern.finditer(seq):
                    start, end = m.span()
                    match_list.append("{},{}".format(start+seqStart, end+seqStart))
                for m in negSeqPattern.finditer(seq):
                    start, end = m.span()
                    match_list.append("{},{}".format(start+seqStart, end+seqStart))
                for site in match_list:
                    bedLine = bedLine + "\t" + site
                bedLine += "\n"
                obedFile.write(bedLine)

