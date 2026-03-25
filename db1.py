# 데이터베이스 연습
import sqlite3
con = sqlite3.connect(":memory:") # 메모리 상에서 데이터베이스 생성
cur = con.cursor() # 커서 객체 생성
cur.execute("CREATE TABLE PhoneBook (Name TEXT, PhoneNum TEXT)") # PhoneBook 테이블 생성
cur.execute("INSERT INTO PhoneBook VALUES ('Alice', '010-1234-5678')") # 데이터 삽입
name = "Bob"
phone_num = "010-9876-5432"
cur.execute("INSERT INTO PhoneBook VALUES (?, ?)", (name, phone_num)) # 데이터 삽입
# 다중 데이터를 입력
datalist = [('Charlie', '010-1111-2222'), ('David', '010-3333-4444')]
cur.executemany("INSERT INTO PhoneBook VALUES (?, ?)", datalist) # 다중 데이터 삽입
# 데이터 조회
# for row in cur.execute("SELECT * FROM PhoneBook;"):
#     print(row)
cur.execute("SELECT * FROM PhoneBook;") # 데이터 조회
print("---fetchone()---")
print(cur.fetchone())
print("---fetchmany(2)---")
print(cur.fetchmany(2))
print("---fetchall()---")
print(cur.fetchall())
con.close() # 데이터베이스 연결 종료