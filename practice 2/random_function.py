from random import *

print(random()) # 0.0 ~ 1.0 미만의 난수 생성 
print(random() * 10) # 0.0 ~ 10.0 미만의 난수 생성
print(int(random() * 10)) # 0 ~ 10 미만의 난수 생성
print(int(random() * 10) + 1) # 1 ~ 10 이하의 난수 생성

## 아래 세 개의 식 모두 같은 의미
print(int(random() * 45) + 1) # 1 ~ 45 이하의 난수 생성
print(randrange(1, 46)) # 1 ~ 46 미만의 난수 생성
print(randint(1, 45)) # 1 ~ 45 이하의 난수 생성
##

'''
print(int(random() * a) + b) 
-> 0+b ~ (1.0*a)+b 미만의 난수 생성

print(randrange(a, b))
-> a ~ b 미만의 난수 생성

print(randint(a, b))
-> a ~ b 이하의 난수 생성
'''