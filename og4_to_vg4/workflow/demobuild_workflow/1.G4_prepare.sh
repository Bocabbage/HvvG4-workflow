#!usr/bin/bash
# Script: 	1.G4_prepare.sh
# Description:	Remove 'chrM';Remove too-short entries;Extract UG4;
# Usage:	bash 1.G4_prepare.sh ${VG4 file} ${outputdir} ${cutoff}
# Author:	Zhuofan Zhang
# Update date:	2020/3/16

VG4=${1}
OG4=${2}
OUTDIR=${2}
LENGTH=${3}
#OVERLAP=${4}

# Exist Files
# VG4=/mnt/disk5/zhangzf/raw_data/VG4_GSE107690/GSE107690_K562_High_confidence_peaks.bed
# OG4=/mnt/disk5/zhangzf/raw_data/OG4_data/all_G4_union.sort.bed

# Ouput Files of this script
VG4_PRO=${OUTDIR}/VG4_cutoff${LENGTH}.bed
OG4_PRO=${OUTDIR}/OG4_cutoff${LENGTH}.bed
UG4=${OUTDIR}/UG4_cutoff${LENGTH}.bed

# Step 1: Remove 'chrM' entries
grep -v 'chrM' ${VG4} > VG4_temp.bed
grep -v 'chrM' ${OG4} > OG4_temp.bed

# Step2: Remove entries whose lengths are under 'LENGTH'
awk -v cutoff="$LENGTH" '{now_len=($3-$2);}
			 {if(now_len>cutoff){print $0;}}' VG4_temp.bed > ${VG4_PRO} && \
awk -v cutoff="$LENGTH" '{now_len=($3-$2);}
                         {if(now_len>cutoff){print $0;}}' OG4_temp.bed > ${OG4_PRO} && \

rm VG4_temp.bed && rm OG4_temp.bed

# Step 3: Extract the UG4
# Noted that the 'bedtools' needs to be in the ENVS.
bedtools intersect -v -a ${OG4_PRO} -b ${VG4_PRO}  > ${UG4}
