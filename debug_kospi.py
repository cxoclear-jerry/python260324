import requests
from bs4 import BeautifulSoup

# 네이버 금융 코스피200 페이지 URL
url = "https://finance.naver.com/sise/sise_index.naver?code=KPI200"

# 헤더 설정
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

try:
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 모든 테이블 찾기
    tables = soup.find_all('table')
    print(f"총 테이블 개수: {len(tables)}")
    print("\n테이블들의 클래스명:")
    for i, table in enumerate(tables[:5]):
        print(f"{i}: {table.get('class')}")
    
    # 모든 div 중에 편입종목상위와 관련된 것 찾기
    print("\n'편입' 키워드 검색:")
    text = soup.get_text()
    if '편입종목상위' in text:
        print("페이지에 '편입종목상위' 텍스트 발견")
        
        # 편입종목상위를 포함하는 div 찾기
        for div in soup.find_all('div'):
            if '편입종목상위' in div.get_text():
                print(f"\n발견된 div 클래스: {div.get('class')}")
                # 그 div 내부의 테이블 찾기
                inner_table = div.find('table')
                if inner_table:
                    print(f"내부 테이블 클래스: {inner_table.get('class')}")
                    print("\n테이블 내용 미리보기:")
                    rows = inner_table.find_all('tr')[:3]
                    for row in rows:
                        cols = row.find_all(['th', 'td'])
                        print([col.text.strip() for col in cols])
                break
    else:
        print("페이지에 '편입종목상위' 텍스트 미발견")
        
except Exception as e:
    print(f"오류: {e}")
