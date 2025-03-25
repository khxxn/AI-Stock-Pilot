import yfinance as yf
import json
import os

# 설정 값
STOCK_SYMBOL = "GOOGL"
NEWS_COUNT = 20  # 원하는 뉴스 개수 설정

def get_news_summary(content_item):
    return content_item.get('summary', '콘텐츠 없음')

# JSON 데이터 구조 생성
news_data = []

# 뉴스 데이터 가져오기
dat = yf.Ticker(STOCK_SYMBOL)
news_items = dat.get_news(count=NEWS_COUNT)  # count 파라미터 추가

for item in news_items:
    content = item['content']
    news_entry = {
        "stock": STOCK_SYMBOL,
        "date": content['pubDate'],
        "title": content['title'],
        "provider": content['provider'].get('displayName', '알 수 없음'),
        "summary": get_news_summary(content)
    }
    news_data.append(news_entry)

    # 콘솔 출력
    print(f"[{news_entry['date']}] {news_entry['title']}")
    print(f"출처: {news_entry['provider']}")
    print(f"내용: {news_entry['summary'][:100]}...\n{'-'*50}")

# JSON 파일 저장
folder_name = "report"
folder_path = os.path.join(os.getcwd(), folder_name)
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"'{folder_name}' 폴더 생성 완료")
with open(folder_path + f'/{STOCK_SYMBOL}_news.json', 'w', encoding='utf-8') as f:
    json.dump(news_data, f, ensure_ascii=False, indent=2)

print(f"{STOCK_SYMBOL} 관련 최신 {NEWS_COUNT}개 뉴스가 저장되었습니다.")