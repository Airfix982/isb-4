import hashlib
import json
import logging
import time

initial = {"hash": "cb28fea647fab039e21aedf9762c895f6514d70ae404d5eac3c2b1da26547745", 
"first_digits": ["519747","537643","548601","548655","552186","555156","555947","514055","531237","558334","541190","545036","547450"],
"last_digits": "5623"}

def serialization_to_json(file_name: str, text: bytes)->None:
     """
    Сереализует str в json файл
    Args:
        file_name (str): имя файла, куда сериализуется текст
        text (bytes): объект не пользовательского класса для сереализации
    Return:
     
     """
     try:
        with open(file_name, 'w') as f:
                json.dump(list(text), f)
     except FileNotFoundError:
          logging.error(f"{file_name} not found")

def luhn(number: int)->bool:
    """
    Проверяет номер на корректность алгоритмом Луна

    args:
        number(int): сгенерированные цифры карты
    return:
        (bool): True, если все сошлось, иначе - False
    """
    number = str(f'{initial["first_digits"]}{number}{initial["last_digits"]}')
    res = 0
    for i, n in enumerate(number):
        if i % 2 == 0 and i < 15:
            res += n if n < 10 else str(n)[0] + str(n)[1]
        else:
            res += n
    res = 0 if res % 10 == 0 else 10 - res % 10
    return int(res) == int((initial["last_digits"])[-1])


def checking_hash(bin: int, number: int)->int:
    """
    Сравнивает хэш полученной карты с уже существующим

    args:
        number(int): сгенерированные цифры карты
    return:
        (int): номер, если хэш совпал, иначе False
    """
    return int(f'{bin}{number}{initial["last_digits"]}') if hashlib.sha3_256(f'{bin}{number}{initial["last_digits"]}'.encode()).hexdigest() == f'{initial["hash"]}' else False