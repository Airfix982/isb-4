import hashlib
import json
import logging
import multiprocessing as mp
from functools import partial
from time import time
from tqdm import tqdm
from matplotlib import pyplot as plt


def luhn(init: dict)->bool:
    """
    Проверяет номер на корректность алгоритмом Луна

    args:
        init(dict): входные данные
    return:
        (bool): True, если все сошлось, иначе - False
    """
    res = 0
    try:
        with open(init["found_card"]) as f:
            number = str(json.load(f))
    except FileNotFoundError:
          logging.error(f"{init['found_card']} not found")
    
    number = list(map(int, number))
    last = number[15]
    number.pop()
    for n in number:
        i = n * 2
        if i > 9:
            res += i % 10 + i // 10
        else:
            res += i

    res = 10 - res % 10
    if res == last:
        logging.info("Карточка корректна")
    else:
        logging.info("Карточка не корректна")
         


def checking_hash(bin: int, init: dict, number: int)->int:
    """
    Сравнивает хэш полученной карты с уже существующим

    args:
        bin(int): первые 6 цифр
        init(dict): входные данные
        number(int): сгенерированные цифры карты
    return:
        (int): номер, если хэш совпал, иначе False
    """
    return int(f'{bin}{number}{init["last_digits"]}') if hashlib.sha3_256(f'{bin}{number}{init["last_digits"]}'.encode()).hexdigest() == f'{init["hash"]}' else False


def searching(init: dict, processes: int):
    """
    Ищет карту с таким же хэшем

    args:
        init(dict): входные данные
        processes(int): количесто процессов
    """
    ok = 0
    with mp.Pool(processes) as p:
        for bin in init['first_digits']:
            logging.info(f'Подбор хэша для карт {bin}XXXXXX{init["last_digits"]}')
            for result in p.map(partial(checking_hash, int(bin), init), tqdm(range(100000, 1000000), colour='#004158') ):
                    if result:
                        p.terminate()
                        ok = 1
                        logging.info(f'Найденная карта лежит по пути {init["found_card"]}')
                        try:
                            with open(init["found_card"], 'w') as f:
                                    json.dump(result, f)
                        except FileNotFoundError:
                            logging.error(f"{init['found_card']} not found")
                        break
            if ok == 1:
                 break
            
def save_stat(init: dict):
    """
    Сохраняет зависимость времени поиска коллизии хэша от кол-ва процессов
    args:
        init(dict): входные данные
    """
    times = []
    for i in range(mp.cpu_count()):
            start = time()
            logging.info(f'{i+1} процессa\n')
            searching(init, i+1)
            times.append(time()-start)
    fig=plt.figure(figsize=(30, 5))
    plt.ylabel('Время')
    plt.xlabel('процессы')
    plt.title('зависимость времени от кол-ва процессов')
    plt.plot(list(x+1 for x in range(4)),times, color='#004158') 
    plt.savefig(f'{init["stat_path"]}')
    logging.info(f'Зависимость времени от процессов сохранена по пути {init["stat_path"]}\n')