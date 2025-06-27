import requests
import json

def test_chat_endpoint():
    url = "http://localhost:5000/chat"
    data = {
        "question": "Tell me about Lucas",
        "role": "recruiter"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        
        if response.status_code == 200:
            print("Success!")
            print(f"Response: {response.json()}")
        else:
            print(f"Error Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    test_chat_endpoint() 