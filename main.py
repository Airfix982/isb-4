import hashlib
import multiprocessing as mp
import time
import logging
from functools import partial
import argparse
import json
import os
from tqdm import tqdm

from some_funcs import checking_hash
from some_funcs import luhn
from some_funcs import searching


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--init_path',default='files\\init.json',help='Путь к json файлу с данными, default = files\\settings.json', action='store') 
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('-f','--find',help='Поиск номеров карт с заданным хэшем', action='store_true')
    group.add_argument('-c','--check',help='Проверяет карту на достоверность', action='store_true')
    group.add_argument('-s','--statistic',help='Вывод зависимости времени выполненя от кол-ва потоков', action='store_true')  
    args = parser.parse_args()
    init_path = args.init_path
    try:
        with open(init_path) as jf:
            init = json.load(jf)
    except FileNotFoundError:
        logging.error(f"{init_path} not found")

    mode = (args.find, args.check, args.statistic)

    match mode:
        case (True, False, False):
                logging.info('Поиск номера карточки\n')
                searching(init)
        case (False, True, False):
                logging.info('Проверка корректности карточки')
                luhn(init)
        case (False, False, True):
            with tqdm(total=2) as pbar:
                logging.info('Сбор данных\n')
                #statistic(init, pbar)
        case _:
            logging.error("wrong mode")