import requests

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc3NTU2OTA3fQ.Flhk0uWMRiZXDWKJltC-CsSMwoTYlLgCRH7At8aA6dg"
headers = {'Authorization': f'Bearer {token}'}

# Test deposit
data = {'amount': 100.00, 'description': 'Test deposit'}
response = requests.post('http://localhost:8001/wallet/deposit', json=data, headers=headers)
print('Deposit:', response.json())

# Test balance again
response = requests.get('http://localhost:8001/wallet/balance', headers=headers)
print('Balance after deposit:', response.json())

# Test withdraw
data = {'amount': 20.00, 'description': 'Test withdraw'}
response = requests.post('http://localhost:8001/wallet/withdraw', json=data, headers=headers)
print('Withdraw:', response.json())

# Test admin users
response = requests.get('http://localhost:8001/admin/users', headers=headers)
print('Admin users:', response.json())