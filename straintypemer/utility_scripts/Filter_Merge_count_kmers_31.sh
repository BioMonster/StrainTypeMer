#!/usr/bin/env bash

########################################################################################################################
#
# This script takes paired fastq files as input runs:
#
# cutadapt - for trimming adapters
# prinseq - to remove and trim bad quality sequence
# merge_pair script
# jellyfish
#
# $1 fastq_1.gz
# $2 fastq_2.gz
# $3 kmer_length (for jellyfish) [default = 31]
source /home/ksimmon/.bashrc

fastq_1=${1##*/} #get the filename without dir
fastq_2=${2##*/}


suffix=${5}

base_file_name="${5}"
echo "Prefix: ${base_file_name}"
echo "file 1: ${1}"
echo "file 2: ${2}"
echo "kmer size: ${3}"
echo "parent taxid: ${4}"   #ACINETO == 5 // STAPH == 4
echo "file_base:  ${5}"


kmer_length=$3

cutadapt="/home/ksimmon/anaconda/bin/cutadapt"
prinseq="perl /home/ksimmon/bin/prinseq-lite-0.20.4/prinseq-lite.pl"
jellyfish="/home/ksimmon/bin/jellyfish-2.2.0/bin/jellyfish"
concat_fastq="python /home/ksimmon/bin/Taxonomer/utilities/concatenate_fastqs_2.0.py"
kraken="/home/ksimmon/bin/kraken/kraken"

PATH="/home/ksimmon/bin/jellyfish-1.1.11/bin/:$PATH"

#### VARIBLES ###########################################################
ADAPTER="AGATCGGAAGAGC"

##SETUP##
#source /home/ksimmon/.bashrc

preprocessed_dir="${PWD}/${base_file_name}_processed_jellyfish_31/"
##cutadapt
mkdir ${preprocessed_dir}
log_file="${preprocessed_dir}${base_file_name}.log"
log_file_time="${preprocessed_dir}${base_file_name}_time"
#
#
#format6
file_1_trimmed="${preprocessed_dir}${base_file_name}_trimmed_1.fq"
file_2_trimmed="${preprocessed_dir}${base_file_name}_trimmed_2.fq"
#
#
echo "trimming adapters"
/usr/bin/time -v -o "${log_file_time}_cutadapt.txt" ${cutadapt} -a ${ADAPTER} -A ${ADAPTER} -o ${file_1_trimmed} \
-p ${file_2_trimmed} ${1} ${2} --minimum-length 1 >> ${log_file} 2>&1


#
######### PRINSEQ ###################
file_clean_base="${preprocessed_dir}${base_file_name}_preprocessed"
file_failed_base="${preprocessed_dir}${base_file_name}_failed"
file_clean_1="${preprocessed_dir}${base_file_name}_preprocessed_1.fasta"
file_clean_2="${preprocessed_dir}${base_file_name}_preprocessed_2.fasta"
file_clean_1_s="${preprocessed_dir}${base_file_name}_preprocessed_1_singletons.fasta"
file_clean_2_s="${preprocessed_dir}${base_file_name}_preprocessed_2_singletons.fasta"

file_concat="${preprocessed_dir}${base_file_name}_preprocessed_1_2.fasta"
file_concat_all="${preprocessed_dir}${base_file_name}_preprocessed_all.fasta"

echo "quality filtering reads"
prinseq_params=" -out_format 1 -line_width 0 -derep 1 -min_len 30 -ns_max_p 2 -lc_method dust -lc_threshold 10 "
prinseq_params=" -trim_tail_left 3 -trim_tail_right 3 -trim_qual_left 20 -trim_qual_right 20 ":${prinseq_params}

/usr/bin/time -v -o "${log_file_time}_prinseq.txt" $prinseq -fastq ${file_1_trimmed} -fastq2 ${file_2_trimmed} \
 -out_good ${file_clean_base} -out_bad ${file_failed_base} ${prinseq_params} >> ${log_file} 2>&1
#
###add singletons to files
#concatenate duplicates

/usr/bin/time -v -o "${log_file_time}_catenate_fastqs.txt" $concat_fastq -1 ${file_clean_1} -2 ${file_clean_2} \
 -o ${file_concat} -f fa

echo "combining reads"
/usr/bin/time -v -o "${log_file_time}_cat.txt" cat ${file_concat} ${file_clean_1_s} \
 ${file_clean_2_s} > ${file_concat_all}


##ADD KRAKEN PREPROCESSING
kraken_db=" --db /home/ksimmon/reference/strian_typing_resources/kraken_strain_typing/ "

kraken_options=" --threads 3 --fasta-input --preload "

echo "identifying plasmid and genomic sequences "
/usr/bin/time -v -o "${log_file_time}_kraken.txt" $kraken ${kraken_db} ${kraken_options} \
 ${file_concat_all} > "${preprocessed_dir}${base_file_name}_kraken_raw.txt"

plasmid_fasta="${preprocessed_dir}${base_file_name}_plasmid_sequence.fa"
genomic_fasta="${preprocessed_dir}${base_file_name}_genome_sequence.fa"

echo "sequestering reads"
/usr/bin/time -v -o "${log_file_time}_get_genomic_reads.txt" \
python "/home/ksimmon/PycharmProjects/strain_typing/Strain_typing/utility_scripts/extract_reads.py" \
    --kraken_input "${preprocessed_dir}${base_file_name}_kraken_raw.txt" \
    --fasta_file "${file_concat_all}" \
    --taxonomy_file "/home/ksimmon/reference/strian_typing_resources/kraken_strain_typing/taxonomy/nodes.dmp" \
    --parent_taxid ${4} > "${genomic_fasta}" &

/usr/bin/time -v -o "${log_file_time}_get_plasmid_reads.txt" \
 python "/home/ksimmon/PycharmProjects/strain_typing/Strain_typing/utility_scripts/extract_reads.py" \
    --kraken_input "${preprocessed_dir}${base_file_name}_kraken_raw.txt" \
    --fasta_file "${file_concat_all}" \
    --taxonomy_file "/home/ksimmon/reference/strian_typing_resources/kraken_strain_typing/taxonomy/nodes.dmp" \
    --parent_taxid 6 > "${plasmid_fasta}" 2>&1 &
wait

echo "counting kmers"
jellyfish_out="${preprocessed_dir}${base_file_name}_all_jellyfish_${3}.jf"

echo "$jellyfish count -m ${3} -L 2 -t 6 -o ${jellyfish_out} -s 4G -C ${file_concat_all}"
/usr/bin/time -v -o "${log_file_time}_jf_all.txt" $jellyfish count -m ${3} -L 2 -t 10 -o ${jellyfish_out} \
    -s 4G -C ${file_concat_all} >> ${log_file} 2>&1

jellyfish_plasmid_out="${preprocessed_dir}${base_file_name}_plasmid_jellyfish_${3}.jf"
#echo "$$f"
/usr/bin/time -v -o "${log_file_time}_jf_plasmid.txt" $jellyfish count -m ${3} -L 2 -t 10 \
    -o ${jellyfish_plasmid_out} -s 4G -C ${plasmid_fasta} >> ${log_file} 2>&1

jellyfish_genome_out="${preprocessed_dir}${base_file_name}_genome_jellyfish_${3}.jf"
echo "$jellyfish count - m ${3} -L 2 -t 3 -o ${jellyfish_genome_out} -s 4G -C ${genomic_fasta}"
/usr/bin/time -v -o "${log_file_time}_jf_genome.txt" $jellyfish count -m ${3} -L 2 -t 10 \
  -o ${jellyfish_genome_out} -s 4G -C ${genomic_fasta} >> ${log_file} 2>&1

echo "cleaning up larger files"
rm "${file_1_trimmed}" "${file_2_trimmed}" "${file_concat}" "${file_clean_1}" "${file_clean_2}" "${file_clean_1_s}"
rm "${file_clean_2_s}" "${file_failed_base}_1.fasta" "${file_failed_base}_2.fasta"


echo "done ${base_file_name}"
