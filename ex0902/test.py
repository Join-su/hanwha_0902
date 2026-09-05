# print("AI 서비스 백엔드 프로그래밍 실무")
# print("===============================")
# print("파이썬 기본 문법, 시간:8")
# print("클래스, 시간:8")
# print("데코레이터, 시간:8")
# print("예외 처리, 시간:8")
# print("로깅, 시간:8")


# 변수로 처리
# a = "AI 서비스 백엔드 프로그래밍 실무"
# b = "==============================="
# c = "파이썬 기본 문법"
# d = "클래스"
# e = "데코레이터"
# f = "예외 처리"
# g = "로깅"

# times='8'
# t = ', 시간:'

# # print(a, b, c+t+times, d+t+times, \
# #       e+t+times, f+t+times, g+t+times, sep='\n')

# list_a = [c,d,e,f,g]

# print(a, b, sep='\n')
# print(*(i+t+times for i in list_a), sep='\n')
# print(a,)

def sum100(f):
    return f+100

def de100(f):
    return f-100

def mul100(f):
    return f*100

x = 100
print("더하기 100 :", sum100(x))
print("빼기 100 :", de100(x))
print("곱하기 100 :", mul100(x))

