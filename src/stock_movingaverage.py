import pandas as pd
import yfinance as yf
from datetime import datetime, date, timedelta
import json
import os

# 데이터 다운로드 종료 날짜를 이전 거래일로 설정
end_date = date.today() - timedelta(days=1)
end_date_str = end_date.strftime('%Y-%m-%d')
start_date_ma = end_date - pd.Timedelta(days=60)

# 3. 가져올 티커(심볼) 지정 
STOCK_SYMBOL = "GOOGL"

df = yf.download(STOCK_SYMBOL, start=start_date_ma, end=end_date)

if df.empty:
    print(f"오류: {end_date_str}의 GOOGL 주가 데이터를 다운로드하지 못했습니다. 나중에 다시 시도하세요.")
else:
    df['MA_5'] = df['Close'].rolling(window=5).mean()
    df['MA_20'] = df['Close'].rolling(window=20).mean()

    # 이동평균선 값이 NaN이 아닌지 확인
    if pd.notna(df['MA_5'].iloc[-1]) and pd.notna(df['MA_20'].iloc[-1]):
        try:
            recent_ma_5 = float(df['MA_5'].iloc[-1])
            recent_ma_20 = float(df['MA_20'].iloc[-1])
            recent_close_price = float(df['Close'].iloc[-1])

            # JSON 형태로 저장할 데이터 구성
            technical_indicators_data = {
                "Stock": STOCK_SYMBOL,
                "Recent_Close_Price": recent_close_price,
                "MA_5": recent_ma_5,
                "MA_20": recent_ma_20,
                "Date": end_date_str
            }

    
            # 저장할 폴더 설정
            folder_name = "report"
            folder_path = os.path.join(os.getcwd(), folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"'{folder_name}' 폴더 생성 완료")

            # JSON 파일 이름 생성 (이전 거래일로 변경)
            filename = f"{STOCK_SYMBOL}_Moving_Average.json"
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'w') as f:
                json.dump(technical_indicators_data, f, indent=4)
            print(f"'{folder_name}' 폴더에 '{filename}' 저장 완료")
        except TypeError as e:
            print(f"JSON 직렬화 오류 발생 (TypeError): {e}")
        except Exception as e:
            print(f"'{filename}' 저장 실패: {e}")
    else:
        print(f"오류: 이동평균선 값을 계산할 수 없습니다. 데이터가 부족하거나 NaN 값을 포함하고 있습니다.")