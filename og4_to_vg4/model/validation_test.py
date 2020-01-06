#!usr/bin/env python
# -*- coding: utf-8 -*-
# Script:       validation_test.py
# Description:  wrap the different validation and test-result visualization
# Update date:  2019/12/30
# Author:       Zhuofan Zhang

from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import accuracy_score
from scipy import interp
# Noted that 'plot_roc_curve' needs sklearn version >= 0.22
from sklearn.metrics import auc, plot_roc_curve
import numpy as np
import matplotlib.pyplot as plt 



def __Kfold_mean_score(clf, X, y, cv):
    return np.mean(cross_val_score(clf, X, y, cv=cv))

def Kfold_cross_validation(clf, X, y, nsplits=5, random_state=42, shuffle=True):
    '''
        get the kfold_mean_score of which k=nsplits.
    '''
    kf = KFold(n_splits=n_splits, random_state=random_state, shuffle=shuffle)
    return __Kfold_mean_score(clf, X, y, kf)

def ROC_plot(clf, X, y, ax, clf_name, n_splits=5, random_state=42, shuffle=True):#  res_pic,
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
        acc = accuracy_score(y[test], clf.predict(X[test]))
        viz = plot_roc_curve(
                             clf, X[test], y[test],
                             name="ROC fold {}: ACC={}".format(i, acc),
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

def ROC_test_plot(clf_dict, X, y, X_test, y_test, res_pic):
    mean_fpr = np.linspace(0, 1, 100)
    fig, ax = plt.subplots()

    for (clf_name, clf) in clf_dict.items():
        clf.fit(X, y)
        acc = accuracy_score(y_test, clf.predict(X_test))
        viz = plot_roc_curve(
                               clf, X, y,
                               name="{}: ACC={}".format(clf_name, acc),
                               alpha=0.6, lw=1, ax=ax
                            )

    ax.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',
            label='Chance', alpha=0.8)

    ax.set(xlim=[-0.05, 1.05], ylim=[-0.05, 1.05],
           title="Receiver operating characteristic curve(Test-set)")
    ax.legend(loc="lower right")
    fig.savefig(res_pic)