# DemoForm2.ui(화면단) + DemoForm2.py(로직단)
import sys
# 수정
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic

# 웹크롤링 선언
from bs4 import BeautifulSoup
# 웹사이트 요청
import urllib.request
import re

# 디자인 파일 로딩
form_class = uic.loadUiType("DemoForm2.ui")[0]  
# DemoForm 클래스 정의
class DemoForm(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # UI 초기화
        self.label.setText("Hello, PyQt6!")  # 라벨 텍스트 설정
# 슬롯 메서드 추가
    def firstClick(self):
        f = open("clien.txt", "wt", encoding="utf-8")
        for i in range(0, 10):
            url="https://www.clien.net/service/board/sold?&od=T31&category=0&po=" + str(i)
            print(url)

            #User-Agent를 조작하는 경우(아이폰에서 사용하는 사파리 브라우져의 헤더) 
            hdr = {'User-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1'}

            #웹브라우져 헤더 추가 
            req = urllib.request.Request(url, headers = hdr)
            data = urllib.request.urlopen(req).read()

            # 검색이 용이한 스프객체
            soup = BeautifulSoup(data, "html.parser")
            lst = soup.find_all("span", {"data-role":"list-title-text"})
            for tag in lst:
                title = tag.text.strip()
                if re.search("아이폰", title):
                    print(title)
                    f.write(title + "\n")

        f.close()
        self.label.setText("클리앙 중고장터 크롤링 완료!!")  # 버튼 클릭 시 라벨 텍스트 변경
    def secondClick(self):
        self.label.setText("두 번째 버튼 클릭!!")  # 버튼 클릭 시 라벨 텍스트 변경
    def thirdClick(self):
        self.label.setText("세 번째 버튼 클릭!!")  # 버튼 클릭 시 라벨 텍스트 변경



# 진입점 체크
if __name__ == "__main__":
    app = QApplication(sys.argv)  # QApplication 객체 생성
    demo = DemoForm()  # DemoForm 인스턴스 생성
    demo.show()  # 창 표시
    sys.exit(app.exec())  # 이벤트 루프 시작