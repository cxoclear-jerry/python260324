# 분기구문 연습
# score = int(input("점수를 입력하세요: "))
# if score >= 90 and score <= 100:
#     grade = "A" 
# elif score >= 80 and score < 90:
#     grade = "B"
# elif score >= 70 and score < 80:
#     grade = "C"
# else:
#     grade = "D"
# print("등급은 ", grade)

# value = 5
# while value > 0:
#     print(value)
#     value -= 1

# list = [100, 3.14, "apple"]
# for item in list:
#     print(item)

# colors = {"apple":"red", "banana":"yellow", "grape":"purple"}
# for item in colors.items():
#     print(item)

# for key, value in colors.items():
#     print(key, value)

print("range 함수 연습")
print(list(range(10)))
print(list(range(2000,2027))) # 2000부터 2026까지의 숫자 생성
print(list(range(1,32)))
print(list(range(10,0,-1))) # 1부터 31까지의 홀수 생성

list = [1,2,3,4,5,6,7,8,9,10]
print([i**2 for i in list if i>5])
tp = ("apple", "banana")
print([len(i) for i in tp])

print("필터링 연습")
lst = [10, 25, 30]
itemL = filter(None, lst)
for item in itemL:
    print(item)

def getBiggerThan20(x):
    return x > 20

itemL = filter(lambda x: x > 20, lst)
for item in itemL:
    print(item)

class Person:
    def __init__(self):
        self.name = "default name"
        self.age = 40
    def print(self):
        print("My name is {0} and I am {1} years old.".format(self.name, self.age))

p1 = Person()
p2 = Person()
p1.name = "Alice" 
p1.print()
p2.print()