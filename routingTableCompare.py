import re
from IPy import IP
from collections import defaultdict
import multiprocessing
import time
source_list = []

with open('/Users/Peter/Downloads/tietong1', mode='rt') as f:
    for line in f:
        if re.match(r'B>', line):
            source_list.extend(re.findall(r'(\d+\.\d+\.\d+\.\d+/\d+)', line))

dest_dict = defaultdict(list)

with open('/Users/Peter/Desktop/Me60RoutingTable.log', mode='rt') as f:
    for line in f:
        subnet = re.findall(r'(\d+\.\d+\.\d+\.\d+/\d+)', line)
        if subnet:
            dest_dict[re.findall(r'^(\d+)', subnet[0])[0]].extend(subnet)


def compare_subnet(source_list, dest_dict):
    for source in source_list:
        print(source)
        source_flag = False
        if re.findall(r'^(\d+)', source)[0] in dest_dict.keys():
            for dest in dest_dict[re.findall(r'^(\d+)', source)[0]]:
                if IP(source) in IP(dest):
                    source_flag = True
            if not source_flag:
                ip, netmask = source.split('/')
                print('ip route-static {} {} 10.6.0.9'.format(ip, netmask))


def main():
    s1 = time.time()
    pool = multiprocessing.Pool(processes=2)

    pool.apply_async(compare_subnet, (source_list[0:int(len(source_list)/2)-1], dest_dict))
    pool.apply_async(compare_subnet, (source_list[int(len(source_list)/2):], dest_dict))
    pool.close()
    pool.join()
    e1 = time.time()
    print('multiprocess {}'.format(e1-s1))
    print("Sub-process(es) done.")


if __name__ == '__main__':
    main()