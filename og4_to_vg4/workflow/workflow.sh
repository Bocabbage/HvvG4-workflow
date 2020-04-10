#!/usr/bin/bash
# Update date: 2020/4/8

g4File=$1
atacFile=$2
cutoff=15
FILEDIR=/mnt/c/Programming/G4/G4_predict_project/webapp/G4site/files
WORKFLOWDIR=/mnt/c/Programming/G4/G4_predict_project/og4_to_vg4

# mkdir -p ${FILEDIR}

# 1.G4 file prepared
bash ${WORKFLOWDIR}/workflow/1.G4_prepare.sh ${g4File} ${FILEDIR}/preG4.bed ${cutoff} && \

# 2.ATAC file prepared
bash ${WORKFLOWDIR}/workflow/2.ATAC_prepare.sh ${atacFile} 10 ${FILEDIR}/preATAC.bw && \

# 3.Compute Matrix
bash ${WORKFLOWDIR}/workflow/3.Matrices_Compute.sh ${FILEDIR}/preG4.bed ${FILEDIR}/preATAC.bw 3000 300 ${FILEDIR}/matrix.tab && \

# 4.Transform TAB to CSV
python ${WORKFLOWDIR}/transformation/tab_to_csv.py -i ${FILEDIR}/matrix.tab -o ${FILEDIR}/matrix.csv

# 5.Predict
python ${WORKFLOWDIR}/model/main.py --g4 ${FILEDIR}/matrix.csv --g4bed ${FILEDIR}/preG4.bed \
                                    --output ${FILEDIR}/result.bed