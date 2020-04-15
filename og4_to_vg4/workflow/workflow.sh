#!/usr/bin/bash
# Update date: 2020/4/11

g4File=$1
atacFile=$2
prefix=$3
cutoff=15
UTILS_DIR=$4
TRANSFORM_DIR=$5
FILEDIR=$6
WORKFLOWDIR=$7

# mkdir -p ${FILEDIR}

# 1.G4 file prepared
bash ${WORKFLOWDIR}/workflow/1.G4_prepare.sh ${g4File} ${FILEDIR}/${prefix}_preG4.bed ${cutoff} && \

# 2.ATAC file prepared
bash ${WORKFLOWDIR}/workflow/2.ATAC_prepare.sh ${atacFile} 10 ${FILEDIR}/${prefix}_preATAC.bw ${UTILS_DIR} ${TRANSFORM_DIR} && \

# 3.Compute Matrix
bash ${WORKFLOWDIR}/workflow/3.Matrices_Compute.sh ${FILEDIR}/${prefix}_preG4.bed ${FILEDIR}/${prefix}_preATAC.bw 3000 300 ${FILEDIR}/${prefix}_forplot ${FILEDIR}/${prefix}_matrix.tab && \

# 4.Transform TAB to CSV
python ${TRANSFORM_DIR}/tab_to_csv.py -i ${FILEDIR}/${prefix}_matrix.tab -o ${FILEDIR}/${prefix}_matrix.csv

# 5.Predict
python ${WORKFLOWDIR}/model/main.py --g4 ${FILEDIR}/${prefix}_matrix.csv --g4bed ${FILEDIR}/${prefix}_preG4.bed \
                                    --output ${FILEDIR}/${prefix}_result.bed --model ${UTILS_DIR}/xgb.joblib

rm $g4File
rm $atacFile