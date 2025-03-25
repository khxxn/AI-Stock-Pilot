import json
from openai import OpenAI
import os
from dotenv import load_dotenv

STOCK_SYMBOL = "GOOGL"
# DeepSeek API 설정
load_dotenv()
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEEPSEEK_URL = "https://api.deepseek.com"
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_URL)

def load_news_data(news_path):
    """최근 20개 종목 뉴스 JSON 파일 로드"""
    with open(news_path, 'r', encoding='utf-8') as f:
        news_data = json.load(f)
    return news_data
def load_price_data(price_data_path):
    """주가 데이터 JSON 파일 로드"""
    with open(price_data_path, 'r', encoding='utf-8') as f:
        price_data = json.load(f)
    return price_data

def load_stock_info(stock_info_path):
    """기업 정보 JSON 파일 로드"""
    with open(stock_info_path, 'r', encoding='utf-8') as f:
        stock_info = json.load(f)
    return stock_info

def get_deepseek_recommendation(stock_data, news_data, stock_info):
    """DeepSeek API 호출: 주가 데이터 + 뉴스 분석 + 기업 정보"""
    system_prompt = f"""
    [Role]
    You are a seasoned Wall Street analyst with 20 years of experience, specializing in ultra-short-term trading decisions.

    [Stock Analysis]
    - MAE (Mean Absolute Error): Average absolute error between actual and predicted
      (lower is better, same unit as original data)
    - MSE (Mean Squared Error): Average of squared errors
      (lower is better)
    - RMSE (Root Mean Squared Error): Square root of MSE
      (lower is better, often used with MAE)
    - MAPE (Mean Absolute Percentage Error): Error as a percentage of the actual values
      (lower is better)
    - Accuracy (%): Computed as 100 - MAPE, serving as a simple accuracy measure
    - Rise_probability (%): represents the percentage change of the predicted future price relative to the last actual price. In other words, it represents the predicted price increase rate as a percentage.
    Stock: {STOCK_SYMBOL}
    Last Actual Price: {stock_data['Last Actual Price']}
    Predicted Future Price: {stock_data['Predicted Future Price']}
    Rise Probability (%): {stock_data['Rise Probability (%)']}%
    Accuacy (%): {stock_data['Accuracy (%)']}%
    Technical Indicators: MAE = {stock_data['MAE']}, RMSE = {stock_data['RMSE']}, MAPE = {stock_data['MAPE (%)']}%
    Note:  Note: These predictions are derived from a deep learning model using a Transformer architecture that predicts stock prices one week into the future. Consider the Transformer architecture prediction as one input among many for your analysis.

    [Recent Stock-Related News (Top 20)]
    {json.dumps(news_data, indent=4)}

     [Company Information]
    {json.dumps(stock_info, indent=4)}

    [Stock Price Data]
    {json.dumps(price_data, indent=4)}

    [Task]
    Analyze the provided stock data and predict whether the stock will rise or fall in price over the next week. Provide a brief justification for your prediction, and recommend whether to buy, hold, or sell the stock.
    """
    user_prompt = "Provide a one-week prediction and recommendation."
    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}]

    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=messages,
    )
    reasoning_content = response.choices[0].message.reasoning_content
    content = response.choices[0].message.content
    print('resoning_content : ', reasoning_content)
    print('===========================')
    print('content : ', content)

#######################
# Main Code
#######################
# File path setting
folder_path = os.path.join(os.getcwd(), "report")
news_path = folder_path + f'/{STOCK_SYMBOL}_news.json'
stock_data_path = folder_path + f'/final_{STOCK_SYMBOL}_analysis.json'
stock_info_path = folder_path + f'/{STOCK_SYMBOL}_info.json'
price_data_path = folder_path + f'/{STOCK_SYMBOL}_Moving_Average.json'

# 데이터 로드
news_data = load_news_data(news_path)
stock_data_list = json.load(open(stock_data_path, 'r', encoding='utf-8'))
stock_info = load_stock_info(stock_info_path)
price_data = load_price_data(price_data_path)

# 첫 번째 종목 데이터 사용 (필요에 따라 다른 종목 선택 가능)
if stock_data_list:
    stock_data = stock_data_list[0]
    # 결과 저장 및 출력
    get_deepseek_recommendation(stock_data, news_data, stock_info)
else:
    print("final_stock_analysis.json 파일에 데이터가 없습니다.")