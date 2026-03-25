import sqlite3
import random
import os

class ProductDB:
    def __init__(self, db_name='MyProduct.db'):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        # 데이터베이스 파일 삭제 시도 (기존 데이터 초기화)
        try:
            if os.path.exists(self.db_name):
                os.remove(self.db_name)
                print("기존 데이터베이스 파일 삭제 완료")
        except OSError as e:
            print(f"데이터베이스 파일 삭제 실패 (다른 프로세스 사용 중): {e}")
            print("기존 데이터를 유지하고 진행합니다.")
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS Products')
        cursor.execute('''
            CREATE TABLE Products (
                productID INTEGER PRIMARY KEY,
                productName TEXT NOT NULL,
                productPrice INTEGER NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        print("테이블 생성 완료")

    def insert_product(self, product_id, product_name, product_price):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Products (productID, productName, productPrice)
            VALUES (?, ?, ?)
        ''', (product_id, product_name, product_price))
        conn.commit()
        conn.close()

    def update_product(self, product_id, product_name=None, product_price=None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        if product_name and product_price:
            cursor.execute('''
                UPDATE Products
                SET productName = ?, productPrice = ?
                WHERE productID = ?
            ''', (product_name, product_price, product_id))
        elif product_name:
            cursor.execute('''
                UPDATE Products
                SET productName = ?
                WHERE productID = ?
            ''', (product_name, product_id))
        elif product_price:
            cursor.execute('''
                UPDATE Products
                SET productPrice = ?
                WHERE productID = ?
            ''', (product_price, product_id))
        conn.commit()
        conn.close()

    def delete_product(self, product_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM Products
            WHERE productID = ?
        ''', (product_id,))
        conn.commit()
        conn.close()

    def select_product(self, product_id=None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        if product_id:
            cursor.execute('''
                SELECT * FROM Products
                WHERE productID = ?
            ''', (product_id,))
            result = cursor.fetchone()
        else:
            cursor.execute('SELECT * FROM Products')
            result = cursor.fetchall()
        conn.close()
        return result

# 샘플 데이터 10만 개 생성 및 삽입
if __name__ == "__main__":
    try:
        db = ProductDB()
        
        # 샘플 데이터 생성
        sample_data = []
        for i in range(1, 100001):  # 1부터 100000까지
            product_name = f"전자제품 {i}"
            product_price = random.randint(1000, 100000)  # 가격 범위: 1000 ~ 100000
            sample_data.append((i, product_name, product_price))
        
        # 데이터 삽입 (배치로 속도 향상)
        conn = sqlite3.connect(db.db_name)
        cursor = conn.cursor()
        cursor.executemany('''
            INSERT INTO Products (productID, productName, productPrice)
            VALUES (?, ?, ?)
        ''', sample_data)
        conn.commit()
        conn.close()
        
        print("샘플 데이터 10만 개 삽입 완료")
        
        # 테스트: 첫 번째 제품 조회
        product = db.select_product(1)
        print(f"제품 ID 1: {product}")
        
    except Exception as e:
        print(f"오류 발생: {e}")