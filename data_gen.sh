#!/usr/bin/env bash

readonly SIZE="$1"
readonly SAMPLE_SIZE=${2:-10000}
set -x

python3 acc_seq_gen.py "${SIZE}"
shuf acc_seq > acc_shf
python3 acc_sfid_graph_gen.py "${SIZE}"
shuf sub_groups > sub_groups_shf
python3 cust_graph_gen.py

cut -d, -f1 acc_vertex | tail -n +2 | shuf | head -"${SAMPLE_SIZE}" > acc_vertex_sample
