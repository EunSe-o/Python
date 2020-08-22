''' 
Quiz) 사이트별로 비밀번호를 만들어주는 프로그램을 작성하시오

예) https://naver.com
규칙 1 : https:// 부분은 제외 => naver.com 출력
규칙 2 : 처음 만나는 점(.) 이후 부분은 제외 => naver 출력
규칙 3 : 남은 글자 중 처음 세자리 + 글자 갯수 + 글자 내 'e' 갯수 + "!"로 구성
                 (nav)               (5)            (1)             (!)
예) 생성된 비밀번호 : nav51!
'''

url = "https://github.com"
site = url[8:]  # 규칙 1
site = site[:-4] # 규칙 2
site = site[:3]  # 규칙 3

length = len(site) # 글자 갯수

Count_E = site.count("e") # 글자 내 'e' 갯수

password = site + str(length) + str(Count_E) + "!"
print("{0}의 비밀번호는 {1}입니다." .format(url, password))

'''
# 나도코딩님 답안
url = "https://github.com"
my_str = url.replace("https://", "") # 규칙 1
my_str = my_str[:my_str.index(".")]  # 규칙 2

password = my_str[:3] + str(len(my_str) + str(my_str.count("e")) + "!"
print("{0}의 비밀번호는 {1}입니다." .format(url, password))
'''