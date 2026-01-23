import requests
import json
import sys

def test_api():
    url = "http://localhost:8000/api/ingest/text"
    payload = {"text": "Project Beta: Finish the API testing via python script"}
    headers = {"Content-Type": "application/json"}
    
    print(f"Sending POST request to {url}...")
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        print("Response Body:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            print("\nSUCCESS: API call returned 200 OK")
        else:
            print(f"\nFAILURE: API call returned {response.status_code}")
            
    except Exception as e:
        print(f"\nERROR: Failed to connect or receive response: {e}")

if __name__ == "__main__":
    test_api()
