# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
from geopy.distance import geodesic

# Load dataset
df = pd.read_csv("./uber.csv")

# Display dataset information
print("Dataset Information:\n")
print(df.info())
print("\nDataset Head:\n")
print(df.head())

# 1. Pre-processing the dataset
# Convert 'pickup_datetime' to datetime
df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'], errors='coerce')

# Drop rows with missing values in 'pickup_datetime' and 'fare_amount'
df.dropna(subset=['pickup_datetime', 'fare_amount'], inplace=True)

# Remove negative and extremely high values in 'fare_amount' and 'passenger_count'
df = df[(df['fare_amount'] > 0) & (df['fare_amount'] < 100)]
df = df[(df['passenger_count'] > 0) & (df['passenger_count'] <= 6)]

print(df[['pickup_latitude', 'pickup_longitude', 'dropoff_latitude', 'dropoff_longitude']].isnull().sum())

invalid_rows = df[
    (df['pickup_latitude'] < -90) | (df['pickup_latitude'] > 90) |
    (df['pickup_longitude'] < -180) | (df['pickup_longitude'] > 180) |
    (df['dropoff_latitude'] < -90) | (df['dropoff_latitude'] > 90) |
    (df['dropoff_longitude'] < -180) | (df['dropoff_longitude'] > 180)
]
print(invalid_rows)

lat_min, lat_max = -90.0, 90.0
lon_min, lon_max = -90.0, 90.0

df['pickup_longitude'] = df['pickup_longitude'].apply(lambda x: x if lon_min <= x <= lon_max else df['pickup_longitude'].median())
df['pickup_latitude'] = df['pickup_latitude'].apply(lambda x: x if lat_min <= x <= lat_max else df['pickup_latitude'].median())
df['dropoff_longitude'] = df['dropoff_longitude'].apply(lambda x: x if lon_min <= x <= lon_max else df['dropoff_longitude'].median())
df['dropoff_latitude'] = df['dropoff_latitude'].apply(lambda x: x if lat_min <= x <= lat_max else df['dropoff_latitude'].median())



# Calculate distance between pickup and dropoff points using geopy
def calculate_distance(row):
    try:
        return geodesic(
            (row['pickup_latitude'], row['pickup_longitude']),
            (row['dropoff_latitude'], row['dropoff_longitude'])
        ).km
    except ValueError as e:
        print(f"Error calculating distance for row {row.name}: {e}")
        return None  # or 0, depending on how you want to handle errors

df['distance_km'] = df.apply(calculate_distance, axis=1)

# Drop rows with zero or very high distances
df = df[df['distance_km'] > 0]
df = df[df['distance_km'] < 100]

# Extract date and time features from 'pickup_datetime'
df['pickup_hour'] = df['pickup_datetime'].dt.hour
df['pickup_day'] = df['pickup_datetime'].dt.day
df['pickup_month'] = df['pickup_datetime'].dt.month
df['pickup_year'] = df['pickup_datetime'].dt.year

# Drop unnecessary columns
df.drop(['key', 'pickup_datetime', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude'], axis=1, inplace=True)

# 2. Identify outliers
# Visualize 'fare_amount' and 'distance_km' distributions
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
sns.boxplot(df['fare_amount'])
plt.title('Boxplot of Fare Amount')
plt.subplot(1, 2, 2)
sns.boxplot(df['distance_km'])
plt.title('Boxplot of Distance (km)')
plt.show()

# Remove outliers based on z-scores for 'fare_amount' and 'distance_km'
from scipy import stats
df = df[(np.abs(stats.zscore(df[['fare_amount', 'distance_km']])) < 3).all(axis=1)]

# 3. Check correlation
# Plot correlation heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix")
plt.show()

# 4. Implement Linear Regression and Random Forest Regression models
# Define features and target variable
X = df.drop('fare_amount', axis=1)
y = df['fare_amount']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Linear Regression model
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

# Initialize and train the Random Forest Regression model
random_forest_model = RandomForestRegressor(n_estimators=100, random_state=42)
random_forest_model.fit(X_train, y_train)

# 5. Evaluate the models and compare their respective scores like R2, RMSE, etc.
# Predict on test set
y_pred_linear = linear_model.predict(X_test)
y_pred_rf = random_forest_model.predict(X_test)

# Calculate evaluation metrics
def evaluate_model(y_true, y_pred):
    r2 = r2_score(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    return r2, rmse

# Linear Regression evaluation
r2_linear, rmse_linear = evaluate_model(y_test, y_pred_linear)
print("Linear Regression:")
print(f"R^2 Score: {r2_linear:.4f}")
print(f"RMSE: {rmse_linear:.4f}")

# Random Forest Regression evaluation
r2_rf, rmse_rf = evaluate_model(y_test, y_pred_rf)
print("\nRandom Forest Regression:")
print(f"R^2 Score: {r2_rf:.4f}")
print(f"RMSE: {rmse_rf:.4f}")

# Visualization of predicted vs actual fare amount for both models
plt.figure(figsize=(14, 6))

# Linear Regression Predictions
plt.subplot(1, 2, 1)
plt.scatter(y_test, y_pred_linear, alpha=0.5, color='blue')
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')
plt.xlabel("Actual Fare")
plt.ylabel("Predicted Fare")
plt.title("Linear Regression: Actual vs Predicted Fares")

# Random Forest Predictions
plt.subplot(1, 2, 2)
plt.scatter(y_test, y_pred_rf, alpha=0.5, color='green')
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')
plt.xlabel("Actual Fare")
plt.ylabel("Predicted Fare")
plt.title("Random Forest: Actual vs Predicted Fares")

plt.show()

# Bar plot of R2 and RMSE comparison
metrics = pd.DataFrame({
    'Model': ['Linear Regression', 'Random Forest'],
    'R^2 Score': [r2_linear, r2_rf],
    'RMSE': [rmse_linear, rmse_rf]
})

plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
sns.barplot(x='Model', y='R^2 Score', data=metrics, palette='viridis')
plt.title("R^2 Score Comparison")

plt.subplot(1, 2, 2)
sns.barplot(x='Model', y='RMSE', data=metrics, palette='viridis')
plt.title("RMSE Comparison")
plt.show()
