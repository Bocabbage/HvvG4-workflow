#!usr/bin/env python
# -*- coding: utf-8 -*-
# Script:       main.py
# Description:  MAIN function of the VG4-predictor
# Update date:  2020/4/11
# Author:       Zhuofan Zhang


from xgboost import XGBClassifier
import matplotlib.pyplot as plt
import joblib
import os
import pandas as pd
import numpy as np
import argparse
# Classifier modules
# from sklearn.svm import SVC

# Arguments-Parsing
parser = argparse.ArgumentParser()
parser.add_argument('--g4', help="G4-ATAC overlapped CSV file.")
parser.add_argument('--g4bed', help="G4 BED file.")
parser.add_argument('--seed', default=42, type=int, help="int random-seed.")
parser.add_argument('--output', help="Output file name.")
parser.add_argument('--model',default='/mnt/c/Programming/G4/G4_predict_project/og4_to_vg4/utils/svc.joblib', help="Used with the --mode parameter.")

args = parser.parse_args()

# Parameters
RANDOM_STATE = args.seed

# Set models
xgb_params = {
                'seed':RANDOM_STATE,
                'learning_rate':0.2,
                'gamma':0.3,
                'subsample':0.7,
                'colsample_bytree':0.8,
                'n_estimators':1000
              }

clf = XGBClassifier()
clf.set_params(**xgb_params)
clf = joblib.load(args.model)
# svc_params = {
#                 'random_state':RANDOM_STATE,
#                 'C':1.0,
#                 'kernel':'rbf',
#              }
# clf = SVC()
# clf.set_params(**svc_params)
# clf = joblib.load(args.model)


# Read G4-ATAC data
g4Data = np.genfromtxt(args.g4, delimiter=',')

# Predict
results = clf.predict(g4Data)

with open(args.g4bed, 'r') as rfile:
    with open(args.output, 'w+') as wfile:
        for i, line in enumerate(rfile.readlines()):
            line = line.rstrip() + "\t{}\n".format(results[i])
            wfile.write(line)





