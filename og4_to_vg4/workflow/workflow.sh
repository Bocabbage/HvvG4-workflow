#!/usr/bin/bash
# Update date: 2020/5/2: G4-BED is provided by the server
#              2020/5/3: Change the call of 2.ATAC_prepare.sh

g4File=$1
atacFile=$2
bsFile=$3
prefix=$4
cutoff=15
UTILS_DIR=$5
TRANSFORM_DIR=$6
FILEDIR=$7
WORKFLOWDIR=$8

# mkdir -p ${FILEDIR}

# 1.G4 file prepared
# bash ${WORKFLOWDIR}/workflow/1.G4_prepare.sh ${g4File} ${FILEDIR}/${prefix}_preG4.bed ${cutoff} && \
awk '{print $1}' ${atacFile} >> chrom.txt_tmp
awk '{print $1}' ${bsFile} >> chrom.txt_tmp
sort chrom.txt_tmp | uniq >> uniq_chrom.txt_tmp
grep -w -f uniq_chrom.txt_tmp ${g4File} > ${FILEDIR}/${prefix}_sub_g4File.bed
awk 'BEGIN{OFS="\t"}{print $1, $2, $3}' ${FILEDIR}/${prefix}_sub_g4File.bed > ${FILEDIR}/${prefix}_sub_default_g4File.bed
rm *.txt_tmp

# 2.ATAC/BS file prepared
bash ${WORKFLOWDIR}/workflow/2.ATAC_prepare.sh ${atacFile} ${FILEDIR}/${prefix}_preATAC.bw ${UTILS_DIR} && \
bash ${WORKFLOWDIR}/workflow/2.ATAC_prepare.sh ${bsFile} ${FILEDIR}/${prefix}_preBS.bw ${UTILS_DIR} && \

# 3.Compute Matrix
# bash ${WORKFLOWDIR}/workflow/3.Matrices_Compute.sh ${FILEDIR}/${prefix}_preG4.bed ${FILEDIR}/${prefix}_preATAC.bw 3000 300 ${FILEDIR}/${prefix}_forplot ${FILEDIR}/${prefix}_matrix.tab && \
bash ${WORKFLOWDIR}/workflow/3.Matrices_Compute.sh ${FILEDIR}/${prefix}_sub_default_g4File.bed ${FILEDIR}/${prefix}_preATAC.bw 3000 300 ${FILEDIR}/${prefix}_atac_forplot ${FILEDIR}/${prefix}_atac_matrix.tab && \
bash ${WORKFLOWDIR}/workflow/3.Matrices_Compute.sh ${FILEDIR}/${prefix}_sub_default_g4File.bed ${FILEDIR}/${prefix}_preBS.bw 3000 300 ${FILEDIR}/${prefix}_bs_forplot ${FILEDIR}/${prefix}_bs_matrix.tab && \

# 4.Transform TAB to CSV
# python ${TRANSFORM_DIR}/tab_to_csv.py -i ${FILEDIR}/${prefix}_matrix.tab -o ${FILEDIR}/${prefix}_matrix.csv
python ${TRANSFORM_DIR}/tab2csv_concat.py --iatac ${FILEDIR}/${prefix}_atac_matrix.tab \
                                          --ibs ${FILEDIR}/${prefix}_bs_matrix.tab \
                                          -o ${FILEDIR}/${prefix}_matrix.csv

# 5.Predict
python ${WORKFLOWDIR}/model/main.py --g4 ${FILEDIR}/${prefix}_matrix.csv --g4bed ${FILEDIR}/${prefix}_sub_g4File.bed \
                                    --output ${FILEDIR}/${prefix}_result.temp.bed --model ${UTILS_DIR}/xgb.joblib
awk 'BEGIN{OFS="\t"}{if($NF==1){$NF="";print $0}}' ${FILEDIR}/${prefix}_result.temp.bed | \
sed 's/:$//g' > ${FILEDIR}/${prefix}_result.bed
mv ${FILEDIR}/${prefix}_result.temp.bed ${FILEDIR}/${prefix}_result.bed

# rm $g4File
rm $atacFile
rm $bsFile