

import os
import string
#
#
# import qrcode
# # пример данных
# data = input("Введите числа:")
# # имя конечного файла
# filename = "1.png"
# # генерируем qr-код
# img = qrcode.make(data)
# # сохраняем img в файл
# img.save(filename)

import os
import string
import hashlib
from django.conf import settings
def generate_random_string(length,
                           stringset="".join(
                               [string.ascii_letters+string.digits]
                           )):

    return "".join([stringset[i%len(stringset)] for i in [x for x in os.urandom(length)]])

a = generate_random_string(300).encode()
#
stringset="".join([string.ascii_letters+string.digits])

# def salted_hash(string):
#     return hashlib.sha1(string.encode()).hexdigest()

solt = "dskljfwqj".encode()

print()
print('********', type(a))
print('********', type(solt))
print()
def salted_hash(string):
    return hashlib.sha1(b" ".join([
        string,
        solt,
    ])).hexdigest()


qr_hash = salted_hash(a)

import qrcode
# пример данных
# data = input("Введите числа:")
# имя конечного файла
filename = "1.png"
# генерируем qr-код
img = qrcode.make(qr_hash)
# сохраняем img в файл
img.save(filename)
print()
print('********', a)
print('********', qr_hash)
print()







