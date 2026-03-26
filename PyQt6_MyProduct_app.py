import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QSpinBox, QPushButton,
    QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox
)

DB_FILE = 'MyProduct.db'

class MyProductApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('자동차 편의용품 관리')
        self.setGeometry(100, 100, 700, 500)

        self.create_db()
        self.init_ui()
        self.load_data()

    def create_db(self):
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS MyProduct (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price INTEGER NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def init_ui(self):
        label_id = QLabel('ID')
        self.input_id = QSpinBox()
        self.input_id.setRange(1, 9999999)

        label_name = QLabel('제품명')
        self.input_name = QLineEdit()

        label_price = QLabel('가격')
        self.input_price = QSpinBox()
        self.input_price.setRange(0, 99999999)

        hbox_id = QHBoxLayout()
        hbox_id.addWidget(label_id)
        hbox_id.addWidget(self.input_id)

        hbox_name = QHBoxLayout()
        hbox_name.addWidget(label_name)
        hbox_name.addWidget(self.input_name)

        hbox_price = QHBoxLayout()
        hbox_price.addWidget(label_price)
        hbox_price.addWidget(self.input_price)

        self.btn_add = QPushButton('입력')
        self.btn_update = QPushButton('수정')
        self.btn_delete = QPushButton('삭제')
        self.btn_search = QPushButton('검색')
        self.btn_refresh = QPushButton('새로고침')

        self.btn_add.clicked.connect(self.add_product)
        self.btn_update.clicked.connect(self.update_product)
        self.btn_delete.clicked.connect(self.delete_product)
        self.btn_search.clicked.connect(self.search_product)
        self.btn_refresh.clicked.connect(self.load_data)

        hbox_buttons = QHBoxLayout()
        hbox_buttons.addWidget(self.btn_add)
        hbox_buttons.addWidget(self.btn_update)
        hbox_buttons.addWidget(self.btn_delete)
        hbox_buttons.addWidget(self.btn_search)
        hbox_buttons.addWidget(self.btn_refresh)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ID', '제품명', '가격'])
        self.table.cellClicked.connect(self.on_table_cell_clicked)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_id)
        vbox.addLayout(hbox_name)
        vbox.addLayout(hbox_price)
        vbox.addLayout(hbox_buttons)
        vbox.addWidget(self.table)

        self.setLayout(vbox)

    def run_query(self, query, params=()):
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        return cur

    def load_data(self):
        cur = self.run_query('SELECT id, name, price FROM MyProduct ORDER BY id')
        rows = cur.fetchall()

        self.table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(row[1]))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(row[2])))

    def add_product(self):
        id_ = self.input_id.value()
        name = self.input_name.text().strip()
        price = self.input_price.value()

        if not name:
            QMessageBox.warning(self, '입력 오류', '제품명을 입력해주세요.')
            return

        try:
            self.run_query('INSERT INTO MyProduct (id, name, price) VALUES (?, ?, ?)', (id_, name, price))
            QMessageBox.information(self, '성공', '상품이 추가되었습니다.')
            self.load_data()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, '오류', f'ID {id_}가 이미 존재합니다.')

    def update_product(self):
        id_ = self.input_id.value()
        name = self.input_name.text().strip()
        price = self.input_price.value()

        if not name:
            QMessageBox.warning(self, '입력 오류', '제품명을 입력해주세요.')
            return

        cur = self.run_query('SELECT COUNT(*) FROM MyProduct WHERE id = ?', (id_,))
        if cur.fetchone()[0] == 0:
            QMessageBox.warning(self, '오류', f'ID {id_} 상품이 존재하지 않습니다.')
            return

        self.run_query('UPDATE MyProduct SET name = ?, price = ? WHERE id = ?', (name, price, id_))
        QMessageBox.information(self, '성공', '상품 정보가 수정되었습니다.')
        self.load_data()

    def delete_product(self):
        id_ = self.input_id.value()

        cur = self.run_query('SELECT COUNT(*) FROM MyProduct WHERE id = ?', (id_,))
        if cur.fetchone()[0] == 0:
            QMessageBox.warning(self, '오류', f'ID {id_} 상품이 존재하지 않습니다.')
            return

        self.run_query('DELETE FROM MyProduct WHERE id = ?', (id_,))
        QMessageBox.information(self, '성공', '상품이 삭제되었습니다.')
        self.load_data()

    def search_product(self):
        id_ = self.input_id.value()
        name = self.input_name.text().strip()

        if id_ > 0:
            cur = self.run_query('SELECT id, name, price FROM MyProduct WHERE id = ?', (id_,))
            rows = cur.fetchall()
        elif name:
            cur = self.run_query('SELECT id, name, price FROM MyProduct WHERE name LIKE ?', (f'%{name}%',))
            rows = cur.fetchall()
        else:
            QMessageBox.warning(self, '검색 오류', 'ID 또는 제품명을 입력해서 검색하세요.')
            return

        self.table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(row[1]))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(row[2])))

    def on_table_cell_clicked(self, row, col):
        self.input_id.setValue(int(self.table.item(row, 0).text()))
        self.input_name.setText(self.table.item(row, 1).text())
        self.input_price.setValue(int(self.table.item(row, 2).text()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyProductApp()
    window.show()
    sys.exit(app.exec())
