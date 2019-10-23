import requests

#curl -X POST http://0.0.0.0:8000/predict -H 'Conent-Type: application/json' -d '{"text": "I Am Nigerain and dream of being president of FIFA "}'

response = requests.post('http://0.0.0.0:8000/api/predict', json={"test":"I Am Nigerain and dream of being president of FIFA "}
if response.ok:
    print (response.json())