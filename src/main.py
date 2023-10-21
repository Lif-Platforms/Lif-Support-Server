from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import utils.auth_server_interface as auth_server
import utils.db_interface as database
import difflib
import uvicorn
import json
import uuid
import yaml
import os

app = FastAPI()

# Get the absolute path of the current script (My Server Plus.py)
script_path = os.path.abspath(__file__)

# Get the directory path of the current script
script_dir = os.path.dirname(script_path)

# Loads Configuration
with open('config.yml', 'r') as file:
    configuration = yaml.safe_load(file)

# Configure CORS
origins = configuration['allow-origins']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def root():
    # Loads "index.html" from resources folder
    with open(script_dir + "/resources/index.html", "r") as index:
        page = index.read()

    return page

@app.post("/new_post/{username}/{token}")
def new_post(username: str, token: str, title: str = Form(), content: str = Form(), software: str = Form()):
    # Verifies token with auth server
    verify = auth_server.verify_token(username, token)

    if verify:

        # Verifies software field is valid
        valid_software = ["Ringer", "Dayly"]

        if software in valid_software:
            # Generate a random UUID
            post_id = str(uuid.uuid4())

            database.new_post(username, title, content, software, post_id)

            return {"Status": "Ok", "post_id": post_id}
        else: 
            return {"Status": "Unsuccessful"}
    else:
        return {"Status": "Unsuccessful"}
    
@app.get("/search/{query}")
def search(query):
    def find_best_results(search_query, results, search_index):
        if results:
            best_matches = difflib.get_close_matches(search_query, [item[search_index] for item in results], n=len(results), cutoff=0.5)
            return [item for match in best_matches for item in results if match == item[search_index]]
        else:
            return []

    search_query = query
    results = database.get_posts()
    search_index = 1  # Change this to the desired index
    best_results = find_best_results(search_query, results, search_index)

    # Formats results for client
    data = []

    for post in best_results:
        title = post[1]
        raw_content = post[2]
        software = post[3]
        id = post[4]
        content = ''
        
        # Adds "..." if the content is too long for the preview
        if len(raw_content) <= 100:
            content = raw_content
        else:
            content =  raw_content[:100 - 3] + "..."

        # Formats and adds data to data list
        data.append({"Title": title, "Content": content, "Software": software, "Id": id})

    return data

@app.get("/load_post/{post_id}")
def load_post(post_id: str):
    # Gets all posts from database
    posts = database.get_posts()

    return_post = False

    # Finds the post based on id
    for post in posts:
        database_post_id = post[4]

        if post_id == database_post_id:
            # Formats data for sending to client
            data = {"Title": post[1], "Content": post[2], "Author": post[0], "Software": post[3]}

            return_post = data

    return return_post

@app.get("/load_comments/{post_id}")
def load_comments(post_id: str):
    # Gets all posts from database
    posts = database.get_posts()

    return_comments = False

    # Finds the post based on id
    for post in posts:
        database_post_id = post[4]

        if post_id == database_post_id:
            # Formats data for sending to client
            data = json.loads(post[5])

            return_comments = data

    return return_comments

@app.post('/new_comment/{username}/{token}')
async def new_comment(username: str, token: str, comment: str = Form(), post_id: str = Form()):
    # Verifies token with auth server
    status = await auth_server.verify_token(username=username, token=token)

    print(status)

    if status:
        # Create comment in database
        database.create_comment(author=username, comment=comment, post_id=post_id)

        # Get post author
        author = database.get_post_author(post_id=post_id)

        # Get author email from auth server
        author_email = await auth_server.get_account_email(author)

        return {"Status": "Ok"}
    
    else:
        return {"Status": "Unsuccessful"}
    

@app.post('/new_answer/{username}/{token}')
def new_answer(username: str, token: str, answer: str = Form(), post_id: str = Form()):
    # Verifies token with auth server
    status = auth_server.verify_token(username=username, token=token)

    if status:
        database.create_answer(author=username, answer=answer, post_id=post_id)

        return {"Status": "Ok"}
    
    else:
        return {"Status": "Unsuccessful"}
    
@app.get('/load_recent_posts')
def recent_posts():
    posts = database.get_recent_posts()

    return posts

if __name__ == '__main__':
    uvicorn.run(app="main:app", port=8003, host="0.0.0.0")