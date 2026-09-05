# 파이썬 클래스
class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"안녕하세요, {self.name}입니다"

p = Person("영희")
print(p.greet())
