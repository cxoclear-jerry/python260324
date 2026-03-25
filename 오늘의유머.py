# 웹크롤링 선언
from bs4 import BeautifulSoup
# 웹사이트 요청
import urllib.request
import re

f = open("today_humor.txt", "wt", encoding="utf-8")
for i in range(1, 11):
    url="https://www.todayhumor.co.kr/board/list.php?table=bestofbest&page=" + str(i)
    print(url)

    #User-Agent를 조작하는 경우(아이폰에서 사용하는 사파리 브라우져의 헤더) 
    hdr = {'User-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1'}

    #웹브라우져 헤더 추가 
    req = urllib.request.Request(url, headers = hdr)
    data = urllib.request.urlopen(req).read()

    # 검색이 용이한 스프객체
    soup = BeautifulSoup(data, "html.parser")
    lst = soup.find_all("td", attrs={"class":"subject"})
    for tag in lst:
        title = tag.find("a").text.strip()
        if re.search("한국", title):
            print(title)
            f.write(title + "\n")

f.close()

# <td class ="subject">
# <a href="/board/view.php?table=bestofbest&amp;no=482478&amp;s_no=482478&amp;kind=bestofbest_sort&amp;page=1&amp;o_table=humordata" target="_top">굿뉴스</a>
# <span class="subject_fixed" data-role="list-title-text" title="닌텐도 스위치 라이트 그레이 + 타이틀 4종 / 22만원">
#       닌텐도 스위치 라이트 그레이 + 타이틀 4종 / 22만원
# </span>