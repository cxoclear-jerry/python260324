# # python 내부모듈 연습
# import random
# print(random.random())
# print(random.random())
# print(random.uniform(2.0, 5.0))
# print([random.randrange(20) for i in range(10)])
# print([random.randrange(20) for i in range(10)])
# print(random.sample(range(20), 10))
# print(random.sample(range(20), 10))
# print(random.shuffle(list(range(1,45))))

import os
from os.path import *
print("운영체제명", os.name)
filename = "c:\\python313\\python.exe"
if exists(filename):   
    print("파일명:", basename(filename))
    print("디렉토리명:", dirname(filename))
    print("파일크기:", getsize(filename), "bytes")
else:
    print("파일이 존재하지 않습니다.")