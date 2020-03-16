#!/usr/bin/bash
# Script: 	2.ATAC_prepare.sh
# Description:	transform the ATAC bedfile to BigWigfile, which's required
#		by the next step's deeptools-computeMatrix
# Usage:	bash 2.ATAC_prepare.sh <Wig-step> <OUTPUTDIR>
# Update date:	2020/3/16
# Author:	Zhuofan Zhang

ATAC_BDG=${1}
STEP=${2}
OUTDIR=${3}
CELLTYPE=${4}

# Exist File(s)
# ATAC_BDG=/mnt/disk5/zhangzf/raw_data/ATAC-seq/K562_ATAC_peak.sorted.bdg
HG19_CS=/mnt/disk5/zhangzf/raw_data/hg19_info/hg19.chrom.sizes

# Output File(s)
ATAC_BW=${OUTDIR}/${CELLTYPE}_ATAC_peak.sorted.step${STEP}.bw

# Tools and scripts
wigToBigWig=/mnt/disk5/zhangzf/softwares/kentUtils/wigToBigWig
trans_script=/mnt/disk5/zhangzf/scripts/transformation/bedgraph_to_wig.pl

perl -w ${trans_script} ${STEP} ${ATAC_BDG} > tempwig.wig && \
$wigToBigWig tempwig.wig ${HG19_CS} ${ATAC_BW} && \
rm tempwig.wig
