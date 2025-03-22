import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
import json
import os


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
predicted_file_path = folder_path + '/predicted_stock.csv'
# 1) Load Data
data = pd.read_csv(predicted_file_path, parse_dates=['날짜'])
# 2) Target columns
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
final_output_path = folder_path + '/final_stock_analysis.json'
final_results_json = final_results.to_json(orient='records', force_ascii=False)
with open(final_output_path, 'w', encoding='utf-8') as f:
    json.dump(json.loads(final_results_json), f, ensure_ascii=False, indent=4)

print(f"\nFinal combined results saved to {final_output_path}\n")
# 9) Print final report
print("=============== Final Report ===============")
print(final_results.to_string(index=False))