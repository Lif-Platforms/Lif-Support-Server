from fastapi import FastAPI, Form, HTTPException, Request
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
import utils.auth_server_interface as auth_server
import utils.db_interface as database
import utils.email_interface as email_interface
import utils.config_interface as config
import difflib
import uvicorn
import json
import uuid
import yaml
import os

app = FastAPI()

# Load config
configurations = config.load_config()

# Sets config for auth_interface and email_interface
auth_server.set_config(configurations)
email_interface.set_config(configurations)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=configurations['allow-origins'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the absolute path of the current script
script_path = os.path.abspath(__file__)

# Get the directory path of the current script
script_dir = os.path.dirname(script_path)

@app.get("/", response_class=HTMLResponse)
def root():
    # Loads "index.html" from resources folder
    with open(script_dir + "/resources/index.html", "r") as index:
        page = index.read()

    return page

@app.post("/new_post")
async def new_post(request: Request, title: str = Form(), content: str = Form(), software: str = Form()):
    # Get username and token from request headers
    username = request.headers.get('username')
    token = request.headers.get('token')

    # Verifies token with auth server
    if await auth_server.verify_token(username, token):

        # Verifies software field is valid
        valid_software = ["Ringer", "Dayly"]

        if software in valid_software:
            # Generate a random UUID
            post_id = str(uuid.uuid4())

            database.new_post(username, title, content, software, post_id)

            return JSONResponse(status_code=201, content={"post_id": post_id})
        else: 
            raise HTTPException(status_code=400, detail='Invalid Software!')
    else:
        raise HTTPException(status_code=401, detail='Invalid Token!')
    
@app.get("/search/{query}")
def search(query, filters: Optional[str] = None):
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

        # Check if filters are supplied
        if filters:
            # Format filters for use
            formatted_filters = filters.split(',')

            # Ignore result if it does not match filters
            if software in formatted_filters: 
                # Formats and adds data to data list
                data.append({"Title": title, "Content": content, "Software": software, "Id": id})
        else:
            # Formats and adds data to data list
            data.append({"Title": title, "Content": content, "Software": software, "Id": id})

    return data

@app.get("/load_post/{post_id}")
def load_post(post_id: str):
    # Gets all posts from database
    post = database.get_post(post_id)

    # Check if post exists
    if post:
        # Formats data for sending to client
        data = {"Title": post[1], "Content": post[2], "Author": post[0], "Software": post[3], "Date": post[6]}

        return data
    else:
       raise HTTPException(status_code=404, detail='Post Not Found') 

@app.get("/load_comments/{post_id}")
def load_comments(post_id: str):
    # Gets post from database
    post = database.get_post(post_id)
    
    # Check if post exists and return comments
    if post:
        return json.loads(post[5])
    else:
        raise HTTPException(status_code=404, detail='Comments Not Found') 
       
@app.post('/new_comment')
async def new_comment(request: Request, comment: str = Form(), post_id: str = Form()):
    # Get username and token from request headers
    username = request.headers.get('username')
    token = request.headers.get('token')

    # Verifies token with auth server
    if await auth_server.verify_token(username=username, token=token):
        # Create comment in database
        database.create_comment(author=username, comment=comment, post_id=post_id)

        # Get post author
        author = database.get_post_author(post_id=post_id)

        # Get author email from auth server
        author_email = await auth_server.get_account_email(author)

        # Send email notification
        email_interface.send_comment_notification(author=username, recipient=author_email, content=comment, post_id=post_id, resources_path=f"{script_dir}/resources")

        return JSONResponse(status_code=201, content='Created Comment!')
    
    else:
        raise HTTPException(status_code=401, detail='Invalid Token!')
    

@app.post('/new_answer')
async def new_answer(request: Request, answer: str = Form(), post_id: str = Form()):
    # Get username and token from request headers
    username = request.headers.get('username')
    token = request.headers.get('token')

    # Verifies token with auth server
    if await auth_server.verify_token(username=username, token=token):
        database.create_answer(author=username, answer=answer, post_id=post_id)

        # Get post author
        author = database.get_post_author(post_id=post_id)

        # Get author email from auth server
        author_email = await auth_server.get_account_email(author)

        # Send email notification
        email_interface.send_comment_notification(author=username, recipient=author_email, content=answer, post_id=post_id, resources_path=f"{script_dir}/resources")

        return JSONResponse(status_code=201, content='Answer Created!')
    
    else:
        raise HTTPException(status_code=401, detail='Invalid Token!')
    
@app.delete('/delete_post/{post_id}')
async def delete_post(post_id: str, request: Request):
    # Get auth information from request header
    username = request.headers.get('username')
    token = request.headers.get('token')
    
    # Verify token with auth server
    if await auth_server.verify_token(username=username, token=token):
        # Verify user has permission to delete post
        author = database.get_post_author(post_id)

        if author == username:
            database.delete_post(post_id)

            return JSONResponse(status_code=200, content='Post Deleted!')
        else:
            raise HTTPException(status_code=403, detail='Permission Denied!')
    else:
        raise HTTPException(status_code=401, detail='Invalid Token!')
    
@app.put('/edit_post/{post_id}')
async def edit_post(request: Request, post_id: str, title: str = Form(), content: str = Form(), software: str = Form()):
    # Get auth information from request header
    username = request.headers.get('username')
    token = request.headers.get('token')

    # Verify token with auth server
    if await auth_server.verify_token(username=username, token=token):
        # Verifies the user is the author of the post
        author = database.get_post_author(post_id)

        if author == username:
            # Update post in database
            database.update_post(post_id, title, content, software)

            return JSONResponse(status_code=200, content='Post Updated Successfully!')
        else:
            raise HTTPException(status_code=403, detail='Permission Denied!')
    else:
        raise HTTPException(status_code=401, detail='Invalid Token!')

@app.get('/load_recent_posts')
def recent_posts():
    posts = database.get_recent_posts()

    return posts

if __name__ == '__main__':
    uvicorn.run(app="main:app", port=8003, host="0.0.0.0")