#!usr/bin/env python
# -*- coding: utf-8 -*-
# Script:       main.py
# Description:  MAIN function of the VG4-predictor
# Update date:  2020/5/12
# Author:       Zhuofan Zhang


from dataset import G4_data_package
from validation_test import ROC_plot, Kfold_cross_validation, Val_Test_Results
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold, cross_val_score
from joblib import dump
import os
import pandas as pd
import numpy as np
import argparse
# Classifier modules
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import normalize
# from imblearn.over_sampling import SMOTE

# Arguments-Parsing
parser = argparse.ArgumentParser()
parser.add_argument('--vg4', help="VG4-ATAC overlapped CSV file.")
parser.add_argument('--ug4', help="UG4-ATAC overlapped CSV file.")
parser.add_argument('--kfroc', default="./KFold_ROC", help="output kfold-validation-ROC curve picture file name.")
parser.add_argument('--testroc', default="./test_ROC", type=str, help="output test-ROC curve picture file name.")
parser.add_argument('--testpr', default=None, help="output test-PR curve picture file name.")
parser.add_argument('--resultdir',default=None, help="output test result-dir.")
parser.add_argument('--seed', default=42, type=int, help="int random-seed.")
parser.add_argument('--kfold', default=5, type=int, help="k of 'KFOLD'.")
parser.add_argument('--test_size', default=0.25, type=float, help="frac of the test size in all dataset.")
parser.add_argument('--mode', default='validation', help="Three mode: validation, train, test")
parser.add_argument('--modeldir',default='./', help="Used with the --mode parameter.")


# Mix features
# parser.add_argument('--newvg4', default="")
# parser.add_argument('--newug4', default="")
# parser.add_argument('--mix', default=0, type=int, help="when positive, the 'newXg4's work.(default:0)")


args = parser.parse_args()

# Parameters
RANDOM_STATE = args.seed
KFOLD = args.kfold
TEST_SIZE = args.test_size




# Hyper-parameters
xgb_params = {
                'seed':RANDOM_STATE,
                'learning_rate':0.2,
                'gamma':0.3,
                'subsample':0.7,
                'colsample_bytree':0.8,
                'n_estimators':1000,
                
              }

svc_params = {
                'random_state':RANDOM_STATE,
                'C':1.0,
                'kernel':'rbf',
                'probability': True
             }

rf_params = {
                'random_state':RANDOM_STATE,
                'n_estimators': 1000,
                'criterion':'gini'
            }

lr_params = {
                'random_state':RANDOM_STATE,
                'penalty':'l2',
                'C':1.0,
                'solver':'liblinear'    
            }

# Classfiers
xgb = XGBClassifier()
svc = SVC()
rf = RandomForestClassifier()
lr = LogisticRegression()

# Set parameters
svc.set_params(**svc_params)
rf.set_params(**rf_params)
lr.set_params(**lr_params)
xgb.set_params(**xgb_params)

Classifiers = {
                'xgboost_classifier':xgb,
                'support vector machine':svc,
                'randomforest':rf,
                'logistic regression':lr
              }

g4_data_package = G4_data_package(args.vg4, args.ug4)

if args.mode == 'validation':
    # Load Data
    train_data, test_data = g4_data_package.get_train_test_set(test_size = TEST_SIZE, random_state=RANDOM_STATE, shuffle=True)
    # train_data = G4_data_package.get_training_set(trainset_size=8000,random_state=RANDOM_STATE)
    # test_data = G4_data_package.get_test_set(testset_size=8000,test_random_state=RANDOM_STATE)
    train_labels = train_data.pop('Label')
    test_labels = test_data.pop('Label')

    kfroc_name = args.kfroc + "_randomstate{}.png".format(RANDOM_STATE)
    fig = plt.figure(1)
    fig.set_size_inches(18.5, 10.5)
    for i, (clf_name, clf) in enumerate(Classifiers.items(), 1):
        ax = fig.add_subplot(2,2,i)
        kfroc_name = args.kfroc + "_{}_randomstate{}.png".format(clf_name, RANDOM_STATE)
        # K-Fold Validation ROC
        ROC_plot(clf, train_data.to_numpy(), train_labels.to_numpy(), ax=ax,  
                 n_splits=KFOLD, clf_name = clf_name)#, res_pic=kfroc_name)
    fig.savefig(kfroc_name,dpi=100)


    testroc_name = args.testroc + "_randomstate{}.png".format(RANDOM_STATE)
    # Output test results
    Val_Test_Results(Classifiers, X=train_data.to_numpy(), y=train_labels.to_numpy(),
                  X_test=test_data.to_numpy(), y_test=test_labels.to_numpy(), res_pic=testroc_name)

elif args.mode == 'train':
    save_files = ['xgb.joblib', 'svc.joblib', 'rf.joblib', 'lr.joblib']
    train_data, _ = g4_data_package.get_train_test_set(test_size = "train", random_state=RANDOM_STATE, shuffle=True)
    train_labels = train_data.pop('Label')
    #train_data_resample, train_labels_resample = SMOTE().fit_resample(train_data.fillna(0.0).to_numpy(), train_labels.to_numpy())
    #print(train_data_resample.shape)
    for i, (clf_name, clf) in enumerate(Classifiers.items()):
        clf.fit(train_data.fillna(0.0).to_numpy(), train_labels.to_numpy())
        #clf.fit(train_data_resample, train_labels_resample)
        dump(clf, os.path.join(args.modeldir, save_files[i]))


elif args.mode == 'test':
    load_files = ['xgb.joblib', 'svc.joblib', 'rf.joblib', 'lr.joblib']
    load_files = [os.path.join(args.modeldir, x) for x in load_files]
    _, test_data = g4_data_package.get_train_test_set(test_size = "test", random_state=RANDOM_STATE, shuffle=True)
    test_labels = test_data.pop('Label')

    testroc_name = args.testroc + "_randomstate{}.png".format(RANDOM_STATE)
    if args.testpr:
        testpr_name = args.testpr + "_randomstate{}.png".format(RANDOM_STATE)
    else:
        testpr_name = None

    Val_Test_Results(Classifiers, X=None, y=None, 
                  X_test=test_data.fillna(0.0).to_numpy(), y_test=test_labels.to_numpy(), 
                  res_pic=testroc_name, res_pr=testpr_name, resultdir=args.resultdir,load_files=load_files)


