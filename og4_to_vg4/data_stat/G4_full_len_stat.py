# -*- coding:utf-8 -*-
# Update date: 2019/12/13

import matplotlib.pyplot as plt

G4_files = [
            "/mnt/disk5/zhangzf/raw_data/VG4_GSE107690/"
            "GSE107690_K562_High_confidence_peaks.bed",

            "/mnt/disk5/zhangzf/raw_data/OG4_data/all_G4_union.bed"
            ]

# G4_file_categories = ["VG4", "OG4"]
G4_stat_save_dirs = ["/mnt/disk5/zhangzf/data_stat/VG4stat.png",
                     "/mnt/disk5/zhangzf/data_stat/OG4stat.png"]

for idx, G4_file in enumerate(G4_files):
    # G4_category = G4_file_categories[idx]
    length_stat = [0 for i in range(61)]    # from 0 to 6000, step = 100
    with open(G4_file, 'r') as ofile:
        line = ofile.readline()
        while line:
            _, start, end = line.split('\t')
            # save to hundred digits
            length_stat[round(abs(int(end)-int(start)), -2)//100] += 1
            line = ofile.readline()

        # print(length_stat)
        plt.figure(idx)
        plt.bar(range(len(length_stat)), length_stat)
        plt.xlabel("Length(100bp)")
        plt.ylabel("Numbers")
        plt.savefig(G4_stat_save_dirs[idx])
