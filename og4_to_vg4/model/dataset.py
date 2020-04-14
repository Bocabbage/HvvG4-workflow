#!usr/bin/env python
# -*- coding: utf-8 -*-
# Script:       dataset.py
# Description:  build G4_data_package class and provide interfaces
#               useful for training and testing
# Update date:  2020/3/17
# Author:       Zhuofan Zhang 

import pandas as pd
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset


class G4_data_package:
    '''
        It's a class for easy processing the VG4/UG4 data.
    '''
    def __init__(self, vg4_file, ug4_file, nvg4_file, nug4_file, mix): #, random_state=42):
        '''
            Initialized the object of G4_data_package, including:
            1.reads the features in csv into dataframes and stores
            2.add labels at the last column of each dataframes

        '''
        self.vg4 = pd.read_csv(vg4_file,dtype = 'a')
        self.ug4 = pd.read_csv(ug4_file,dtype = 'a')

        if mix > 0:
            self.nvg4 = pd.read_csv(nvg4_file, dtype= 'a')
            self.nug4 = pd.read_csv(nug4_file, dtype= 'a')
            self.vg4 = pd.concat([self.vg4, self.nvg4], axis=1, sort=False)
            self.ug4 = pd.concat([self.ug4, self.nug4], axis=1, sort=False)
        # self.random_state = random_state
        # self.train_set_size = -1

        # Add labels
        self.vg4['Label'] = 1
        self.ug4['Label'] = 0

    def get_train_test_set(self, test_size=0.25, random_state=42, shuffle=True):
        '''
            Get train_test set used random-seed: random_state.
            Noted that the random_state will also be used in sampling the negative-samples
        '''
        ug4_sample = self.ug4.sample(n=self.vg4.shape[0], random_state=random_state)
        all_dataset = pd.concat([self.vg4, ug4_sample], axis=1, sort=False)

        if test_size == 0.0:
            return all_dataset, None
        elif test_size == 1.0:
            return None, all_dataset

        return train_test_split(
                                    all_dataset, 
                                    test_size=test_size, 
                                    random_state=random_state, 
                                    shuffle=True
                               )


    # Old API: not used any more
    # def get_training_set(self, trainset_size, random_state=42, shuffle=True):
    #     '''
    #         Get training-set of 'trainset_size', which includes
    #         same sample_nums of VG4 and UG4. If random_state != self.random_state,
    #         the new one will replaced the former one, recording for 'getting_testing_set'.
    #     '''
    #     self.random_state = random_state
    #     self.train_set_size = trainset_size

    #     if trainset_size//2 > self.vg4.shape[0] or trainset_size//2 > self.ug4.shape[0]:
    #         print("trainset_size too large! Only return None!")
    #         return None

    #     vg4_sample = self.vg4.sample(n=trainset_size//2, random_state=self.random_state)
    #     ug4_sample = self.ug4.sample(n=trainset_size - trainset_size//2, random_state=self.random_state)

    #     training_set = pd.concat([vg4_sample, ug4_sample])
    #     if shuffle:
    #         training_set = training_set.sample(frac=1, random_state=self.random_state)
    #     return training_set


    # Old API: not used any more
    # def get_test_set(self, testset_size, test_random_state=42):
    #     '''
    #         Get test-set of 'testset_size', which samples excluding the 
    #         training-set(this is implemented by using 'self.random_state', which would be
    #         update when using 'get_training_set') using random_state 'test_random_state'.
    #         If there are no enough samples, the function returns 'None'.
    #     '''
    #     if self.train_set_size == -1:
    #         print("You must get the training_set first.")
    #         return None
    #     if (testset_size//2 > (self.vg4.shape[0] - self.train_set_size//2) or
    #         testset_size - testset_size//2 > (self.ug4.shape[0] - self.train_set_size + self.train_set_size//2)):
    #         print("No enough test samples.")
    #         return None
    #     vg4_sample = self.vg4.drop(
    #                                 index=self.vg4.sample(
    #                                 n=self.train_set_size//2,
    #                                 random_state = self.random_state).index
    #                               ).sample(n=testset_size//2, random_state=test_random_state)
    #     ug4_sample = self.ug4.drop(
    #                                 index=self.ug4.sample(
    #                                 n=self.train_set_size - self.train_set_size//2,
    #                                 random_state = self.random_state).index
    #                               ).sample(n=testset_size - testset_size//2, random_state=test_random_state)

    #     return pd.concat([vg4_sample, ug4_sample])

class g4_dataset(Dataset):
    '''
        inherit from torch.utils.data.Dataset .
        input: samples (numpy_ndarray of features)
               labels  (sequential list of labels)
        Noted that the two inputs' length must be consistent.
    '''
    def __init__(self, samples, labels):
        self.samples = samples
        self.labels = labels
    def __getitem__(self, index):
        features = self.samples[index]
        label = self.labels[index]
        return features, label
    def __len__(self):
        return len(self.labels)


def test_main():
    vg4_file = input("vg4 file:")
    ug4_file = input("ug4 file:")
    # train_size = int(input("train_set_size:"))
    # test_size = int(input("test_set_size:"))
    dataset_G4 = G4_data_package(vg4_file, ug4_file)
    g4_train, g4_test = dataset_G4.get_train_test_set()

    # g4_train = test_G4.get_training_set(train_size)
    # g4_test = test_G4.get_test_set(test_size)
    print("train size:{0} \t test size:{1}".format(g4_train.shape[0],g4_test.shape[0]))
    print("train.head:")
    print(g4_train.head(5))

if __name__ == '__main__':
    test_main()


