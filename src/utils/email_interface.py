import requests
import os

# Allow main script to set the config
def set_config(config):
    global configuration
    configuration = config

# Get the absolute path of the current script
script_path = os.path.abspath(__file__)

# Get the directory path of the current script
script_dir = os.path.dirname(script_path)

def send_comment_notification(author: str, recipient: str, content: str, post_id: str, resources_path: str, post_title: str):
    # Load email html template
    with open (f'{resources_path}/new_comment.html', 'r') as template:
        template_content = template.read()
        template.close()
    
    email_content = template_content.replace('[COMMENTOR_USERNAME]', author).replace('[COMMENT_CONTENT]', content).replace('[POST_URL]', f"https://support.lifplatforms.com/post/{post_id}/{post_title}")

    # Make request to mail server
    headers = {
        "Content-Type": "text/plain", 
        "recipient": recipient, 
        "access-token": configuration['mail-service-token'], 
        "subject": "Someone replied to your post on Lif Support!"
    }

    requests.post(configuration['mail-service-url']+ "/service/send_email", headers=headers, data=email_content)