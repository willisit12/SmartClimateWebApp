import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, accuracy_score
import pickle

# Load the dataset containing synthetic AC and lighting data
dataset = pd.read_csv('train_data/training_dataset.csv')

# Inspect missing values in the target columns (ac_temp and light_status)
print("Inspecting missing data...")
print(dataset[['ac_temp', 'light_status']].isna().sum())

# Remove records with missing target values
dataset_cleaned = dataset.dropna(subset=['ac_temp', 'light_status'])

# Ensure the timestamp column is in datetime format
dataset_cleaned['timestamp'] = pd.to_datetime(dataset_cleaned['timestamp'])

# Derive additional temporal features from the timestamp
dataset_cleaned['hour_of_day'] = dataset_cleaned['timestamp'].dt.hour  # Hour (0-23)
dataset_cleaned['weekday'] = dataset_cleaned['timestamp'].dt.dayofweek  # Weekday (0=Monday, 6=Sunday)

# Define feature variables and target labels
features = dataset_cleaned[['outside_temp', 'room_temp', 'number_of_people', 'hour_of_day', 'weekday']]
target_ac_temp = dataset_cleaned['ac_temp']  # Target for AC temperature prediction (regression)
target_light_status = dataset_cleaned['light_status']  # Target for light status prediction (classification)

# Split the data into training and testing subsets
X_train, X_test, y_ac_temp_train, y_ac_temp_test, y_light_train, y_light_test = train_test_split(
    features, target_ac_temp, target_light_status, test_size=0.3, random_state=42
)

# Initialize and train the regression model for predicting AC temperature
ac_temp_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
ac_temp_regressor.fit(X_train, y_ac_temp_train)

# Initialize and train the classification model for predicting light status
light_status_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
light_status_classifier.fit(X_train, y_light_train)

# Generate predictions using the trained regression model
ac_temp_predictions = ac_temp_regressor.predict(X_test)

# Generate predictions using the trained classification model
light_status_predictions = light_status_classifier.predict(X_test)

# Evaluate the performance of the regression model
rmse_ac_temp = mean_squared_error(y_ac_temp_test, ac_temp_predictions, squared=False)
print(f'AC Temperature Prediction RMSE: {rmse_ac_temp:.2f}')

# Evaluate the performance of the classification model
accuracy_light_status = accuracy_score(y_light_test, light_status_predictions)
print(f'Light Status Prediction Accuracy: {accuracy_light_status:.2%}')

# Save the trained regression model to a file using pickle
with open('model/ac_temperature_regressor.pkl', 'wb') as ac_temp_file:
    pickle.dump(ac_temp_regressor, ac_temp_file)

# Save the trained classification model to a file using pickle
with open('model/light_status_classifier.pkl', 'wb') as light_status_file:
    pickle.dump(light_status_classifier, light_status_file)

print("Models have been successfully saved.")
