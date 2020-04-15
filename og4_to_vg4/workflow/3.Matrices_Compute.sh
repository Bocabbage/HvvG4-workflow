#!/usr/bin/bash
# Script:	3.Matrices_compute.sh
# Description:	use deeptools to compute ATAC-G4 overlap matrices.
# Usage:	bash 3.Matrices_compute.sh <G4.bed> <ATAC.bw> <ablength> <binSize> <OUTDIR>
# Update date:	2020/4/8
# Author:	Zhuofan Zhang
# TOOLS REQ:	deeptools(Added to ENVS)

G4=$1
ATAC=$2
EXTEND=$3
BINSIZE=$4
OUTFORPLOT=$5
OUTPUT=$6

# ComputeMatrix
computeMatrix reference-point -S ${ATAC} -R ${G4} -p 6 \
	      --referencePoint "center" \
	      -a ${EXTEND} -b ${EXTEND} -bs ${BINSIZE} \
	      --outFileName ${OUTFORPLOT} \
	      --outFileNameMatrix ${OUTPUT}



