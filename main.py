import hashlib
import multiprocessing as mp
import time
import argparse
import logging
from functools import partial

from additional_funcs import checking_hash
from additional_funcs import luhn

initial = {"hash": "cb28fea647fab039e21aedf9762c895f6514d70ae404d5eac3c2b1da26547745", 
"first_digits": ["519747","537643","548601","548655","552186","555156","555947","514055","531237","558334","541190","545036","547450"],
"last_digits": "5623"}

def searching():
    ok = 0
    cores = mp.cpu_count()
    with mp.Pool(processes=cores) as p:
        for bin in initial['first_digits']:
            for result in p.map(partial(checking_hash, int(bin)), range(100000, 1000000)):
                    if result:
                        p.terminate()
                        ok = 1
                        print(f'we have found {result} and have terminated pool')
                        break
            if ok == 1:
                 break


if __name__ == '__main__':
    searching()