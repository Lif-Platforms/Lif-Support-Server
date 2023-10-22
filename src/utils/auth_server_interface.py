import requests
import yaml

# Load config
with open("config.yml", "r") as config:
    contents = config.read()
    configurations = yaml.safe_load(contents)

async def verify_token(username, token):
    # Gets response from auth server
    status = requests.get(f"{configurations['auth-url']}/verify_token/{username}/{token}")
    response_status = status.json()

    # Checks the response from auth server
    if response_status['Status'] == "Successful":
        return True
    
    else: 
        return False
    
async def get_account_email(account): 
    headers = {
        "access-token": configurations['auth-access-token']
    }

    response = requests.get(f"{configurations['auth-url']}/get_account_info/email/{account}", headers=headers)
    raw_response = response.json()

    # Get email from json response
    email = raw_response['email']

    return email