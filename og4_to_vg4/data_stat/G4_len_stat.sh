#!/bin/bash
# Update date: 2019/12/13
OG4=$1
VG4=$2
# OG4=/mnt/disk5/zhangzf/raw_data/OG4_data/all_G4_union.bed
# VG4=/mnt/disk5/zhangzf/raw_data/VG4_GSE107690/GSE107690_K562_High_confidence_peaks.bed
FILES=($OG4 $VG4)

for file in ${FILES[@]}
do
	echo -e "$file"
	echo -e "Ave_len\tMax_len\tMin_len"
	eval $(awk 'BEGIN{OFS="\t";min_len=50000} 	
		    {now_len=($3-$2);} 
		    {if(now_len<=min_len){min_len=now_len;}} 
		    {if(now_len>=max_len){max_len=now_len;}} 
		    {nums+=1;total_len+=now_len;} 
		    END{print "MAX_LEN="max_len,";MIN_LEN="min_len,";AVE_LEN="total_len/nums";";}' $file)
	echo -e "${AVE_LEN}\t${MAX_LEN}\t${MIN_LEN}"
	# Beacuse the 'awk' can only support 2-Bytes long int,
	# so I can't just take the line-numbers to seek the seq.
	# Thus, I extract the longest/shortest entries scanning another time.
	awk -v max_len=${MAX_LEN} -v min_len=${MIN_LEN} \
	    '{if($3-$2==max_len){print "Longest entry:"$0;}}
	     {if($3-$2==min_len){print "Shortest entry:"$0;}}
	    ' $file | sort
	echo -e "\n"
done
