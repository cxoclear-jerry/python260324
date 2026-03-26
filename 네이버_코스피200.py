from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime

try:
    # Selenium 드라이버 설정
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

    driver = webdriver.Chrome(options=options)

    # 전체 데이터를 저장할 리스트
    all_data = []

    # 1부터 20페이지까지 크롤링
    for page in range(1, 21):
        print(f"페이지 {page}/20 크롤링 중...")

        # 페이지별 URL 생성
        url = f"https://finance.naver.com/sise/entryJongmok.naver?type=KPI200&page={page}"
        driver.get(url)

        # 테이블이 로드될 때까지 대기
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table.type_1 tr")))

        time.sleep(1)  # 페이지 로드 대기

        # HTML 파싱
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 편입종목상위 테이블 찾기
        table = soup.find('table', {'class': 'type_1'})

        if table:
            # 테이블의 모든 행 추출
            rows = table.find_all('tr')

            # 해더 행 이후부터 데이터 추출 (tr[0]은 th, tr[1]은 빈 행)
            for row in rows[2:]:
                cols = row.find_all('td')

                if len(cols) >= 7:  # 필요한 열이 모두 있는지 확인
                    # 종목명은 td 내의 a 태그에서 추출
                    stock_link = cols[0].find('a')
                    stock_name = stock_link.text.strip() if stock_link else cols[0].text.strip()

                    # 전일비 정리 (불필요한 줄바꿈 및 공백 제거)
                    change_val = cols[2].text.strip()
                    change_val = ' '.join(change_val.split())  # 여러 줄의 공백을 하나로 정리

                    # 등락률 정리
                    change_rate = cols[3].text.strip()
                    change_rate = ' '.join(change_rate.split())

                    col_data = {
                        '종목명': stock_name,
                        '현재가': cols[1].text.strip(),
                        '전일비': change_val,
                        '등락률': change_rate,
                        '거래량': cols[4].text.strip(),
                        '거래대금(백만)': cols[5].text.strip(),
                        '시가총액(억)': cols[6].text.strip()
                    }

                    # 빈 행이나 구분선 제외
                    if stock_name and '종목별' not in stock_name:
                        all_data.append(col_data)

    # 드라이버 종료
    driver.quit()

    # 데이터프레임으로 변환
    df = pd.DataFrame(all_data)

    # 전체 순위 재설정
    df['순위'] = range(1, len(df) + 1)

    # 컬럼 순서 재배열
    df = df[['순위', '종목명', '현재가', '전일비', '등락률', '거래량', '거래대금(백만)', '시가총액(억)']]

    # 결과 출력
    print("=" * 120)
    print("코스피200 편입종목상위 데이터 (전체 20페이지)")
    print("=" * 120)
    print(df.to_string(index=False))
    print(f"\n총 {len(df)}개의 데이터가 수집되었습니다.")

    # 현재 날짜 가져오기
    today = datetime.now().strftime('%Y%m%d')
    
    # 엑셀 파일로 저장
    excel_filename = f'kospi200_all_stocks_{today}.xlsx'
    df.to_excel(excel_filename, index=False, engine='openpyxl')
    print(f"\n엑셀 파일로 저장되었습니다: {excel_filename}")

except Exception as e:
    print(f"오류 발생: {e}")
    try:
        driver.quit()
    except:
        pass
