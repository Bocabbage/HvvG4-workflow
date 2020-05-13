#!/usr/bin/bash
G4FILE=$1
REFFILE=$2
OUTDIR=$3

bedtools getfasta -fi ${REFFILE} -bed ${G4FILE} > ${OUTDIR}/temp.G4.fasta && \

python ./quadParse.py --fa ${OUTDIR}/temp.G4.fasta --bed ${G4FILE} --mode cannon -o ${OUTDIR}/g4seq_cannon.bed
python ./quadParse.py --fa ${OUTDIR}/temp.G4.fasta --bed ${G4FILE} --mode longloop -o ${OUTDIR}/g4seq_longloop.bed

rm ${OUTDIR}/temp.G4.fasta