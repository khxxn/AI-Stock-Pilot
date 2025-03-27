# 📈 AI STOCK PILOT (주가 예측 및 구매판단 프로그램)

최신버전(ipynb) 다운로드: v1.0.0 [다운로드]()

## 📃프로젝트 설명
AI STOCK PILOT은 딥러닝과 생성형 AI를 활용하여 주가를 예측하고, 예측 결과를 바탕으로 주식 매수/매도 판단을 지원하는 프로그램입니다. 특히 Transformer 모델을 사용하여 시계열 데이터인 주가 예측의 정확도를 높이고, DeepSeek API를 통해 투자 판단의 근거를 생성합니다.

### ⚙개발 환경
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=white)<br/>
![Google Colab](https://img.shields.io/badge/Google%20Colab-%23F9A825.svg?style=for-the-badge&logo=googlecolab&logoColor=white)<br/><br/>
- 주요 라이브러리:
    - 데이터 처리: pandas, numpy
    - 주가 데이터 수집: yfinance
    - 외부 API 호출: requests (FRED API 등)
    - 생성형 AI API: openai (DeepSeek API 활용)
    - 머신러닝/딥러닝: tensorflow (Keras)
        - 모델 구축: tensorflow.keras.models, tensorflow.keras.layers (Input, Dense, Dropout, LayerNormalization, MultiHeadAttention, Add, GlobalAveragePooling1D)
        - 최적화: tensorflow.keras.optimizers.Adam
    - 데이터 스케일링: sklearn.preprocessing.MinMaxScaler
    - 모델 평가: sklearn.metrics (mean_absolute_error, mean_squared_error)
    - 시각화: matplotlib.pyplot, matplotlib.dates

## 📂파일 구조
### AI-Stock-Pilot/
├── report/<br/>
│   ├── dl_report.json<br/>
│   ├── predicted_stock.csv<br/>
│   ├── total.csv<br/>
│   └── ...<br/>
├── src/<br/>
│   ├── fred.py<br/>
│   ├── stock_analyzer.py<br/>
│   ├── stock_dl_report.py<br/>
│   ├── stock_movingaverage.py<br/>
│   ├── transformer.ipynb<br/>
│   ├── yf_companyinfo.py<br/>
│   └── yf_newsdata.py<br/>
├── .gitignore<br/>
├── README.md<br/>
└── main.ipynb

## 📌프로그램 설명
AI STOCK PILOT은 주식 시장 데이터를 다양한 소스로부터 수집하고, 딥러닝 모델인 Transformer를 사용하여 일주일 후의 주가 변동을 예측합니다. 예측된 주가 정보를 바탕으로 생성형 AI인 DeepSeek API를 활용하여 주식 매수/매도 판단을 생성하고, 사용자에게 제공합니다.
### 주요 기능
- 데이터 수집:
    - 주가 데이터: yfinance 라이브러리를 통해 야후 파이낸스에서 주식 가격 데이터를 수집합니다.
    - 경제 지표 데이터: requests 라이브러리를 사용하여 FRED API로부터 경제 지표 데이터를 수집합니다 (선택 사항).
    - 기업 정보 및 뉴스: yfinance 라이브러리를 통해 기업 정보 및 뉴스 데이터를 수집합니다.
- 데이터 전처리: 수집된 데이터를 pandas와 numpy를 이용하여 분석에 용이하도록 가공합니다. MinMaxScaler를 사용하여 데이터를 스케일링합니다.
- 딥러닝 모델 (Transformer): 시계열 데이터 처리에 강력한 성능을 보이는 Transformer 모델을 tensorflow와 keras를 이용하여 구현하고 학습합니다.
- 주가 예측: 학습된 Transformer 모델을 사용하여 일주일 후의 주가를 예측합니다.
- 생성형 AI 기반 판단 (DeepSeek API): openai 라이브러리를 통해 DeepSeek API를 호출하여 주가 예측 결과와 관련 뉴스를 분석하고, 매수/매도 판단을 생성합니다.
- 결과 보고 및 시각화: 예측 결과와 매수/매도 판단을 matplotlib 등의 라이브러리를 이용하여 시각화하고, stock_dl_report.py를 통해 보고서 형태로 제공합니다.

### 사용 방법

1. main.ipynb 파일을 Google Colab에서 엽니다.
2. API 키 입력: DeepSeek API를 사용하기 위해 Google Colab에 API 키를 등록합니다.<br/>![Image](https://github.com/user-attachments/assets/cc570fa6-34a2-4c11-b021-41d3dba47ebd)
3. 런타임 유형 GPU로 설정합니다.
4. 데이터 설정: 분석하려는 주식 종목, 기간 등 필요한 데이터를 노트북 내에서 설정합니다. (fred_indicators, yfinance_indicators, nasdaq_top_100, STOCK_SYMBOL, target_columns, economic_features)
5. 노트북 순차 실행: transformer.ipynb 파일을 위에서부터 순서대로 실행하여 데이터 수집, 모델 학습, 예측 및 판단 과정을 진행합니다.
6. 결과 확인: 예측된 주가 정보와 DeepSeek API의 매수/매도 판단 결과를 확인하고, 생성된 보고서를 분석합니다.