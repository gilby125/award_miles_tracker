import requests
import psycopg2
from psycopg2 import sql
import math
import json

Sources = ["lifemiles", "virginatlantic", "aeromexico", "american", "delta", "etihad", "united", "emirates", "aeroplan",
           "alaska", "velocity", "qantas"]

# Headers for API request
headers = {"accept": "application/json"}

# Database connection parameters
conn = psycopg2.connect(
    database="xxxxxx",
    user="xxxxx",
    password="xxxx",
    host="xxxxx",
    port="5432"
)

# Create a dynamic UPSERT query with double-quoted field names
upsert_query = sql.SQL("""
        INSERT INTO availability ({}) 
        VALUES ({})
        ON CONFLICT ("ID") DO UPDATE
        SET {}
    """)


def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


# Chunk size for batch inserts
chunk_size = 100

# Iterate through each source
for source in Sources:
    url = f"https://seats.aero/api/availability?source={source}"

    # Fetch data from the API
    response = requests.get(url, headers=headers)
    json_data = response.json()

    # Split json_data into chunks
    num_chunks = math.ceil(len(json_data) / chunk_size)
    chunks = [json_data[i * chunk_size: (i + 1) * chunk_size] for i in range(num_chunks)]

    for chunk in chunks:
        cursor = conn.cursor()

        # Lists to hold values for batch insertion
        column_names = []
        placeholders = []
        values = []

        for item in chunk:
            flattened_route = flatten_dict(item['Route'])

            column_data = {}
            for key in json_data[0]:
                if key == 'Route':
                    for route_key, route_value in flattened_route.items():
                        column_data[route_key] = route_value
                elif key in item:
                    column_data[key] = item[key]
                else:
                    column_data[key] = None

            # Append values for batch insertion
            if not column_names:  # Only do this once for the first item
                column_names = [sql.Identifier(col) for col in column_data.keys()]
                placeholders = [sql.Placeholder()] * len(column_data)
            values.append([data for data in column_data.values()])

        # Create a dynamic UPSERT query with the correct column names and placeholders
        upsert_query_formatted = upsert_query.format(
            sql.SQL(', ').join(column_names),
            sql.SQL(', ').join(placeholders),
            sql.SQL(', ').join([
                col + sql.SQL(" = EXCLUDED.") + col
                for col in column_names
            ])
        )

        # Print the query for debugging
        print(upsert_query_formatted.as_string(conn))

        # Batch insertion using executemany
        cursor.executemany(upsert_query_formatted.as_string(conn), values)

        conn.commit()
        cursor.close()

conn.close()
