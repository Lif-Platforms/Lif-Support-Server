import yaml
import requests
import os

# Get the absolute path of the current script
script_path = os.path.abspath(__file__)

# Get the directory path of the current script
script_dir = os.path.dirname(script_path)

# Load config
with open('config.yml', 'r') as file:
    configuration = yaml.safe_load(file)

def send_comment_notification(author: str, recipient: str, content: str, post_id: str, resources_path: str):
    # Load email html template
    with open (f'{resources_path}/new_comment.html', 'r') as template:
        template_content = template.read()
        template.close()
    
    email_content = template_content.replace('[COMMENTOR_USERNAME]', author).replace('[COMMENT_CONTENT]', content).replace('[POST_URL]', f"https://support.lifplatforms.com/#/view_post/{post_id}")

    # Make request to mail server
    headers = {
        "Content-Type": "text/plain", 
        "recipient": recipient, 
        "access-token": configuration['mail-service-token'], 
        "subject": "Someone replied to your post on Lif Support!"
    }

    requests.post(configuration['mail-service-url']+ "/service/send_email", headers=headers, data=email_content)