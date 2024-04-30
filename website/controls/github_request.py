import os
import time
import requests
import json
import atexit
from ..config.config import GitHub_User

#Global Variables
json_name = "github.json"

# Makes the request to the url in order to get the data
def make_http_get_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data from {url}.")
        return None


# Gets all the data for the repos accociated with my GitHub repo
def get_user_repos(username):
    url = f"https://api.github.com/users/{username}/repos?sort=updated"
    return make_http_get_request(url)


# Makes a request to the GitHub API in order to get the specific information of each repo.
def get_repo_info(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"

    # ** Use make_http_get_request here
    response = requests.get(url)
    if response.status_code == 200:
        repo_info = response.json()
        # Makes the request to the GitHub API to get specific language distribution from the specific repo
        languages_url = repo_info["languages_url"]
        languages_response = requests.get(languages_url)
        languages = languages_response.json()

        # Stores the necessary data in json form
        repo_data = {
            "name": repo_info["name"],
            "description": repo_info["description"],
            "created": repo_info["created_at"],
            "updated": repo_info["updated_at"],
            "languages": languages,
        }
        return repo_data
    else:
        print(f"Failed to fetch repository information for {repo}.")
        return None


# Takes the data and turns it into a json file
def save_to_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


# Opens the data from a json file
def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return None


# creates the lock file that prevents the user from making multiple requests of the API while it already running
def write_lock_file(lock_file):
    open(lock_file, "w").close()

# Deletes the lock file once the procedure is completed
def remove_lock_file(lock_file):
    if os.path.exists(lock_file):
        os.unlink(lock_file)

# Verifies if the json file with the data has been edited in the specified amount of time
def is_file_recently_modified(filename, max_age_seconds):
    if not os.path.exists(filename):
        return False
    modification_time = os.path.getmtime(filename)
    current_time = time.time()
    return current_time - modification_time < max_age_seconds

# Main method for getting and storing the data collected from the GitHub API
def get_project_info():
    # Stores the path to the config file
    config_folder = "website/config"

    # Creates a lock file to prevent method from being called more than once while its still executing
    lock_file = os.path.join(config_folder, "project_info.lock")

    # If the file already exists then the command was already excuted and refuses any other inputs
    if os.path.exists(lock_file):
        print("The API has already been requested once. Please Wait...")
        return

    write_lock_file(lock_file)
    atexit.register(lambda: remove_lock_file(lock_file))

    try:
        # Prepares to connect to GitHub API
        username = GitHub_User
        # location where data will be stored
        json_filename = f"website/static/data/{json_name}"

        print("The request started. Please Wait..")

        # If the file has been edited in the last hour then use the existing data
        if is_file_recently_modified(json_filename, 3600):
            print("Using existing JSON file.")
        else:
            # If the file has not been edited for more than an hour then verify if any repositories have been updated.
            # This is done to prevent unnecesary requests to the GitHub API
            repos_info = get_user_repos(username)
            if repos_info:
                all_repo_data = {}
                for repo_info in repos_info:
                    repo_name = repo_info["name"]
                    # This if is placed here to prevent the Read Me Repository from being used.
                    if repo_name != username:
                        # Loads the existing json file with repository data in order to compare the new and old data
                        existing_data = load_json(json_filename)
                        # If the data already exists and now updates where found then just use the old data
                        # ** This is incorrect because it is only verfying if there are new repositories not if the updated date has changed **
                        if existing_data and repo_name in existing_data:
                            all_repo_data[repo_name] = existing_data[repo_name]
                            print(f"Using existing data for {repo_name}.")
                        else:
                            # If the data has changed then retrive that repor info and store it
                            repo_data = get_repo_info(username, repo_name)
                            if repo_data:
                                all_repo_data[repo_name] = repo_data

                # Convert all repos data into a single json file
                save_to_json(all_repo_data, json_filename)
                print(f"All repository information saved to {json_name}")
    finally:
        # Deletes the lock file meaning the process has finished
        remove_lock_file(lock_file)
