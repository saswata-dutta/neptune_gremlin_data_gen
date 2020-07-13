import random
from time import time


CUST_PREFIX = "aws__customer__"
CUST_VERTEX = "customer"
CUST_EDGE = "has_customer"
#####

def print_headers(fout_cust, fout_cust_edge):
    V_HEADERS = "~id,createdBy:String,createdAt:Long,~label"
    print(V_HEADERS, file = fout_cust)

    E_HEADERS = "~from,~to,~label,createdBy:String,createdAt:Long"
    print(E_HEADERS, file = fout_cust_edge)

def new_cust(count):
        prefix = str(count).zfill(7)
        suffix = str(random.randrange(100000)).zfill(5)
        return CUST_PREFIX + prefix + suffix

CREATED_AT = int(time())
CREATED_BY = '"AUTO-INGEST"'

#####

with open('sub_groups_shf', 'r') as fin_sub_groups:
    with open('cust_vertex', 'w') as fout_cust:
        with open('subg_cust_edge', 'w') as fout_cust_edge:

            print_headers(fout_cust, fout_cust_edge)

            next_block = 0
            cust = None
            for i, line in enumerate(fin_sub_groups):
                
                if i == next_block:
                    cust = new_cust(i + 1)
                    next_block = random.randint(i + 1, i + 50)
                    print(f"{cust},{CREATED_BY},{CREATED_AT},{CUST_VERTEX}", file = fout_cust)

                sub_group = line.strip()
                print(f"{sub_group},{cust},{CUST_EDGE},{CREATED_BY},{CREATED_AT}", file = fout_cust_edge)
