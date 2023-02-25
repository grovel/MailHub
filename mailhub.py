import os
import time
import requests


class colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    END = '\033[0m'


def clear_screen():
    """Clears the console screen."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def print_header():
    """Prints the program header."""
    clear_screen()
    print(f"""{colors.BLUE}___  ___        _  _  _   _         _     
|  \/  |       (_)| || | | |       | |    
| .  . |  __ _  _ | || |_| | _   _ | |__  
| |\/| | / _` || || ||  _  || | | || '_ \ 
| |  | || (_| || || || | | || |_| || |_) |
\_|  |_/ \__,_||_||_|\_| |_/ \__,_||_.__/ 
                                          
                                          
""" + colors.END)
    print(f"{colors.YELLOW}Welcome to MailHub!\n{colors.END}")


def get_repos(username):
    """Retrieves the repositories for a given GitHub user."""
    url = f"https://api.github.com/users/{username}/repos"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        print(f"{colors.RED}Error retrieving repositories.{colors.END}")
        time.sleep(2)
        main()
    repos = response.json()
    return repos


def get_commit_authors(username, repo):
    """Retrieves the commit authors for a given repository."""
    url = f"https://api.github.com/repos/{username}/{repo}/commits"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        print(
            f"{colors.RED}Error retrieving commits for repository {repo}.{colors.END}")
        return []
    commits = response.json()
    commit_authors = [(commit["commit"]["author"]["email"], commit["commit"]["author"]["name"])
                      for commit in commits if commit["author"] and commit["author"]["login"] == username]
    return commit_authors


def search_github():
    """Searches for commit authors in the user's GitHub repositories."""
    while True:
        username = input("Enter GitHub username: ")
        repos = get_repos(username)
        if not repos:
            print(f"{colors.RED}User not found.{colors.END}")
            time.sleep(2)
            main()
        commit_authors = []
        for repo in repos:
            repo_commit_authors = get_commit_authors(username, repo["name"])
            commit_authors.extend(repo_commit_authors)
        commit_authors = list(set(commit_authors))
        commit_authors.sort(key=lambda x: x[1], reverse=True)
        if not commit_authors:
            print(f"{colors.YELLOW}No commits found for {username}.{colors.END}")
            time.sleep(2)
            main()
        else:
            print(
                f"{colors.GREEN}Email addresses for commits in {username}'s repositories:{colors.END}")
            for commit_author in commit_authors:
                print(f"{commit_author[0]} ({commit_author[1]})")


def main():
    print_header()
    search_github()


if __name__ == "__main__":
    main()
