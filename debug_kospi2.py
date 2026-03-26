import requests
from bs4 import BeautifulSoup

url = "https://finance.naver.com/sise/sise_index.naver?code=KPI200"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

try:
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # type_4 테이블 확인
    table_type4 = soup.find('table', {'class': 'type_4'})
    if table_type4:
        print("=== type_4 테이블 ===")
        rows = table_type4.find_all('tr')[:5]
        for row in rows:
            cols = row.find_all(['th', 'td'])
            print([col.text.strip() for col in cols[:6]])
    
    # type_r1 테이블 확인
    table_type_r1 = soup.find('table', {'class': 'type_r1'})
    if table_type_r1:
        print("\n=== type_r1 테이블 ===")
        rows = table_type_r1.find_all('tr')[:5]
        for row in rows:
            cols = row.find_all(['th', 'td'])
            print([col.text.strip() for col in cols[:6]])
    
    # 페이지 텍스트에서 '코스피200' 관련 정보 찾기
    print("\n=== 페이지 주요 텍스트 ===")
    text = soup.get_text()
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if len(line.strip()) > 10 and ('편입' in line or '상위' in line or '종목' in line):
            print(f"{i}: {line.strip()[:80]}")
            if i > 50:  # 처음 50줄만
                break
                
except Exception as e:
    print(f"오류: {e}")
