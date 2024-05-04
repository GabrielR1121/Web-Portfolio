import os
import time
import requests
import json


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
def get_repo_info(repo_info, ignored_repo):

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
        "ignore": repo_info["name"] in ignored_repo,
        "languages": languages,
    }
    return repo_data




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


# Verifies if the json file with the data has been edited in the specified amount of time
def is_file_recently_modified(filename, max_age_seconds):
    if not os.path.exists(filename):
        return False
    modification_time = os.path.getmtime(filename)
    current_time = time.time()
    return current_time - modification_time < max_age_seconds


# Verify if the repository has been updated by comparing updated dates
def is_repo_updated(repo_name, new_repo, old_repo):
    try:
        return new_repo["updated_at"] == old_repo["projects"][repo_name]["updated"]
    except:
        return False


# Main method for getting and storing the data collected from the GitHub API
def get_project_info(settings):

    print("The request started. Please Wait..")

    github_filepath = settings["github_filepath"]
    GitHub_User = settings["GitHub_User"]
    timer = settings["timer"]
    ignore_repo = settings["ignore_repo"]

    # If the file has been edited in the last hour then use the existing data
    if is_file_recently_modified(github_filepath, timer):
        print("Using existing JSON file.")
    else:
        # If the file has not been edited for more than an hour then verify if any repositories have been updated.
        # This is done to prevent unnecesary requests to the GitHub API
        repos_info = get_user_repos(GitHub_User)
        if repos_info:
            all_repo_data = {}
            all_repo_data["projects"] = {}
            for repo_info in repos_info:
                repo_name = repo_info["name"]
                # Loads the existing json file with repository data in order to compare the new and old data
                existing_data = load_json(github_filepath)
                # If the data already exists and now updates where found then just use the old data
                if existing_data and is_repo_updated(
                    repo_name, repo_info, existing_data
                ):
                    all_repo_data["projects"][repo_name] = existing_data["projects"][
                        repo_name
                    ]
                    print(f"Using existing data for {repo_name}.")
                else:
                    # If the data has changed then retrive that repo info and store it
                    repo_data = get_repo_info(repo_info, ignore_repo)
                    if repo_data:
                        all_repo_data["projects"][repo_name] = repo_data

            # Convert all repos data into a single json file
            save_to_json(all_repo_data, github_filepath)

            print("All repository information saved.")
            return all_repo_data
