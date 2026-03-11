import pandas as pd

import psycopg2
from psycopg2 import extras

def save_to_postgres(data_list):
        # Connect to PostgreSQL
        conn = {
            "dbname": "flipkart_2026",
            "user": 'postgres',
            "password": input("Enter your PostgreSQL password: "),
            "host": 'localhost',
            "port": '5432'
        }

        try:
            conn = psycopg2.connect(**conn)
            cursor = conn.cursor()

            # Create table if it doesn't exist
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS laptops (
                id SERIAL PRIMARY KEY,
                name TEXT,
                price TEXT,
                rating TEXT,
                ratings_count TEXT,
                reviews_count TEXT,
                features TEXT[],
                original_price TEXT,
                discount TEXT
            );

            ''')
            #Insert data into the table
            insert_query = """
            INSERT INTO laptops (name, price, rating, ratings_count, reviews_count, features, original_price, discount) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            
            for item in data_list:
                cursor.execute(insert_query, (
                    item["Title"],
                    item["Current_Price"],
                    item["Rating"],
                    item["Ratings_Count"],
                    item["Reviews_Count"],
                    item["Features"].split(" | "),
                    item["Original_Price"],
                    item["Discount"]
                ))

            conn.commit()
            cursor.close()
            conn.close()
            print("Data saved to PostgreSQL successfully!")

            df= pd.DataFrame(data_list)
            print(df.head())
        except Exception as e:
            print(f"An error occurred: {e}")

def save_to_csv(data_list, filename="flipkart_laptops.csv"):
    df = pd.DataFrame(data_list)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename} successfully!")
