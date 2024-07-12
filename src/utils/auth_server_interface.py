import requests

# Allow main script to set the config
def set_config(config):
    global configurations
    configurations = config

async def verify_token(username, token):
    # Gets response from auth server
    response = requests.post(f"{configurations['auth-url']}/auth/verify_token",
        data={
            "username": username,
            "token": token
        }
    )

    # Checks the response from auth server
    if response.ok:
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