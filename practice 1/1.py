# 자기 소개
print("저의 이름은 박은서입니다.")
print("저는 20살이며, 광운대학교에 다니고 있습니다.")
print("저는 성인일까요? True")

# 변수를 사용하여 자기소개
name = "박은서"
age = 20
collage = "광운대학교" # 변수를 바꾸어 문장을 바꿀 수 있음
is_adult = age >= 20

# '+ 변수 +'를 사용하면 앞 뒤 띄어쓰기가 되지 않음
print("저의 이름은 "+ name +"입니다.")
print("저는 "+ str(age) +"살이며, "+ collage +"에 다니고 있습니다.")
print("저는 성인일까요? " + str(is_adult))

# ', 변수 ,'를 사용하면 자동으로 앞 뒤 띄어쓰기가 됨
print("저의 이름은",name,"입니다.")
print("저는 ",str(age),"살이며, ",collage,"에 다니고 있습니다.")
print("저는 성인일까요?", str(is_adult))