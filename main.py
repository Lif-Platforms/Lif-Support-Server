from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import utils.auth_server_interface as auth_server
import utils.db_interface as database
import difflib

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    # Add more allowed origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"Hello": "World"}

@app.get("/new_post/{username}/{token}/{title}/{content}/{software}")
def new_post(username: str, token: str, title: str, content: str, software: str):
    # Verifies token with auth server
    verify = auth_server.verify_token(username, token)

    if verify:

        # Verifies software field is valid
        valid_software = ["Ringer", "Dayly"]

        if software in valid_software:
            database.new_post(username, title, content, software)

            return {"Status": "Ok"}
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
