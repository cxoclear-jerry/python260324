# 클래스 상속 연습
# Person 클래스를 정의하는 데 id, name 변수가 있고
# printInfo()라는 메서드로 해당 정보를 클릭
class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def printInfo(self):
        print(f"ID: {self.id}, Name: {self.name}")

# 해당 클래스의 인스턴스를 생성
person1 = Person(1, "Alice")
# printInfo() 메서드를 호출하여 정보를 출력
person1.printInfo()