# SmartClimateWebApp

SmartClimateWebApp is a Flask-based web application that leverages Artificial Intelligence (AI) to predict and manage home climate and lighting conditions. By integrating machine learning models, the application provides users with intelligent recommendations for optimal Air Conditioning (AC) temperatures and lighting statuses based on various environmental and temporal factors.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installing Dependencies](#installing-dependencies)
- [Machine Learning Model](#machine-learning-model)
  - [Training the Models](#training-the-models)
  - [Model Explanations](#model-explanations)
  - [Code Complexity](#code-complexity)
- [Developing the Web Application](#developing-the-web-application)
  - [Flask Application Structure](#flask-application-structure)
  - [Database Setup with SQLite3](#database-setup-with-sqlite3)
  - [Web Application Flow](#web-application-flow)
    - [User Registration](#user-registration)
    - [User Login](#user-login)
    - [Dashboard](#dashboard)
  - [Data Handling and Model Integration](#data-handling-and-model-integration)
    - [Passing Data in JSON Format](#passing-data-in-json-format)
    - [Making Predictions](#making-predictions)
    - [Storing Predictions in the Database](#storing-predictions-in-the-database)
- [Running the Application Locally](#running-the-application-locally)
- [Conclusion](#conclusion)
- [License](#license)

## Project Overview

**SmartClimateWebApp** is designed to offer users an intuitive interface for managing and predicting home climate and lighting conditions. The application integrates machine learning models to provide actionable insights, enhancing comfort and energy efficiency within smart homes.

## Features

- **User Authentication:** Secure registration and login system ensuring personalized access.
- **AI-Powered Predictions:** Utilizes trained machine learning models to predict AC temperature and light status.
- **Interactive Dashboard:** User-friendly interface for inputting data, viewing predictions, and accessing prediction history.
- **Prediction History:** Stores and displays past predictions for user reference.
- **SQLite3 Database:** Efficient storage and retrieval of user data and prediction records.

## Installing Dependencies

Ensure you have Python 3.7 or higher installed. Follow the steps below to set up the project:

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/SmartClimateWebApp.git
    cd SmartClimateWebApp
    ```

2. **Create and Activate a Virtual Environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Required Packages:**

    ```bash
    pip install -r requirements.txt
    ```

    **Dependency Explanations:**

    - **Flask (`2.3.2`):** A lightweight web framework for building the application.
    - **Flask-Login (`0.6.2`):** Manages user session and authentication.
    - **Flask-WTF (`1.1.1`):** Integrates WTForms with Flask for form handling.
    - **Flask-SQLAlchemy (`3.0.5`):** ORM for interacting with the SQLite3 database.
    - **Werkzeug (`2.3.2`):** Provides utilities for WSGI applications.
    - **pandas (`1.5.3`):** For data manipulation and analysis.
    - **scikit-learn (`1.2.2`):** Machine learning library used for training models.
    - **numpy (`1.23.5`):** Supports large, multi-dimensional arrays and matrices.
    - **pickle (Built-in):** Serializes and deserializes Python objects, used for saving and loading trained ML models.

## Machine Learning Model

### Training the Models

The application employs two machine learning models:

1. **AC Temperature Predictor (Regression):**
    - **Model:** `RandomForestRegressor`
    - **Purpose:** Predicts optimal AC temperature based on user inputs.
    - **Training Process:** Utilizes features such as `outside_temp`, `room_temp`, `occupancy`, `hour_of_day`, and `weekday` to train the model.

2. **Light Status Predictor (Classification):**
    - **Model:** `RandomForestClassifier`
    - **Purpose:** Predicts whether lights should be turned on or off.
    - **Training Process:** Similar features are used to train the classifier for binary outcomes (`On` or `Off`).

### Model Explanations

- **RandomForestRegressor:** Chosen for its ability to handle non-linear relationships and interactions between features, providing robust predictions for continuous variables like AC temperature.
- **RandomForestClassifier:** Selected for its high accuracy and efficiency in classification tasks, ideal for predicting categorical outcomes such as light status.

### Code Complexity

The training script (`train_models.py`) is designed to be modular and efficient:

- **Data Preprocessing:** Handles missing values, converts timestamps, and extracts relevant features.
- **Model Training:** Separates regression and classification tasks, allowing for independent tuning and evaluation.
- **Serialization:** Uses `pickle` to save trained models for easy integration into the Flask application.

## Developing the Web Application

### Flask Application Structure

The application follows a modular structure for scalability and maintainability:


### Database Setup with SQLite3

- **Configuration:** Defined in `config.py` with `SQLALCHEMY_DATABASE_URI = 'sqlite:///smart_climate.db'`.
- **Models:** Two primary models, `User` and `Prediction`, with appropriate fields and relationships.
- **Initialization:** Tables are automatically created using `db.create_all()` within the application context.

### Web Application Flow

#### User Registration

1. **Access Registration Page:** Navigate to `/register`.
2. **Fill Out Form:** Provide a unique username and password.
3. **Submit:** Form data is validated and stored securely with hashed passwords.
4. **Feedback:** Users receive a success message and are redirected to the login page.

#### User Login

1. **Access Login Page:** Navigate to `/login`.
2. **Enter Credentials:** Provide registered username and password.
3. **Authenticate:** Credentials are verified against the database.
4. **Feedback:** Successful login redirects to the dashboard; failures prompt error messages.

#### Dashboard

1. **Access Dashboard:** Navigate to `/dashboard` after authentication.
2. **Input Data:** Enter `outside_temp`, `room_temp`, `occupancy`, `hour_of_day`, and `weekday`.
3. **Submit Data:** Data is passed in JSON format to the machine learning models.
4. **Receive Predictions:** Display predicted AC temperature and light status.
5. **Store Predictions:** Save prediction results to the database for historical reference.

### Data Handling and Model Integration

#### Passing Data in JSON Format

- **Form Submission:** User inputs are collected via Flask-WTF forms.
- **Data Serialization:** Inputs are converted to NumPy arrays and structured for model prediction.
- **JSON Handling:** Although current implementation uses direct array inputs, JSON can be utilized for enhanced flexibility and API integrations.

#### Making Predictions

- **Model Loading:** Serialized models are loaded during application initialization in `app.py`.
- **Prediction Execution:** Input features are fed into the respective models to generate predictions.
- **Result Interpretation:** Outputs are formatted for user readability (e.g., rounding temperature values, translating classification labels).

#### Storing Predictions in the Database

- **Database Entry:** Each prediction is stored with all input features, predicted values, timestamp, and associated user ID.
- **Relationship Mapping:** Utilizes SQLAlchemy relationships to link predictions to respective users.
- **Historical Access:** Users can view their prediction history on the dashboard, facilitating trend analysis and informed decision-making.

## Running the Application Locally

Follow these steps to set up and run **SmartClimateWebApp** on your local machine:

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/SmartClimateWebApp.git
    cd SmartClimateWebApp
    ```

2. **Create and Activate a Virtual Environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Train the Machine Learning Models:**

    Ensure the dataset `synthetic_ac_light_data.csv` is placed inside the `artifacts/` directory.

    ```bash
    python train_models.py
    ```

5. **Set Environment Variables:**

    It's recommended to set a secure secret key.

    - **On macOS and Linux:**

        ```bash
        export SECRET_KEY='your_secure_secret_key'
        ```

    - **On Windows (Command Prompt):**

        ```cmd
        set SECRET_KEY=your_secure_secret_key
        ```

    - **On Windows (PowerShell):**

        ```powershell
        $env:SECRET_KEY = "your_secure_secret_key"
        ```

6. **Run the Application:**

    ```bash
    python run.py
    ```

7. **Access the Application:**

    Open your web browser and navigate to [http://localhost:5000](http://localhost:5000).

## Conclusion

**SmartClimateWebApp** seamlessly integrates AI with web technologies to provide an intelligent solution for home climate and lighting management. By offering user-friendly interfaces and leveraging robust machine learning models, the application enhances energy efficiency and user comfort. This project serves as a foundation for further advancements in smart home automation and AI-driven environmental controls.

## License

This project is licensed under the [MIT License](LICENSE).
