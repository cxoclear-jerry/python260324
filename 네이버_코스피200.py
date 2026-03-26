import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import time
from datetime import datetime


def sanitize_filename(name: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", name)
    return safe[:255]


def fetch_kospi200_data(max_pages: int = 20, progress_callback=None, page_callback=None) -> pd.DataFrame:
    if not isinstance(max_pages, int) or max_pages < 1 or max_pages > 100:
        raise ValueError('max_pages must be integer between 1 and 100')

    all_data = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    for page in range(1, max_pages + 1):
        if callable(progress_callback):
            progress_callback(page, max_pages)

        print(f"페이지 {page}/{max_pages} 크롤링 중...")
        url = f"https://finance.naver.com/sise/entryJongmok.naver?type=KPI200&page={page}"

        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
        except Exception as exc:
            print(f"페이지 {page} 요청 실패: {exc}")
            time.sleep(1)
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'type_1'})
        if not table:
            continue

        page_data = []
        rows = table.find_all('tr')
        for row in rows[2:]:
            cols = row.find_all('td')
            if len(cols) < 7:
                continue

            stock_link = cols[0].find('a')
            stock_name = stock_link.text.strip() if stock_link else cols[0].text.strip()
            if not stock_name or '종목별' in stock_name:
                continue

            def clean_text(text: str) -> str:
                text = text.strip()
                return ' '.join(text.split())

            col_data = {
                '종목명': stock_name,
                '현재가': clean_text(cols[1].text),
                '전일비': clean_text(cols[2].text),
                '등락률': clean_text(cols[3].text),
                '거래량': clean_text(cols[4].text),
                '거래대금(백만)': clean_text(cols[5].text),
                '시가총액(억)': clean_text(cols[6].text)
            }
            all_data.append(col_data)
            page_data.append(col_data)

        if callable(page_callback) and page_data:
            page_callback(page, max_pages, page_data)

        time.sleep(0.5)

    if not all_data:
        return pd.DataFrame()

    df = pd.DataFrame(all_data)
    df['순위'] = range(1, len(df) + 1)
    df = df[['순위', '종목명', '현재가', '전일비', '등락률', '거래량', '거래대금(백만)', '시가총액(억)']]
    return df


def save_dataframe_to_excel(df: pd.DataFrame, prefix: str = 'kospi200') -> str:
    if df.empty:
        raise ValueError('저장할 데이터가 없습니다.')

    today_str = datetime.now().strftime('%Y%m%d')

    if '날짜' not in df.columns:
        df = df.copy()
        df['날짜'] = today_str

    filename = f"{prefix}[{today_str}].xlsx"
    filename = sanitize_filename(filename)

    df.to_excel(filename, index=False, engine='openpyxl')
    abspath = os.path.abspath(filename)
    return abspath


from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QTextEdit, QMessageBox, QHeaderView
)
from PyQt6.QtCore import QTimer
import threading


class Kospi200Gui(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('네이버 코스피200 크롤러 GUI')
        self.setGeometry(150, 150, 1000, 700)

        self.df = pd.DataFrame()
        self.init_ui()

    def init_ui(self):
        label_pages = QLabel('크롤링 페이지 수 (1-100)')
        self.input_pages = QLineEdit('20')
        self.input_pages.setFixedWidth(80)

        self.btn_fetch = QPushButton('데이터 수집')
        self.btn_fetch.clicked.connect(self.start_fetch)

        self.btn_save = QPushButton('엑셀 저장')
        self.btn_save.clicked.connect(self.save_data)
        self.btn_save.setEnabled(False)

        hbox_controls = QHBoxLayout()
        hbox_controls.addWidget(label_pages)
        hbox_controls.addWidget(self.input_pages)
        hbox_controls.addWidget(self.btn_fetch)
        hbox_controls.addWidget(self.btn_save)

        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(['순위', '종목명', '현재가', '전일비', '등락률', '거래량', '거래대금(백만)', '시가총액(억)'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addLayout(hbox_controls)
        layout.addWidget(self.table)
        layout.addWidget(QLabel('로그'))
        layout.addWidget(self.log)

        self.setLayout(layout)

    def append_log(self, text: str) -> None:
        self.log.append(f"[{datetime.now().strftime('%H:%M:%S')}] {text}")

    def start_fetch(self) -> None:
        try:
            max_pages = int(self.input_pages.text().strip())
        except ValueError:
            QMessageBox.warning(self, '입력 오류', '페이지 수는 정수여야 합니다.')
            return

        if max_pages < 1 or max_pages > 100:
            QMessageBox.warning(self, '입력 오류', '페이지 수는 1에서 100 사이여야 합니다.')
            return

        self.btn_fetch.setEnabled(False)
        self.btn_save.setEnabled(False)
        self.append_log(f'데이터 수집 시작 (페이지 수: {max_pages})')

        thread = threading.Thread(target=self.fetch_data_worker, args=(max_pages,), daemon=True)
        thread.start()

    def fetch_data_worker(self, max_pages: int) -> None:
        try:
            data = fetch_kospi200_data(
                max_pages=max_pages,
                progress_callback=self.report_progress,
                page_callback=lambda page, max_pages, rows: QTimer.singleShot(0, lambda: self.append_page_data(page, max_pages, rows))
            )
            QTimer.singleShot(0, lambda: self.on_fetch_success(data))
        except Exception as error:
            QTimer.singleShot(0, lambda: self.on_fetch_error(str(error)))

    def on_fetch_success(self, data: pd.DataFrame) -> None:
        self.df = data
        if data.empty:
            self.append_log('데이터가 없습니다.')
            QMessageBox.information(self, '완료', '데이터를 가져오지 못했습니다.')
        else:
            self.load_table(data)
            self.btn_save.setEnabled(True)
            self.append_log(f'데이터 수집 완료: {len(data)}건')
            QMessageBox.information(self, '완료', f'총 {len(data)}개 항목 수집 완료')

        self.btn_fetch.setEnabled(True)

    def report_progress(self, page: int, max_pages: int) -> None:
        QTimer.singleShot(0, lambda: self.append_log(f'진행 중: 페이지 {page}/{max_pages}'))

    def append_page_data(self, page: int, max_pages: int, page_data: list) -> None:
        self.append_log(f'페이지 {page}/{max_pages} 추가 {len(page_data)}개')

        if not page_data:
            return

        # GUI thread에서 직접 반영
        df_page = pd.DataFrame(page_data)
        current_count = len(self.df)
        if '순위' not in df_page.columns:
            df_page.insert(0, '순위', range(current_count + 1, current_count + 1 + len(df_page)))

        self.df = pd.concat([self.df, df_page], ignore_index=True)
        self.load_table(self.df)

    def on_fetch_error(self, message: str) -> None:
        self.append_log(f'오류 발생: {message}')
        QMessageBox.critical(self, '오류', message)
        self.btn_fetch.setEnabled(True)

    def load_table(self, df: pd.DataFrame) -> None:
        self.table.setRowCount(0)
        for row_idx, row in df.iterrows():
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row['순위'])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(str(row['종목명'])))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(row['현재가'])))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(row['전일비'])))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(row['등락률'])))
            self.table.setItem(row_idx, 5, QTableWidgetItem(str(row['거래량'])))
            self.table.setItem(row_idx, 6, QTableWidgetItem(str(row['거래대금(백만)'])))
            self.table.setItem(row_idx, 7, QTableWidgetItem(str(row['시가총액(억)'])))

    def save_data(self) -> None:
        if self.df.empty:
            QMessageBox.warning(self, '저장 오류', '저장할 데이터가 없습니다.')
            return

        try:
            path = save_dataframe_to_excel(self.df)
            self.append_log(f'엑셀 저장 완료: {path}')
            QMessageBox.information(self, '저장 완료', f'엑셀 파일 저장: {path}')
        except Exception as ex:
            self.append_log(f'저장 실패: {ex}')
            QMessageBox.critical(self, '저장 오류', str(ex))


if __name__ == '__main__':
    app = QApplication([])
    window = Kospi200Gui()
    window.show()
    app.exec()

