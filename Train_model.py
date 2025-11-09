# ----------------------------------------
# Train and Save Random Forest Model
# ----------------------------------------

import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_absolute_error

# 1. Load Dataset
df = pd.read_csv("House Price Prediction Dataset.csv")

# Drop Id column (not needed for prediction)
df = df.drop(columns=['Id'], errors='ignore')

# 2. Define Features and Target
TARGET = 'Price'
FEATURES = ['Area', 'Bedrooms', 'Bathrooms', 'Floors', 'YearBuilt', 'Location', 'Condition', 'Garage']

X = df[FEATURES]
y = df[TARGET]

# 3. Identify Feature Types
categorical_features = ['Location', 'Condition', 'Garage']
numerical_features = [col for col in FEATURES if col not in categorical_features]

# 4. Preprocessing Pipeline
numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

# 5. Model Definition
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    max_depth=15
)

# 6. Combine Preprocessor + Model
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', model)
])

# 7. Train/Test Split & Fit
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
pipeline.fit(X_train, y_train)

# 8. Evaluate Model
y_pred = pipeline.predict(X_test)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print(f"Model trained successfully!")
print(f"R² Score: {r2:.3f}")
print(f"Mean Absolute Error: ${mae:,.2f}")

# 9. Save Model + Feature Names
model_data = {
    'model': pipeline,
    'features': FEATURES
}

with open('random_forest_model.pkl', 'wb') as file:
    pickle.dump(model_data, file)

print("Model and feature list saved as random_forest_model.pkl")
