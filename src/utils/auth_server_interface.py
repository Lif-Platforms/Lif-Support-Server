import requests

def verify_token(username, token):
    # Gets response from auth server
    status = requests.get(f"http://localhost:8002/verify_token/{username}/{token}")
    response_status = status.json()

    # Checks the response from auth server
    if response_status['Status'] == "Successful":
        return True
    
    else: 
        return False