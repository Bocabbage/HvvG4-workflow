#!usr/bin/bash
# Script: 	1.G4_prepare.sh
# Description:	Remove 'chrM';Remove too-short entries;Extract UG4;
# Usage:	bash 1.G4_prepare.sh ${G4-file} ${output-G4-prepared file} ${cutoff} 
# Author:	Zhuofan Zhang
# Update date:	2020/4/8

G4=${1}
G4_PRO=${2}
LENGTH=${3}

# Step 1: Remove 'chrM' entries
grep -v 'chrM' ${G4} > G4_temp.bed && \

# Step2: Remove entries whose lengths are under 'LENGTH'
awk -v cutoff="$LENGTH" '{now_len=($3-$2);}
			 {if(now_len>cutoff){print $0;}}' G4_temp.bed > ${G4_PRO} && \

rm G4_temp.bed

