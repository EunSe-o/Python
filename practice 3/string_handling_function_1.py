python = "Python is Amazing"

# lower() 전부 소문자 출력
print(python.lower())

# upper() 전부 대문자 출력
print(python.upper())

# isupper() 해당 문자가 대문자인지 출력
print(python[0].isupper())

# len(변수) 해당 변수 전체 문자열의 길이 출력
print(len(python))

# replace("찾고 싶은 문자", "바꿀 문자")
print(python.replace("Python", "Java"))

# index("문자") 해당 문자가 몇 번째에 있는지 출력
index = python.index("n")
print(index)
index = python.index("n", index + 1) 
# 앞에서 찾은 위치의 다음(6)부터 찾음
print(index)

# find("문자") 해당 문자가 몇 번째에 있는지 출력
print(python.find("n"))

''' find 과 index 의 차이점
: find는 해당 문자가 변수에 없으면 -1 출력
print(python.find("Java")) # -1

: index는 해당 문자가 변수에 없으면 오류
print(python.index("Java")) # 오류
'''

# count("문자") 해당 문자가 변수 안에 몇 번 등장하는지 출력
print(python.count("n"))