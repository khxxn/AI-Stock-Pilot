import requests #외부 api 호출
import pandas as pd #데이터 구조, 가공
import yfinance as yf #yahoo finance 데이터 수집
from datetime import datetime #날짜 시간처리
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('FRED_API_KEY')

# FRED에서 제공하는 지표 코드와 명칭
fred_indicators = {
    'T10YIE': '10년 기대 인플레이션율',  # 10년 만기 기대 인플레이션율 (일간)
    'T10Y2Y': '장단기 금리차',  # 10년-2년 국채 수익률 스프레드 (일간)
    'FEDFUNDS': '기준금리',  # 연방기금 금리 (월간)
    'UMCSENT': '미시간대 소비자 심리지수',  # 소비자 신뢰 지수 (월간)
    'UNRATE': '실업률',  # 실업률 (월간)
    'USREC': '경기침체',  # 경기침체 지수 (월간) --> 장단기 금리차를 통해 확인 가능.
    'DGS2': '2년 만기 미국 국채 수익률',  # 2년 만기 국채 수익률 (일간)
    'DGS10': '10년 만기 미국 국채 수익률',  # 10년 만기 국채 수익률 (일간)

    # 추가 지표
    'STLFSI4': '금융스트레스지수',  # 금융 스트레스 지수 (주간)
    #'PCE': '개인 소비 지출',  # 개인 소비 지출 (월간) -> 소비자물가지수(CPI)나 GDP, 실업률, 인플레이션 기대 등 다른 핵심 지표가 이미 전반적 경기 상황을 반영.
    'INDPRO': '산업생산',  # 산업 생산 지수 (월간)
    #'HOUST': '주택 착공',  # 신규 주택 착공 건수 (월간)
    #'UNEMPLOY': '실업자수',  # 실업자의 총 수 (월간)
    'RSAFS': '소매판매',  # 소매판매 지수 (월간)
    'CPIENGSL': '에너지 가격 지수',  # 소비자 물가지수 중 에너지 부문 (월간) -> 소비자물가지수(CPI)나 GDP, 실업률, 인플레이션 기대 등 다른 핵심 지표가 이미 전반적 경기 상황을 반영.
    'AHETPI': '임금 성장률',  # 시간당 평균 임금 성장률 (월간)
    #'PPIACO': '농산물 가격 지수',  # 생산자 물가지수 중 농산물 부문 (월간)
    'CPIAUCSL': '소비자 물가지수',  # 전체 소비자 물가지수 (월간)
    #'CSUSHPINSA': '주택가격지수',  # 케이스-실러 주택 가격 지수 (월간) -> 5년 변동금리 모기지 (MORTGAGE5US): 부동산 시장이 대상 종목(빅테크) 주가 변동에 단기적으로 큰 영향 미치는지 불분명. 단기간(1주일 후) 예측에서는 영향력 제한적.
    #'MORTGAGE30US': '30년 고정금리 모기지',  # 30년 만기 고정금리 모기지 금리 (주간)
    #'MORTGAGE15US': '15년 고정금리 모기지',  # 15년 만기 고정금리 모기지 금리 (주간)
    'MORTGAGE5US': '5년 변동금리 모기지',  # 5년 변동금리 모기지 금리 (주간)
    'DTWEXM': '미국 달러 환율',  # 미국 무역가중 환율 (월간)
    'M2': '통화 공급량 M2',  # M2 통화 공급량 (주간) -> FEDFUNDS나 금리 동향, 달러 인덱스, 금융스트레스지수가 이미 유동성 상황을 대략 파악 가능.
    #'TEDRATE': 'TED 스프레드',  # 3개월 만기 미국 국채와 유로달러 금리 스프레드 (일간) -> FEDFUNDS나 금리 동향, 달러 인덱스, 금융스트레스지수가 이미 유동성 상황을 대략 파악 가능.
    'BAMLH0A0HYM2': '미국 하이일드 채권 스프레드',  # 미국 하이일드 채권과 국채 스프레드 (일간) -> 금융시장 신용위험을 반영하지만, 이미 금융스트레스지수(STLFSI4), 장단기금리차, VIX 등의 지표로 대략적인 위험 선호도나 스트레스 상황 파악 가능.
    'BAMLC0A0CM': '미국 회사채 스프레드',  # 미국 회사채와 국채 스프레드 (일간)
    'BAMLCC0A0CMTRIV': '미국 회사채 수익률',  # 미국 회사채 수익률 (일간)
    #'BAMLCC0A1AAATRIV': '미국 회사채 AAA등급 수익률',  # AAA등급 회사채 수익률 (일간)
    'BAMLCC0A4BBBTRIV': '미국 회사채 BBB등급 수익률',  # BBB등급 회사채 수익률 (일간)
    'BAMLHYH0A0HYM2TRIV': '미국 하이일드 채권 수익률',  # 하이일드 채권 수익률 (일간)
    'BAMLHYH0A3CMTRIV': '미국 하이일드 채권 CCC등급 수익률',  # CCC등급 하이일드 채권 수익률 (일간)
    #'BAMLHE00EHYIEY': '미국 하이일드 채권 기대수익률',  # 하이일드 채권 기대수익률 (일간)
    'TDSP': '가계 부채 비율',  # 가계의 부채 상환 비율을 나타냄 (분기)
    #'A939RX0Q048SBEA': '실질 GDP 성장률',  # 계절 조정된 연간 실질 GDP 성장률 (분기)
    'GDPC1': 'GDP 성장률',  # 실질 국내총생산 성장률, 물가 조정을 반영 (분기)
    #'W019RCQ027SBEA': '정부 지출',  # 정부의 총 지출 금액 (분기)
    #'DRBLACBS': '대출 연체율',  # 기업 대출의 연체율 (분기)

    # 주식시장 관련 추가 지표
    'DJIA': '다우존스 산업평균지수',  # 미국 대형 30개 기업의 주가 평균 (일간)
    'NASDAQCOM': '나스닥 종합지수'  # 나스닥 시장 전체 종합 주가 지수 (일간)
}

yfinance_indicators = {
    'S&P 500 지수': '^GSPC',    # S&P 500 지수: 미국 주식 시장의 대형주 500개로 구성된 지수로, 전체 시장의 대표 지표입니다.
    #'금 가격': 'GC=F',           # 금 가격 (선물): 시장의 안전자산 선호도를 나타내며, 인플레이션 및 경제 불확실성에 민감합니다.
    #'달러 인덱스': 'DX-Y.NYB',    # 달러 인덱스: 미국 달러의 글로벌 통화 대비 상대적 가치를 나타냅니다.

    # 추가 지표
    '나스닥 100': '^NDX',           # 나스닥 100 지수: 나스닥 상장 대형 기술주 100개를 포함하며, 기술주 중심의 시장 흐름을 반영합니다.
    #'S&P 500 ETF': 'SPY',           # S&P 500 추종 ETF: S&P 500 지수를 추종하는 상장지수펀드로, 시장 전체의 동향을 추적합니다.
    #'QQQ ETF': 'QQQ',               # 나스닥 100 추종 ETF: 기술주 중심의 나스닥 100 지수를 추종하는 ETF입니다.
    #'러셀 2000 ETF': 'IWM',         # 러셀 2000 추종 ETF: 중소형주로 구성된 러셀 2000 지수를 추종하며, 경제 성장성을 반영합니다.
    #'다우 존스 ETF': 'DIA',         # 다우 존스 추종 ETF: 다우존스 산업평균지수를 추종하며, 안정적인 대형주의 흐름을 나타냅니다.
    'NYSE FANG+ 지수': '^NYFANG',   # NYSE FANG+ 지수
    'VIX 지수': '^VIX'              # ^VIX (변동성 지수, 공포 지수): 시장의 변동성 기대치를 반영하며, 투자 심리를 측정하는 지표입니다.
}

# 나스닥 100 상위 종목 티커 리스트와 한글 이름
nasdaq_top_100 = [
    ("AAPL", "애플"), ("MSFT", "마이크로소프트"), ("AMZN", "아마존"), ("GOOGL", "구글 A"),
    ("GOOG", "구글 C"), ("META", "메타"), ("TSLA", "테슬라"), ("NVDA", "엔비디아"), ("PYPL", "페이팔"),
    ("ADBE", "어도비"), ("NFLX", "넷플릭스")

    , ("CMCSA", "컴캐스트"), ("PEP", "펩시코"),
    ("INTC", "인텔"), ("CSCO", "시스코"), ("AVGO", "브로드컴"), ("TXN", "텍사스 인스트루먼트"),
    ("QCOM", "퀄컴"), ("COST", "코스트코"), ("AMGN", "암젠")

    , ("CHTR", "차터 커뮤니케이션"),
    ("SBUX", "스타벅스"), ("AMD", "AMD")
    , ("MDLZ", "몬델리즈"), ("INTU", "인트윗"),
    ("ISRG", "인튜이티브 서지컬"), ("BKNG", "부킹홀딩스"), ("ADP", "ADP"),
    ("VRTX", "버텍스"), ("MU", "마이크론"), ("AMAT", "어플라이드 머티리얼즈"), ("REGN", "리제네론"),
    ("LRCX", "램 리서치"), ("KDP", "케우리그 닥터페퍼"), 
    ("FISV.VI", "피서브"),
    ("CSX", "CSX"),
    ("GILD", "길리어드 사이언스"), ("MELI", "메르카도 리브레"), ("SNPS", "시놉시스"),
    ("EA", "일렉트로닉 아츠")
    
    , ("KLAC", "KLA"), ("ADSK", "오토데스크"), ("CTAS", "신타스"),
    ("XEL", "엑셀 에너지"), ("PANW", "팔로알토 네트웍스"), ("ANSS", "앤시스"), ("TEAM", "아틀라시안"),
    ("WDAY", "워크데이"), ("ILMN", "일루미나"), ("DOCU", "도큐사인"),
    ("MRNA", "모더나"), ("IDXX", "아이덱스"), ("ZM", "줌 비디오"), ("DXCM", "덱스컴"),
    ("ROST", "로스 스토어스"), ("CRWD", "크라우드스트라이크"), ("MAR", "메리어트"),
    ("EXC", "엑셀론"), ("MNST", "몬스터 비버리지"), ("PCAR", "PACCAR"), ("LCID", "루시드 모터스"),
    ("ALGN", "얼라인 테크놀로지"), ("BIIB", "바이오젠"),
    ("MTCH", "매치 그룹"), ("OKTA", "옥타"), ("BKR", "베이커 휴즈"), ("ZS", "지스케일러"),
    ("CDNS", "케이던스"), ("CPRT", "코파트"), ("FAST", "패스트널"), ("AEP", "아메리칸 일렉트릭"),
    ("ORLY", "오라일리"), ("VRSK", "버리스크"), ("CTSH", "코그니전트"), ("PDD", "핀둬둬"),
    ("CHKP", "체크포인트"), ("JD", "징둥"), ("NTES", "넷이즈"), ("KHC", "크래프트 하인즈"),
    ("DLTR", "달러 트리"), ("EPAM", "EPAM 시스템즈"), ("SWKS", "스카이웍스"),
    ("NXPI", "NXP 반도체"), ("TTD", "트레이드 데스크"),
    ("PAYX", "페이첵스"), ("BIDU", "바이두"), ("WDC", "웨스턴 디지털"), ("TRMB", "트림블"),
    ("FTNT", "포티넷"), ("VRSN", "베리사인"), ("ASML", "ASML 홀딩"), ("BMRN", "바이오마린"),
    ("LULU", "룰루레몬"), ("EBAY", "이베이"), ("CEG", "컨스텔레이션 에너지"), ("RIVN", "리비안")
]

#수집할 날짜
start_date = '2006-01-01'
end_date = datetime.today().strftime('%Y-%m-%d')

fred_data_frames = []
for code, name in fred_indicators.items():
    
    # 지표별 제공 주기에 따른 요청 주기 설정
    if code in ['FEDFUNDS', 'UMCSENT', 'UNRATE', 'USREC', 'PCE', 'INDPRO',
                'HOUST', 'UNEMPLOY', 'RSAFS', 'CPIENGSL', 'AHETPI', 'PPIACO', 'CPIAUCSL',
                'CSUSHPINSA', 'DTWEXM']:
        frequency = 'm'
    elif code in ['STLFSI4', 'M2', 'MORTGAGE30US', 'MORTGAGE15US', 'MORTGAGE5US']:
        frequency = 'w'
    elif code in ['TDSP', 'A939RX0Q048SBEA', 'GDPC1', 'W019RCQ027SBEA', 'DRBLACBS']:
        frequency = 'q'
    else:
        frequency = 'd'


    url = f'https://api.stlouisfed.org/fred/series/observations'

    params = {
        'series_id': code,
        'api_key': api_key,
        'file_type': 'json',
        'observation_start': start_date,
        'observation_end': end_date,
        'frequency': frequency  
    }
    response = requests.get(url, params=params)


    if response.status_code == 200:
        data = response.json().get('observations', [])
        if data:
            df = pd.DataFrame(data)[['date', 'value']]
            df.columns = ['date', name]  
            df['date'] = pd.to_datetime(df['date']).dt.tz_localize(None)  #타임존 제거
            fred_data_frames.append(df.set_index('date'))
        else:
            print(f"No data found for indicator {name} ({code}).")
    else:
        print(f"Failed to fetch data for indicator {name} ({code}): {response.status_code}")


    #데이터 빈도에 따른 리샘플링 처리

for i, df in enumerate(fred_data_frames):
    if df.empty: #아얘 없을때
        print(f"DataFrame {i} is empty, skipping resampling.")
        continue
    try:
        inferred_freq = df.index.inferred_freq #데이터 빈도 확인
        # 빈도에 따라 일간 데이터로 변환
        if inferred_freq in ['M', 'MS']:  # 월간 데이터
            fred_data_frames[i] = df.resample('D').ffill() #ffill 이전 날짜에서 채우기
        elif inferred_freq in ['W', 'W-FRI']:  # 주간 데이터
            fred_data_frames[i] = df.resample('D').ffill()
        elif inferred_freq in ['Q', 'QS-OCT']:  # 분기 데이터
            fred_data_frames[i] = df.resample('D').ffill()
        elif inferred_freq in ['B']:  # 영업일 데이터
            fred_data_frames[i] = df.resample('D').ffill()
        # else:
        #     print(f"Unknown frequency for DataFrame {i}: {inferred_freq}")
        else:
            fred_data_frames[i] = df.resample('D').ffill()
    except Exception as e:
        print(f"Error processing DataFrame {i}: {e}")
'''
    print(fred_data_frames)
    #리샘플링 후 저장 (테스트)
    if fred_data_frames:
        merged_df = pd.concat(fred_data_frames, axis=1)

        merged_df.to_csv('fred_data.csv',index=True,encoding='utf-8-sig')
        print("데이터가 'fred_data.csv' 파일로 저장되었습니다.")
    else:
        print("저장할 데이터가 없습니다.")
        
'''

# yfinance를 통한 데이터 수집
yfinance_data_frames = []
for name, ticker in yfinance_indicators.items():
    df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)
    if not df.empty:
        # df = df[['Close']].rename(columns={'Close': name})
        # name만 사용하여 컬럼 이름 지정
        df = df[['Close']]
        df.columns = [name]  # rename 대신 직접 columns 할당
        df.index = df.index.tz_localize(None)  
        yfinance_data_frames.append(df)
    else:
        print(f"No data found for indicator {name} ({ticker}).")



'''
#print(yfinance_data_frames)

#(테스트)
if yfinance_data_frames:
    merged_df = pd.concat(yfinance_data_frames, axis=1)

    merged_df.to_csv('fred_data_yf.csv',index=True,encoding='utf-8-sig')
    print("데이터가 'fred_data_yf.csv' 파일로 저장되었습니다.")
else:
    print("저장할 데이터가 없습니다.")

'''

# 나스닥 100 상위 종목 데이터 수집
nasdaq_data_frames = []
for ticker, name in nasdaq_top_100:
    try:
        df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)
        if not df.empty:
            #df = df[['Close']].rename(columns={'Close': f"{name}"})
            df = df[['Close']] #시가(Open) 고가(High) 저가(Low) 종가(Close) 조정종가(Adj Close) 거래량(Volume) 값중 종가만
            df.columns = [name]  # rename 대신 직접 columns 할당
            df.index = df.index.tz_localize(None)
            nasdaq_data_frames.append(df)
    except Exception as e:
        print(f"Error downloading data for {ticker} ({name}): {e}")


'''
#print(yfinance_data_frames)

#(테스트)
if nasdaq_data_frames:
    merged_df = pd.concat(nasdaq_data_frames, axis=1)

    merged_df.to_csv('fred_data_yf_stock.csv',index=True,encoding='utf-8-sig')
    print("데이터가 'fred_data_yf_stock.csv' 파일로 저장되었습니다.")
else:
    print("저장할 데이터가 없습니다.")
'''

# 모든 데이터를 날짜 기준으로 외부 결합하여 하나의 데이터프레임으로 결합
all_data_frames = fred_data_frames + yfinance_data_frames + nasdaq_data_frames
if all_data_frames:
    # 결합
    result_df = pd.concat(all_data_frames, axis=1, join='outer')  # 외부 결합으로 누락된 날짜 보완

    # 결측치 및 비정상적인 값 처리
    result_df.replace('.', pd.NA, inplace=True)  # '.'을 NaN으로 변환
    # result_df = result_df.dropna(subset=['10년 기대 인플레이션율', '장단기 금리차', '금융스트레스지수', '5년 변동금리 모기지'], how='any')  # 해당 열에서 NaN 제거
    result_df = result_df.dropna(subset=['10년 기대 인플레이션율', '장단기 금리차'], how='any')  # 해당 열에서 NaN 제거
    
    # 결측치를 이전 값으로 채움
    result_df.sort_index(inplace=True)
    result_df.ffill(inplace=True)

    # 특정 열에서 결측치가 있는 행 제거
    # result_df = result_df.dropna(subset=['S&P 500 지수'])

    # CSV 파일로 저장
    folder_name = "report"
    folder_path = os.path.join(os.getcwd(), folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"'{folder_name}' 폴더 생성 완료")
        
    try:
        result_df.to_csv(folder_path + "/total.csv", index_label="날짜", encoding='utf-8-sig')
        print(f"Data saved to {folder_path}")
    except PermissionError:
        # 현재 시간을 파일명에 추가하여 새로운 파일 생성
        # from datetime import datetime
        # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # folder_path = f'total_{timestamp}.csv'
        result_df.to_csv(folder_path + "/total.csv", index_label="날짜", encoding='utf-8-sig')
        print(f"Permission denied for original file. Data saved to {folder_path}")
else:
    print("No data collected for any indicators.")

