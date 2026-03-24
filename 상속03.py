class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def printInfo(self):
        print(f"ID: {self.id}, Name: {self.name}")

class Manager(Person):
    def __init__(self, id, name, title):
        super().__init__(id, name)
        self.title = title

    def printInfo(self):
        super().printInfo()
        print(f"Title: {self.title}")

class Employee(Person):
    def __init__(self, id, name, skill):
        super().__init__(id, name)
        self.skill = skill

    def printInfo(self):
        super().printInfo()
        print(f"Skill: {self.skill}")

# 테스트 코드
if __name__ == "__main__":
    # 테스트 1: Person 객체 생성 및 printInfo
    person1 = Person(1, "Alice")
    person1.printInfo()
    print()

    # 테스트 2: Person 객체 생성 및 printInfo
    person2 = Person(2, "Bob")
    person2.printInfo()
    print()

    # 테스트 3: Manager 객체 생성 및 printInfo
    manager1 = Manager(3, "Charlie", "Senior Manager")
    manager1.printInfo()
    print()

    # 테스트 4: Manager 객체 생성 및 printInfo
    manager2 = Manager(4, "Diana", "Project Manager")
    manager2.printInfo()
    print()

    # 테스트 5: Employee 객체 생성 및 printInfo
    employee1 = Employee(5, "Eve", "Python Programming")
    employee1.printInfo()
    print()

    # 테스트 6: Employee 객체 생성 및 printInfo
    employee2 = Employee(6, "Frank", "Data Analysis")
    employee2.printInfo()
    print()

    # 테스트 7: Manager의 부모 메서드 접근
    print("Manager's ID:", manager1.id)
    print("Manager's Name:", manager1.name)
    print("Manager's Title:", manager1.title)
    print()

    # 테스트 8: Employee의 부모 메서드 접근
    print("Employee's ID:", employee1.id)
    print("Employee's Name:", employee1.name)
    print("Employee's Skill:", employee1.skill)
    print()

    # 테스트 9: 여러 객체 리스트
    people = [
        Person(7, "Grace"),
        Manager(8, "Henry", "Team Lead"),
        Employee(9, "Ivy", "Machine Learning")
    ]
    for person in people:
        person.printInfo()
        print()

    # 테스트 10: 상속 확인
    print("Is manager1 a Person?", isinstance(manager1, Person))
    print("Is employee1 a Person?", isinstance(employee1, Person))
    print("Is person1 a Manager?", isinstance(person1, Manager))
