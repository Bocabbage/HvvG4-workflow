#!/usr/bin/bash
# Script: 	2.ATAC_prepare.sh
# Description:	transform the ATAC bedfile to BigWigfile, which's required
#		by the next step's deeptools-computeMatrix
# Usage:	bash 2.ATAC_prepare.sh <ATAC-BED-file> <Wig-step> <OUTPUTDIR>
# Update date:	2020/4/10
# Author:	Zhuofan Zhang

ATAC_BDG=${1}
STEP=${2}
#OUTDIR=${3}
OUTPUT=${3}
# CELLTYPE=${4}

# Exist File(s)
# ATAC_BDG=/mnt/disk5/zhangzf/raw_data/ATAC-seq/K562_ATAC_peak.sorted.bdg
# HG19_CS=/mnt/disk5/zhangzf/raw_data/hg19_info/hg19.chrom.sizes
HG19_CS=/mnt/c/Programming/G4/G4_predict_project/og4_to_vg4/utils/hg19.chrom.sizes

# Output File(s)
# ATAC_BW=${OUTDIR}/${CELLTYPE}_ATAC_peak.sorted.step${STEP}.bw

# Tools and scripts
# wigToBigWig=/mnt/disk5/zhangzf/softwares/kentUtils/wigToBigWig
# trans_script=/mnt/disk5/zhangzf/scripts/transformation/bedgraph_to_wig.pl
wigToBigWig=/mnt/c/Programming/G4/G4_predict_project/og4_to_vg4/utils/wigToBigWig
trans_script=/mnt/c/Programming/G4/G4_predict_project/og4_to_vg4/transformation/bedgraph_to_wig.pl

sort -k1,1 -k2,2n ${ATAC_BDG} > atac.sorted.bed
perl -w ${trans_script} ${STEP} atac.sorted.bed > tempwig.wig && \
$wigToBigWig tempwig.wig ${HG19_CS} ${OUTPUT} && \
rm tempwig.wig
rm atac.sorted.bed
