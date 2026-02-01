import requests

# GET запрос
print("=== Testing GET /api/students/ ===")
response = requests.get('http://127.0.0.1:8000/api/students/')
print(response.json())

print("\n=== Testing POST /api/attendance/ ===")
# POST запрос
data = {
    "student_id": 1,
    "date": "2026-01-18",
    "status": "present"
}
response = requests.post('http://127.0.0.1:8000/api/attendance/', json=data)
print(response.json())