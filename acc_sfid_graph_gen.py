from time import time
import random
import sys

###########

def new_sfid(sfid_count):
        prefix = str(sfid_count).zfill(9)
        suffix = str(random.randrange(1000)).zfill(3)
        return "S_" + prefix + suffix

def print_headers(fout_acc, fout_sfid, fout_acc_sfid):
    V_HEADERS = "~id,createdBy:String,createdAt:Long,~label"
    print(V_HEADERS, file = fout_acc)
    print(V_HEADERS, file = fout_sfid)

    E_HEADERS = "~id,~from,~to,~label,createdBy:String,createdAt:Long"
    print(E_HEADERS, file = fout_acc_sfid)

###########

SIZE = 200000000 # num accounts in sample
if len(sys.argv) == 2:
    SIZE = int(sys.argv[1])

LIMIT = round(0.8 * SIZE)
BKT_SZ = round(LIMIT / 4)
BLOCK_SZ = [round(BKT_SZ / 10), round(BKT_SZ / 100), round(BKT_SZ / 1000), round(BKT_SZ / 10000)]

CREATED_AT = int(time())
CREATED_BY = '"AUTO-INGEST"'


with open('acc_shf', 'r') as fin_acc:
    with open('acc_vertex', 'w') as fout_acc:
        with open('sfid_vertex', 'w') as fout_sfid:
            with open('acc_sfid_edge', 'w') as fout_acc_sfid:
                with open('sub_groups', 'w') as fout_sub_groups:

                    print_headers(fout_acc, fout_sfid, fout_acc_sfid)

                    i = 0
                    sfid_count = 0
                    sfid = None
                    block_pos = 0

                    while i < LIMIT:
                        acc = "A_" + fin_acc.readline().strip()

                        sfid_block_sz = BLOCK_SZ[block_pos]
                        
                        if not sfid or i % sfid_block_sz == 0:
                            sfid = new_sfid(sfid_count)
                            print(f"{sfid},{CREATED_BY},{CREATED_AT},aws_sfid", file = fout_sfid)
                            print(sfid, file = fout_sub_groups)
                            sfid_count += 1

                        sfid_edge_id = f"{acc}_{sfid}"
                        print(f"{acc},{CREATED_BY},{CREATED_AT},aws_account", file = fout_acc)
                        print(f"{sfid_edge_id},{acc},{sfid},has_sfid,{CREATED_BY},{CREATED_AT}", file = fout_acc_sfid)

                        if i > 0 and i % BKT_SZ == 0:
                            block_pos += 1

                        print(i)
                        i += 1

                    while i < SIZE:

                        payer_acc = "A_" + fin_acc.readline().strip()
                        print(f"{payer_acc},{CREATED_BY},{CREATED_AT},aws_account", file = fout_acc)
                        print(payer_acc, file = fout_sub_groups)
                        i += 1

                        payer_block_sz = random.randrange(min(1000, SIZE - i))

                        while i + payer_block_sz < SIZE:
                            acc = "A_" + fin_acc.readline().strip()
                            print(f"{acc},{CREATED_BY},{CREATED_AT},aws_account", file = fout_acc)

                            pay_edge_id = f"{acc}_{payer_acc}"
                            print(f"{pay_edge_id},{acc},{payer_acc},has_payer_acc,{CREATED_BY},{CREATED_AT}", file = fout_acc_sfid)

                            print(i)
                            i += 1
