# web1.py
# web crawling with bs4 
from bs4 import BeautifulSoup
page = open("Chap09_test.html", "rt", encoding="utf-8").read()
soup = BeautifulSoup(page, "html.parser")
print(soup.prettify())

# <p>를 검색
# print(soup.find_all("p"))
# print(soup.find("p"))
print(soup.find_all("p", class_="outer-text"))
