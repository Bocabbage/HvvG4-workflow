#!usr/bin/env python
# -*- coding: utf-8 -*-
# Script:       dataset.py
# Description:  build G4_data_package class and provide interfaces
#               useful for training and testing
# Update date:  2020/5/12
# Author:       Zhuofan Zhang

import pandas as pd
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset


class G4_data_package:
    r'''
        It's a class for easy processing the VG4/UG4 data.
    '''
    def __init__(self, vg4_file, ug4_file):  # , random_state=42):
        r'''
            Initialized the object of G4_data_package, including:
            1.reads the features in csv into dataframes and stores
            2.add labels at the last column of each dataframes

        '''
        self.vg4 = pd.read_csv(vg4_file, dtype='a')
        self.ug4 = pd.read_csv(ug4_file, dtype='a')

        # Add labels
        self.vg4['Label'] = 1
        self.ug4['Label'] = 0

    def get_train_test_set(self,
                           test_size=0.25,
                           random_state=42,
                           shuffle=True):
        r'''
            Get train_test set used random-seed: random_state.
            Noted that the random_state will also be used in
            sampling the negative-samples
        '''

        # Return all the data as the test_set
        if test_size == "train":
            all_dataset = pd.concat([self.vg4, self.ug4], sort=False)
            return all_dataset, None

        # Return all the data as the train_set
        if test_size == "test":
            all_dataset = pd.concat([self.vg4, self.ug4], sort=False)
            return None, all_dataset

        ug4_sample = self.ug4.sample(n=self.vg4.shape[0],
                                     random_state=random_state)
        all_dataset = pd.concat([self.vg4, ug4_sample], sort=False)

        # Return balanced dataset
        if test_size == 0.0:
            return all_dataset, None
        elif test_size == 1.0:
            return None, all_dataset

        return train_test_split(
                                    all_dataset,
                                    test_size=test_size,
                                    random_state=random_state,
                                    shuffle=shuffle
                               )


def test_main():
    vg4_file = input("vg4 file:")
    ug4_file = input("ug4 file:")
    # train_size = int(input("train_set_size:"))
    # test_size = int(input("test_set_size:"))
    dataset_G4 = G4_data_package(vg4_file, ug4_file)
    g4_train, g4_test = dataset_G4.get_train_test_set()

    # g4_train = test_G4.get_training_set(train_size)
    # g4_test = test_G4.get_test_set(test_size)
    print("train size:{0} \t test size:{1}".format(g4_train.shape[0],
                                                   g4_test.shape[0]))
    print("train.head:")
    print(g4_train.head(5))


if __name__ == '__main__':
    test_main()
