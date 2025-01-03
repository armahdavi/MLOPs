# -*- coding: utf-8 -*-
"""
Random forest to predict loan approval 
Accuracy: ~97%

@author: alima
"""

import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import pickle
import warnings

# Turn off warnings
warnings.filterwarnings('ignore')

# Step 1: ETL
project_root = r'C:\Users\alima\code\e2e_loan_approval_predictor'
file_path = os.path.join(project_root, 'data', 'processed\processed_ml.csv')
df = pd.read_csv(file_path)
X = df.iloc[:, 1:-1]
y = df.iloc[:, -1]

# Step 2: 5fold cv over training set (training and testing together)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

## Develop random forest model 
rf = RandomForestClassifier(random_state=42)
param_grid = {
    'n_estimators': [50, 100, 200],         # Number of trees
    'max_depth': [3, 5, 7],                 # Maximum depth of a tree
    'min_samples_split': [2, 5, 10],        # Minimum samples required to split a node
    'min_samples_leaf': [1, 2, 4],          # Minimum samples required to be at a leaf node
}

grid_search = GridSearchCV(
    estimator = rf,
    param_grid = param_grid,
    scoring = 'accuracy',       # Use accuracy as the evaluation metric
    cv = 5,                     # 5-fold cross-validation
    verbose = 1,                # Print progress
    n_jobs = -1                 # Use all available CPU cores
)

grid_search.fit(X_train, y_train)

## Extract best results
results = grid_search.cv_results_

best_index = grid_search.best_index_  # Index of the best parameter combination
best_mean = results['mean_test_score'][best_index]
best_std = results['std_test_score'][best_index]
best_params = grid_search.best_params_


print(f"Best Parameters: {best_params}")
print(f"Mean Score: {best_mean:.4f}, Std Dev: {best_std:.4f}")

# Step 3: Evaluate the test set (basically serv)
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)
test_accuracy = accuracy_score(y_test, y_pred)
print("Test Set Accuracy:", test_accuracy)


# Step 4: Save the model
model_path = os.path.join(os.path.join(project_root, 'data', 'processed', 'random_forest.pkl'))
with open(model_path, 'wb') as file:
    pickle.dump(best_model, file)
print(f"Model saved at: {model_path}")

if __name__ == "__main__":
    print("This script is running directly")
