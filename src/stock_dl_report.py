import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
import json
import os
STOCK_SYMBOL = "GOOGL"
# Evaluation Function
def evaluate_predictions(data, target_columns, forecast_horizon):
    """
    This function compares actual vs. predicted values (for the next 7 days)
    and computes various metrics such as MAE, MSE, RMSE, MAPE, and Accuracy.
    - MAE (Mean Absolute Error): Average absolute error between actual and predicted
      (lower is better, same unit as original data)
    - MSE (Mean Squared Error): Average of squared errors
      (lower is better)
    - RMSE (Root Mean Squared Error): Square root of MSE
      (lower is better, often used with MAE)
    - MAPE (Mean Absolute Percentage Error): Error as a percentage of the actual values
      (lower is better)
    - Accuracy (%): Computed as 100 - MAPE, serving as a simple accuracy measure
    """
    metrics = []
    for col in target_columns:
        predicted_col = f'{col}_Predicted'
        actual_col = f'{col}_Actual'
        # Check if the columns exist
        if predicted_col not in data.columns or actual_col not in data.columns:
            print(f"Skipping {col}: Columns not found in data")
            continue
        # Retrieve predicted and actual values
        predicted = data[predicted_col]
        # Shift the actual values by forecast_horizon days
        # so that today's prediction aligns with actual values 7 days ahead
        actual = data[actual_col].shift(-forecast_horizon)
        # Use only valid (non-NaN) indices
        valid_idx = ~predicted.isna() & ~actual.isna()
        predicted = predicted[valid_idx]
        actual = actual[valid_idx]
        if len(predicted) == 0:
            print(f"Skipping {col}: No valid prediction/actual pairs.")
            continue
        # Calculate metrics
        mae = mean_absolute_error(actual, predicted)
        mse = mean_squared_error(actual, predicted)
        rmse = mse ** 0.5
        mape = (abs((actual - predicted) / actual).mean()) * 100
        accuracy = 100 - mape
        metrics.append({
            'Stock': col,
            'MAE': mae,
            'MSE': mse,
            'RMSE': rmse,
            'MAPE (%)': mape,
            'Accuracy (%)': accuracy
        })
    return pd.DataFrame(metrics)


# Future Rise Analysis
def analyze_rise_predictions(data, target_columns):
    """
    This function looks at the last row of the DataFrame (most recent date),
    compares actual vs. predicted values, and calculates rise/fall information
    and rise probability in percentage.
    """
    last_row = data.iloc[-1]
    results = []
    for col in target_columns:
        last_actual_price = last_row.get(f'{col}_Actual', np.nan)
        predicted_future_price = last_row.get(f'{col}_Predicted', np.nan)
        # Determine rise/fall and rise percentage
        if pd.notna(last_actual_price) and pd.notna(predicted_future_price):
            predicted_rise = predicted_future_price > last_actual_price
            rise_probability = ((predicted_future_price - last_actual_price) / last_actual_price) * 100
        else:
            predicted_rise = np.nan
            rise_probability = np.nan
        results.append({
            'Stock': col,
            'Last Actual Price': last_actual_price,
            'Predicted Future Price': predicted_future_price,
            'Predicted Rise': predicted_rise,
            'Rise Probability (%)': rise_probability
        })
    return pd.DataFrame(results)

# Main Code
# File path setting
folder_path = os.path.join(os.getcwd(), "report")
predicted_file_path = folder_path + f'/predicted_stock.csv'
# 1) Load Data
data = pd.read_csv(predicted_file_path, parse_dates=['날짜'])
# 2) Target columns
# target_columns = ['애플', '마이크로소프트', '아마존', '구글 A', '구글 C', 
#                   '메타', '테슬라', '엔비디아', '페이팔', '어도비', 
#                   '넷플릭스', '컴캐스트', '펩시코', '인텔', '시스코', 
#                   '브로드컴', '텍사스 인스트루먼트', '퀄컴', '코스트코', '암젠', 
#                   '차터 커뮤니케이션', '스타벅스', 'AMD', '몬델리즈', '인트윗', 
#                   '인튜이티브 서지컬', '부킹홀딩스', 'ADP', '버텍스', '마이크론', 
#                   '어플라이드 머티리얼즈', '리제네론', '램 리서치', 
#                   '케우리그 닥터페퍼', '피서브', 'CSX', '길리어드 사이언스', 
#                   '메르카도 리브레', '시놉시스', '일렉트로닉 아츠', 'KLA', 
#                   '오토데스크', '신타스', '엑셀 에너지', '팔로알토 네트웍스', 
#                   '앤시스', '아틀라시안', '워크데이', '일루미나', '도큐사인', 
#                   '모더나', '아이덱스', '줌 비디오', '덱스컴', '로스 스토어스', 
#                   '크라우드스트라이크', '메리어트', '엑셀론', '몬스터 비버리지', 
#                   'PACCAR', '루시드 모터스', '얼라인 테크놀로지', '바이오젠', 
#                   '매치 그룹', '옥타', '베이커 휴즈', '지스케일러', '케이던스', 
#                   '코파트', '패스트널', '아메리칸 일렉트릭', '오라일리', 
#                   '버리스크', '코그니전트', '핀둬둬', '체크포인트', '징둥', 
#                   '넷이즈', '크래프트 하인즈', '달러 트리', 'EPAM 시스템즈', 
#                   '스카이웍스', 'NXP 반도체', '트레이드 데스크', '페이첵스', 
#                   '바이두', '웨스턴 디지털', '트림블', '포티넷', '베리사인', 
#                   'ASML 홀딩', '바이오마린', '룰루레몬', '이베이', 
#                   '컨스텔레이션 에너지', '리비안']
target_columns = [
    '구글 A'
]
forecast_horizon = 7  # predicting 7 days ahead
# 3) Evaluate predictions
evaluation_results = evaluate_predictions(data, target_columns, forecast_horizon)
print("============ Evaluation Results ============")
print(evaluation_results)
# 4) Analyze future rise
rise_results = analyze_rise_predictions(data, target_columns)
print("============ Rise Predictions ============")
print(rise_results)
# 5) Merge DataFrames (evaluation metrics + rise analysis)
final_results = pd.merge(evaluation_results, rise_results, on='Stock', how='outer')
# 6) Sort by rise probability (descending order)
final_results = final_results.sort_values(by='Rise Probability (%)', ascending=False)
# Reorder columns
column_order = [
    'Stock',
    'MAE', 'MSE', 'RMSE', 'MAPE (%)', 'Accuracy (%)',
    'Last Actual Price', 'Predicted Future Price', 'Predicted Rise', 'Rise Probability (%)'
]
final_results = final_results[column_order]
# 8) Save final results to JSON
final_output_path = folder_path + f'/dl_report.json'
final_results_json = final_results.to_json(orient='records', force_ascii=False)
with open(final_output_path, 'w', encoding='utf-8') as f:
    json.dump(json.loads(final_results_json), f, ensure_ascii=False, indent=4)

print(f"\nFinal combined results saved to {final_output_path}\n")
# 9) Print final report
print("=============== Final Report ===============")
print(final_results.to_string(index=False))