# DemoForm.ui(화면단) + DemoForm.py(로직단)
import sys
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6 import uic

# 디자인 파일 로딩
form_class = uic.loadUiType("DemoForm.ui")[0]  
# DemoForm 클래스 정의
class DemoForm(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # UI 초기화
        self.label.setText("Hello, PyQt6!")  # 라벨 텍스트 설정

# 진입점 체크
if __name__ == "__main__":
    app = QApplication(sys.argv)  # QApplication 객체 생성
    demo = DemoForm()  # DemoForm 인스턴스 생성
    demo.show()  # 창 표시
    sys.exit(app.exec())  # 이벤트 루프 시작