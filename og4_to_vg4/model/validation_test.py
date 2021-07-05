#!usr/bin/env python
# -*- coding: utf-8 -*-
# Script:       validation_test.py
# Description:  wrap the different validation and test-result visualization
# Update date:  2020/5/8 (Add Precision-Recall Curve)
# Author:       Zhuofan Zhang

from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import accuracy_score, recall_score, precision_score
from scipy import interp
# Noted that 'plot_roc_curve' needs sklearn version >= 0.22
from sklearn.metrics import auc, plot_roc_curve, plot_precision_recall_curve
import joblib
import numpy as np
import matplotlib.pyplot as plt 
import os


def __Kfold_mean_score(clf, X, y, cv):
    return np.mean(cross_val_score(clf, X, y, cv=cv))


def Kfold_cross_validation(clf, X, y, 
                           nsplits=5, random_state=42, shuffle=True):
    '''
        get the kfold_mean_score of which k=nsplits.
    '''
    kf = KFold(n_splits=nsplits, random_state=random_state, shuffle=shuffle)
    return __Kfold_mean_score(clf, X, y, kf)


def ROC_plot(clf, X, y, ax, clf_name,
             n_splits=5, random_state=42, shuffle=True):  # res_pic,
    '''
        get roc curve saved in res_pic.
        return:
            AUC list, TPR list
    '''
    tprs = []
    aucs = []
    mean_fpr = np.linspace(0, 1, 100)
    # fig, ax = plt.subplots()

    kf = KFold(n_splits=n_splits, random_state=random_state, shuffle=shuffle)
    for i, (train, test) in enumerate(kf.split(X, y)):
        clf.fit(X[train], y[train])
        y_pred = clf.predict(X[test])
        acc = accuracy_score(y[test], y_pred)
        recall = recall_score(y[test], y_pred)
        precision = precision_score(y[test], y_pred)
        viz = plot_roc_curve(
                             clf, X[test], y[test],
                             name=("ROC fold {}: ACC={:3f},"
                                   "REC={:3f},PRE={:3f}").format(
                                       i, acc, recall, precision),
                             alpha=0.3, lw=1, ax=ax
                            )
        interp_tpr = interp(mean_fpr, viz.fpr, viz.tpr)
        interp_tpr[0] = 0.0
        tprs.append(interp_tpr)
        aucs.append(viz.roc_auc)

    ax.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',
            label='Chance', alpha=0.8)

    mean_tpr = np.mean(tprs, axis=0)
    mean_tpr[-1] = 1.0
    mean_auc = auc(mean_fpr, mean_tpr)
    std_auc = np.std(aucs)
    ax.plot(mean_fpr, mean_tpr, color='b', 
            label=r'Mean ROC (AUC = %0.2f $ \pm$ %0.2f)' % (mean_auc, std_auc),
            lw=2, alpha=0.8)

    std_tpr = np.std(tprs, axis=0)
    tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
    tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
    ax.fill_between(mean_fpr, tprs_lower, tprs_upper, 
                    color='grey', alpha=0.2,
                    label=r"$\pm$ 1 std. dev.")

    ax.set(xlim=[-0.05, 1.05], ylim=[-0.05, 1.05],
           title="Receiver operating characteristic curve:{}".format(clf_name))
    ax.legend(loc="lower right")
    # fig.savefig(res_pic)

    return aucs, tprs


def Val_Test_Results(clf_dict, X, y, X_test, y_test,
                     res_pic, res_pr, resultdir, load_files=None):
    # mean_fpr = np.linspace(0, 1, 100)
    fig, ax = plt.subplots(figsize=(10, 10))
    fig2, ax2 = plt.subplots(figsize=(10, 10))
    # print(X_test.shape)
    for i, (clf_name, clf) in enumerate(clf_dict.items()):
        if X is None and y is None:
            clf = joblib.load(load_files[i])
        else:
            clf.fit(X, y)
        y_pred = clf.predict(X_test)

        if resultdir:
            y_pred_proba = clf.predict_proba(X_test)
            with open(
                os.path.join(
                    resultdir,
                    "{}_y_pred.txt".format(clf_name)), 'w+') as ypredfile:
                for Y in y_pred:
                    ypredfile.write("{}\n".format(Y))

            with open(
                os.path.join(
                    resultdir,
                    "{}_y_test.txt".format(clf_name)), 'w+') as ytestfile:
                for Y in y_test:
                    ytestfile.write("{}\n".format(Y))

            with open(
                os.path.join(
                    resultdir,
                    "{}_y_pred_proba.txt".format(clf_name)),
                    'w+') as ypredprobafile:
                for Y in y_pred_proba:
                    ypredprobafile.write("{}\t{}\n".format(Y[0], Y[1]))

        recall = recall_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        acc = accuracy_score(y_test, y_pred)

        # if res_pr:
        #     viz = plot_precision_recall_curve(clf, X_test, y_test, ax=ax)

        # viz = plot_roc_curve(
        #     clf, X_test, y_test,
        #     name=("{}: ACC={:.3f},RECALL={:.3f},PRE={:3f}"
        #           "").format(clf_name, acc, recall, precision),
        #     alpha=0.6, lw=1, ax=ax2)

    if res_pr:
        ax.plot([0, 1], [0, 1], linestyle='--', lw=2,
                color='r', label='Chance', alpha=0.8)
        ax.set(xlim=[-0.05, 1.05], ylim=[-0.05, 1.05],
               title="Precision-Recall Curve")
        ax.legend(loc="lower right")
        fig.savefig(res_pr) 

    ax2.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',
             label='Chance', alpha=0.8)
    ax2.set(xlim=[-0.05, 1.05], ylim=[-0.05, 1.05],
            title="Receiver operating characteristic curve(Test-set)")
    ax2.legend(loc="lower right")
    fig2.savefig(res_pic)