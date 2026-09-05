# 파이썬 상속
class Animal:
    def sound(self):
        return "..."

class Dog(Animal):
    def sound(self):
        return "멍멍"

print(Dog().sound())
