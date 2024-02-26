from pprint import pprint

import pandas as pd
import requests
import random
from datetime import datetime, timezone


def generate_random_data(num_objects=1):
    road_states = ['dry', 'wet', 'icy', 'snowy', 'slippery']
    data = []
    for _ in range(num_objects):
        obj = {
            "road_state": random.choice(road_states),
            "agent_data": {
                "accelerometer": {
                    "x": random.uniform(-10, 10),
                    "y": random.uniform(-10, 10),
                    "z": random.uniform(-10, 10)
                },
                "gps": {
                    "latitude": random.uniform(-90, 90),
                    "longitude": random.uniform(-180, 180)
                },
                "timestamp": datetime.now(timezone.utc).isoformat().replace(" ", "")
            }
        }
        data.append(obj)
    return data


def send_post_request(url, data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)
    return response


def get_request(url):
    response = requests.get(url)
    print("Fetching current data...")
    if response.status_code == 200:
        data = response.json()
        print("Current data:")
        df = pd.DataFrame(data)
        pprint(df)
    else:
        print(f"Failed to fetch data, status code: {response.status_code}")
        data = []
    return data


def delete_request(url, object_id):
    delete_url = f"{url}/{object_id}"
    response = requests.delete(delete_url)
    return response


def update_request(url, object_id, data):
    update_url = f"{url}/{object_id}"
    headers = {'Content-Type': 'application/json'}
    response = requests.put(update_url, json=data, headers=headers)
    return response


def delete_all_objects(url, data):
    print("Deleting all objects...")
    for obj in data:
        response = delete_request(url, obj['id'])
        print(f"Deleted object id {obj['id']}, status code: {response.status_code}")


def main():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    url = 'http://127.0.0.1:8000/processed_agent_data'

    print("\n1-3. Generating random data...")
    num_objects = 3
    for _ in range(num_objects):
        print(f"\nSending POST request with random data...", end=" ")
        response = send_post_request(url, generate_random_data())
        print(f"Status code: {response.status_code}")
        get_request(url)

    print("\n4. Fetching current data...")
    data = get_request(url)

    print("\n5. Deleting second object...", end=" ")
    if len(data) >= 2:
        response = delete_request(url, data[1]['id'])
        print(f"Status code: {response.status_code}")

    print("\n6. Fetching current data...")
    data = get_request(url)

    print("\n7.Updating last object...", end=" ")
    if data:
        data_update = generate_random_data()[0]
        response = update_request(url, data[-1]['id'], data_update)
        print(f"Status code: {response.status_code}")

    data = get_request(url)

    print()
    delete_all_objects(url, data)

    get_request(url)


if __name__ == "__main__":
    main()
