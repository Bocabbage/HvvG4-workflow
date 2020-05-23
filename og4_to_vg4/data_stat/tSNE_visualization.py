#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Update date: 2020/05/23

import argparse
import pandas as pd
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

def twoColorChoose(x):
    if x==1:
        return 'r'
    return 'b'

parser = argparse.ArgumentParser()
parser.add_argument('--vg4', help="input VG4 csv.")
parser.add_argument('--ug4', help="input UG4 csv.")
parser.add_argument('-o', help="output tSNE 2D figs.")
args = parser.parse_args()

vg4 = pd.read_csv(args.vg4, dtype='a')
ug4 = pd.read_csv(args.ug4, dtype='a')
vg4['Label'] = 1
ug4['Label'] = 0
g4 = pd.concat([vg4, ug4])
g4_labels = g4.pop('Label')
g4_labels_color = [twoColorChoose(x) for x in g4_labels]
g4_embedded = TSNE(n_components=2, n_iter=500, random_state=42).fit_transform(g4.fillna(0.0))
del vg4, ug4, g4, g4_labels

fig, ax = plt.subplots(figsize=(10, 10))
ax.scatter(g4_embedded[:, 0], g4_embedded[:, 1], color=g4_labels_color, alpha=0.4)
ax.set_title("t-SNE")
fig.savefig(args.o)