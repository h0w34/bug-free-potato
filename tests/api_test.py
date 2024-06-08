import requests
import json

# Set the server URL
server_url = 'http://localhost:5000'

# Function to send a GET request
def send_get_request():
    response = requests.get(server_url + '/duties/1/reserves', json={'role' : '3'})
    print(f'GET /duties: {response.status_code} {response.reason}')
    print(response.json())

# Function to send a POST request
def send_post_request():
    data = {'start_date': '2024-06-06', 'end_date': '2024-08-06'}
    response = requests.post(server_url + '/duties', json=data)
    print(f'POST /duties: {response.status_code} {response.reason}')
    print(response.json())

# Function to send a DELETE request
def send_delete_request():
    data = {'start_date': '2024-06-06', 'end_date': '2024-08-06'}
    response = requests.delete(server_url + '/duties', json=data)
    print(f'DELETE /duties: {response.status_code} {response.reason}')
    print(response.json())


def send_put_request():
    data = {
            'replaced_id': 49,
            'replacing_id': 37,
            'reason': {
                'type': 'sick',
                'start_date': '2024-04-03',
                'end_date': '2024-04-13'
            }
        }
    response = requests.put(server_url + '/duties/1', json=data)
    print(f'PUT /duties/1: {response.status_code} {response.reason}')
    print(response.json())

# Prompt user for the type of request
user_choice = input("Choose the type of request (GET, POST, PUT, DELETE): ").upper()

# Perform the selected request
if user_choice == 'GET':
    send_get_request()
elif user_choice == 'POST':
    send_post_request()
elif user_choice == 'DELETE':
    send_delete_request()
elif user_choice == 'PUT':
    send_put_request()
else:
    print("Invalid choice. Please choose GET, POST, or DELETE.")


print('done')
