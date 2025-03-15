import yfinance as yf
from datetime import datetime
import csv

def format_pub_date(full_date_str):
    try:
        dt = datetime.fromisoformat(full_date_str.replace('Z', ''))
        return dt.strftime("%Y-%m-%d")
    except:
        return full_date_str[:10]

# CSV 파일 생성
with open('news.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    # CSV 작성기 생성 및 헤더 작성
    fieldnames = ['날짜', '제목', '출처', '요약']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # 뉴스 데이터 가져오기
    dat = yf.Ticker("GOOGL")
    news = dat.get_news(count=5)

    # 각 뉴스 항목 처리
    for item in news:
        content = item['content']
        
        # 데이터 추출
        pub_date = format_pub_date(content['pubDate'])
        title = content['title']
        provider = content['provider']['displayName']
        summary = content.get('summary', '요약 내용 없음')  # summary가 없는 경우 대비

        # CSV 파일에 기록
        writer.writerow({
            '날짜': pub_date,
            '제목': title,
            '출처': provider,
            '요약': summary
        })

        # 콘솔 출력 (기존 기능 유지)
        print(f"[{pub_date}] {title}")
        print(f"출처: {provider}")
        print(f"요약: {summary}\n{'-'*50}")

print("뉴스 데이터가 news.csv 파일로 저장되었습니다.")