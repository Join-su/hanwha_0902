student = {
    "name": "지수",
    "age": 20,
    "address": {
        "city": "서울",
        "district": "강남구"
    },
    "grades": {
        "math": 90,
        "english": 85
    }
}

print(student["name"])
print(student["address"]["city"])
print(student["grades"]["math"])

for subject, score in student["grades"].items():
    print(subject, score)

student1 = {
    "name": "지수",
    "age": 20
}

student2 = {
    "name": "민준",
    "age": 22
}

students = {
    "student1": student1,
    "student2": student2
}

print(students["student1"]["name"])
print(students["student2"]["age"])

for key, info in students.items():
    print(key, info["name"], info["age"])

