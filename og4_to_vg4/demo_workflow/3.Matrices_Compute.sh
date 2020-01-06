#!/usr/bin/bash
# Script:	3.Matrices_compute.sh
# Description:	use deeptools to compute ATAC-G4 overlap matrices.
# Usage:	bash 3.Matrices_compute.sh <VG4.bed> <UG4.bed> <ATAC.bw> <ablength> <binSize> <OUTDIR>
# Update date:	2019/12/24
# Author:	Zhuofan Zhang
# TOOLS REQ:	deeptools(Added to ENVS)

VG4=$1
UG4=$2
ATAC=$3
EXTEND=$4
BINSIZE=$5
OUTDIR=$6

# ComputeMatrix
computeMatrix reference-point -S ${ATAC} -R ${VG4} -p 10 \
	      --referencePoint "center" \
	      -a ${EXTEND} -b ${EXTEND} -bs ${BINSIZE} \
	      --outFileName ${OUTDIR}/VG4_extend${EXTEND}_BS${BINSIZE}_forplot \
	      --outFileNameMatrix ${OUTDIR}/VG4_extend${EXTEND}_BS${BINSIZE}.tab

computeMatrix reference-point -S ${ATAC} -R ${UG4} -p 10 \
	      --referencePoint "center" \
	      -a ${EXTEND} -b ${EXTEND} -bs ${BINSIZE} \
	      --outFileName ${OUTDIR}/UG4_extend${EXTEND}_BS${BINSIZE}_forplot \
	      --outFileNameMatrix ${OUTDIR}/UG4_extend${EXTEND}_BS${BINSIZE}.tab

# PlotProfile
plotProfile -m ${OUTDIR}/VG4_extend${EXTEND}_BS${BINSIZE}_forplot \
	    -o ${OUTDIR}/VG4_extend${EXTEND}_BS${BINSIZE}.png \
	    --refPointLabel "G4-center" \
	    --yMin 0 --yMax 15

plotProfile -m ${OUTDIR}/UG4_extend${EXTEND}_BS${BINSIZE}_forplot \
	    -o ${OUTDIR}/UG4_extend${EXTEND}_BS${BINSIZE}.png \
	    --refPointLabel "G4-center" \
	    --yMin 0 --yMax 15


