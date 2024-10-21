import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np


def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.getenv("DB_PASSWORD", "Bootcamp24"),  
            database="aviation.data"  
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def load_data(connection):
    try:
        query = """
            SELECT `flight_date`, `flight_number`, `tail_number`, `destination_airport`,
                   `scheduled_departure_time`, `actual_departure_time`, `departure_delay_minutes`,
                   `delay_carrier_minutes`, `delay_weather_minutes`, `delay_nas_minutes`,
                   `delay_security_minutes`, `delay_late_aircraft_minutes`
            FROM `flights_bigdata`  # Ensure this table exists in the aviation_data database
        """
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=[
            'flight_date', 'flight_number', 'tail_number', 'destination_airport',
            'scheduled_departure_time', 'actual_departure_time', 'departure_delay_minutes',
            'delay_carrier_minutes', 'delay_weather_minutes', 'delay_nas_minutes',
            'delay_security_minutes', 'delay_late_aircraft_minutes'
        ])
        return df
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return pd.DataFrame()

def perform_analysis(df):
  
    df['flight_date'] = pd.to_datetime(df['flight_date'])
    df['scheduled_departure_time'] = pd.to_datetime(df['scheduled_departure_time'], format='%H:%M:%S', errors='coerce').dt.time
    df['actual_departure_time'] = pd.to_datetime(df['actual_departure_time'], format='%H:%M:%S', errors='coerce').dt.time


    print("Sample of the dataset:")
    print(df.head())


    print("Full dataset:")
    print(df.to_string())

 
    def delay_category(minutes):
        if minutes <= 15:
            return 'Green'  
        elif 15 < minutes <= 60:
            return 'Yellow'  
        else:
            return 'Red'  

    df['delay_category'] = df['departure_delay_minutes'].apply(delay_category)


    delay_category_counts = df['delay_category'].value_counts().reset_index()
    delay_category_counts.columns = ['Delay Category', 'Number of Flights']

  
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Delay Category', y='Number of Flights', data=delay_category_counts, palette=['green', 'yellow', 'red'])
    plt.title('Flight Delays Categorized by Traffic Light System')
    plt.xlabel('Delay Category')
    plt.ylabel('Number of Flights')
    plt.show()

    delay_types = [
        'delay_carrier_minutes', 'delay_weather_minutes', 'delay_nas_minutes',
        'delay_security_minutes', 'delay_late_aircraft_minutes'
    ]
    df_delay_summary = df[delay_types].sum().reset_index()
    df_delay_summary.columns = ['Delay Type', 'Total Minutes']


    plt.figure(figsize=(10, 6))
    sns.barplot(x='Delay Type', y='Total Minutes', data=df_delay_summary, palette='viridis')
    plt.title('Total Delay by Type')
    plt.xlabel('Delay Type')
    plt.ylabel('Total Delay (Minutes)')
    plt.xticks(rotation=45)
    plt.show()

def predict_next_year_delays(df):
   
    df['year'] = df['flight_date'].dt.year
    delay_features = ['delay_carrier_minutes', 'delay_weather_minutes', 'delay_nas_minutes', 'delay_security_minutes', 'delay_late_aircraft_minutes']
    df['total_delay'] = df[delay_features].sum(axis=1)


    df_filtered = df[['year'] + delay_features + ['total_delay']].dropna()
    X = df_filtered[['year'] + delay_features]
    y = df_filtered['total_delay']

   
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

 
    model = LinearRegression()
    model.fit(X_train, y_train)

 
    next_year = np.array([[2025] + [0] * len(delay_features)]) 
    predicted_delay = model.predict(next_year)
    print(f"Predicted total delay for the year 2025: {predicted_delay[0]} minutes")


    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error of the model: {mse}")

def main():
    connection = connect_to_db()
    if connection:
        df = load_data(connection)
        if not df.empty:
            perform_analysis(df)
            predict_next_year_delays(df)
        connection.close()

if __name__ == "__main__":
    main()
