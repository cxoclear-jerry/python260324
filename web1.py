# web1.py
# web crawling with bs4 
from bs4 import BeautifulSoup
page = open("Chap09_test.html", "rt", encoding="utf-8").read()
soup = BeautifulSoup(page, "html.parser")
print(soup.prettify())

# <p>를 검색
# print(soup.find_all("p"))
# print(soup.find("p"))
# print(soup.find_all("p", class_="outer-text"))
# 조건 검색 attrs를 사용
# print(soup.find_all("p", attrs={"class":"outer-text"}))
# id 로 검색
# print(soup.find_all(id="first"))
# 태그 내부의 문자열: .text
for tag in soup.find_all("p"):
    title = tag.text.strip()
    print(title)

# 문자열 처리
strA = "<<< python >>>"
result = strA.strip("<> ")
print(result)
strB = strA.replace("python", "javascript")
print(strB)
result = "spam ham egg banana".split()
print(result)
print(":) ".join(result))

# 정규표현식: 특정한 패턴(규칙) 문자열
import re

result = re.search("\d{4}", "올해는 2026년입니다.")
print(result.group())
result = re.search("apple", "this is apple.")
print(result.group())
