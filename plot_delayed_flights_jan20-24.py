import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Establishing the connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Bootcamp24",
    database="aviation.data"
)

# Creating a cursor object using the cursor() method
cursor = connection.cursor()

# Analysis: Plotting the distribution of all flight statuses (early, on time, late) in 10-minute increments
query_status = """
    SELECT status
    FROM flights
    WHERE status <= 200;
"""

# Execute the query and convert the results into a DataFrame
cursor.execute(query_status)
status_data = cursor.fetchall()
status_df = pd.DataFrame(status_data, columns=['status_minutes'])

# Plotting the distribution of flight statuses in 10-minute increments
plt.figure(figsize=(10, 6))
plt.hist(status_df['status_minutes'], bins=range(status_df['status_minutes'].min() - 10, status_df['status_minutes'].max() + 10, 10), edgecolor='black', color='skyblue')
plt.xlabel('Status Minutes (in 10-minute increments)')
plt.ylabel('Number of Flights')
plt.title('Distribution of Flight Statuses (Early, On Time, Late) in 10-Minute Buckets')
plt.grid(axis='y')
plt.show()

# Close the cursor and connection
cursor.close()
connection.close()