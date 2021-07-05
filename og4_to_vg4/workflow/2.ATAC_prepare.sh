#!/usr/bin/bash
# Script: 	2.ATAC_prepare.sh
# Description:	transform the ATAC bedfile to BigWigfile, which's required
#		        by the next step's deeptools-computeMatrix
# Usage:	bash 2.ATAC_prepare.sh <ATAC-BED-file> <Wig-step> <OUTPUTDIR>
# Update date:	2020/5/3(use bedGraphToBigWig to replace the script written by myself)
# Author:	Zhuofan Zhang

ATAC_BDG=${1}
#STEP=${2}
#OUTDIR=${3}
OUTPUT=${2}
UTILS_DIR=${3}
# TMPSPACE=${4}

# Exist File(s)
# ATAC_BDG=/mnt/disk5/zhangzf/raw_data/ATAC-seq/K562_ATAC_peak.sorted.bdg
# HG19_CS=/mnt/disk5/zhangzf/raw_data/hg19_info/hg19.chrom.sizes
HG19_CS=${UTILS_DIR}/hg19.chrom.sizes

# Output File(s)
# ATAC_BW=${OUTDIR}/${CELLTYPE}_ATAC_peak.sorted.step${STEP}.bw

# Tools and scripts
# wigToBigWig=/mnt/disk5/zhangzf/softwares/kentUtils/wigToBigWig
# trans_script=/mnt/disk5/zhangzf/scripts/transformation/bedgraph_to_wig.pl
# wigToBigWig=${UTILS_DIR}/wigToBigWig
# trans_script=${TRANSFORM_DIR}/bedgraph_to_wig.pl
bedGraphToBigWig=${UTILS_DIR}/bedGraphToBigWig

sort -k1,1 -k2,2n ${ATAC_BDG} -T /mnt/disk8/zhangzf/ > atac.sorted.bed
awk -f ${UTILS_DIR}/atac.dedup.awk atac.sorted.bed > atac.sorted.dedup.bed
$bedGraphToBigWig atac.sorted.dedup.bed ${HG19_CS} ${OUTPUT}
# perl -w ${trans_script} ${STEP} atac.sorted.bed > tempwig.wig && \
# $wigToBigWig tempwig.wig ${HG19_CS} ${OUTPUT} && \
# rm tempwig.wig
rm atac.sorted.bed
rm atac.sorted.dedup.bed
