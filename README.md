Say we want to generate 200,000,000 Accounts, run following in order:
1. python3 acc_seq_gen.py 200000000
1. shuf acc_seq > acc_shf
1. python3 acc_sfid_graph_gen.py 200000000
1. shuf sub_groups > sub_groups_shf
1. python3 cust_graph_gen.py
