# Step 1: Import the required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.decomposition import PCA

# Step 2: Load the dataset
# Replace 'emails.csv' with the path to the dataset file.
df = pd.read_csv("emails.csv")

# Step 3: Data Exploration
print("Dataset Shape:", df.shape)
print("Dataset Sample:\n", df.head())

# Check for missing values
print("Missing values:\n", df.isnull().sum().sum())

# Step 4: Data Preprocessing
# Dropping the first column as it is just an email identifier
df.drop(df.columns[0], axis=1, inplace=True)

# Separate features and target variable
X = df.iloc[:, :-1]
y = df.iloc[:, -1]

# Step 5: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Step 6: Feature Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Step 7: Dimensionality Reduction for Visualization
# Reduce dimensions to 2 for plotting using PCA
pca = PCA(n_components=2)
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)

# Visualizing the data distribution after PCA
plt.figure(figsize=(10, 6))
sns.scatterplot(x=X_train_pca[:, 0], y=X_train_pca[:, 1], hue=y_train, palette="coolwarm", s=60)
plt.title("Data Distribution After PCA")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.show()

# Step 8: Model Training and Evaluation - KNN
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_scaled, y_train)
y_pred_knn = knn.predict(X_test_scaled)

# Step 9: Model Training and Evaluation - SVM
svm = SVC(kernel='linear', random_state=42)
svm.fit(X_train_scaled, y_train)
y_pred_svm = svm.predict(X_test_scaled)

# Step 10: Performance Analysis

# Function to display performance metrics
def display_metrics(y_true, y_pred, model_name):
    print(f"--- {model_name} ---")
    print("Accuracy:", accuracy_score(y_true, y_pred))
    print("Classification Report:\n", classification_report(y_true, y_pred))
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="YlGnBu", cbar=False, xticklabels=['Not Spam', 'Spam'], yticklabels=['Not Spam', 'Spam'])
    plt.title(f"{model_name} Confusion Matrix")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.show()

# Display metrics for KNN
display_metrics(y_test, y_pred_knn, "K-Nearest Neighbors")

# Display metrics for SVM
display_metrics(y_test, y_pred_svm, "Support Vector Machine")

# Step 11: Compare Model Performance Using a Bar Chart
knn_accuracy = accuracy_score(y_test, y_pred_knn)
svm_accuracy = accuracy_score(y_test, y_pred_svm)
model_names = ['K-Nearest Neighbors', 'Support Vector Machine']
accuracies = [knn_accuracy, svm_accuracy]

plt.figure(figsize=(8, 5))
sns.barplot(x=model_names, y=accuracies, palette="viridis")
plt.title("Comparison of Model Accuracies")
plt.xlabel("Model")
plt.ylabel("Accuracy")
plt.ylim(0, 1)
plt.show()

# Step 12: Add Predictions to the Original DataFrame

# Compute predictions on the entire dataset (scaled)
X_scaled = scaler.transform(X)  # Scaling the full feature set for consistency
df['KNN_Prediction'] = knn.predict(X_scaled)
df['SVM_Prediction'] = svm.predict(X_scaled)

# Display the updated DataFrame with predictions
print("Updated DataFrame with Predictions:")
print(df.head())
