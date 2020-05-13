#! /usr/env/bin python
#-*- coding:utf-8 -*-
# Dirty and work

import argparse
import matplotlib.pyplot as plt
parser = argparse.ArgumentParser()
parser.add_argument('-i')
parser.add_argument('-o')
args = parser.parse_args()

len_stat = [0 for i in range(11)]

with open(args.i, 'r') as ifile:
    with open(args.o, 'w+') as ofile:
        iline = ifile.readline()
        while iline:
            iline.strip()
            token = iline.split('\t')
            if token[4] != '-1':
                lstart, lend = [int(x) for x in token[1:3]]
                rstart, rend = [int(x) for x in token[4:6]]
                rmid = rstart + (rend - rstart + 1) // 2
                if rmid <= lstart:
                    len_stat[6 + int((lstart - rmid + 1)/(rend - rstart + 1) * 10)]+=1
                else:
                    if (rmid - lstart + 1) > (rend - rstart + 1) // 2:
                        len_stat[0]+=1
                    else:
                        if(5 - int((rmid - lstart + 1)/(rend - rstart + 1) * 10) < 0):
                            print(5 - int((rmid - lstart + 1)/(rend - rstart + 1) * 10))
                        len_stat[5 - int((rmid - lstart + 1)/(rend - rstart + 1) * 10)]+=1
            iline = ifile.readline()
        fig, ax = plt.subplots(figsize=(20,10))
        x = range(len(len_stat))
        rects = ax.bar(x, len_stat)
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()*0.5, 1.01*height, "{}".format(height),ha='center',va='bottom')
        labels = ["Notin","(-0.5,-0.4]","(-0.4,-0.3]","(-0.3,-0.2]","(-0.2,-0.1]","(-0.1,0]","(0,0.1]","(0.1,0.2]","(0.2,0.3]","(0.3,0.4]","(0.4,0.5]"]
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_xlabel("Rate")
        ax.set_ylabel("Numbers")
        fig.savefig(args.o)
