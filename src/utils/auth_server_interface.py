import requests
import yaml

# Load config
with open("config.yml", "r") as config:
    contents = config.read()
    configurations = yaml.safe_load(contents)

async def verify_token(username, token):
    # Gets response from auth server
    status = await requests.get(f"{configurations['auth-url']}/{username}/{token}")
    response_status = status.json()

    # Checks the response from auth server
    if response_status['Status'] == "Successful":
        return True
    
    else: 
        return False