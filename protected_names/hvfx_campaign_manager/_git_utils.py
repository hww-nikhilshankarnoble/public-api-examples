"""
Git utilities for the campaign manager.
"""
# Built-ins
import logging

# Third-party
import git

# Internal
from hvfx_campaign_manager.exceptions import _GitError


# Private
def clone_repo(repo_url: str, repo_path: str) -> git.Repo:
    """
    Clones the repo at the given URL to the given path.

    Args:
        repo_url (str): The URL of the repo to clone.
        repo_path (str): The path to clone the repo to.

    Returns:
        git.Repo: The cloned repo.
    """
    try:
        return git.Repo.clone_from(repo_url, repo_path)
    except git.exc.GitCommandError as e:
        raise GitError("Failed to clone repo: %s" % e)
    except git.excGitError as e:
        raise GitError("Failed to clone repo: %s" % e)


# Private
def verify_local_repo(repo_path: str) -> bool:
    """
    Verifies that the directory is a valid Git repo and is clean.

    Args:
        repo_path (str): The path to clone the repo to.

    Returns:
        bool: True if the repo is valid and clean, False otherwise.
    """
    try:
        repo = git.Repo(repo_path)
    except git.exc.GitError:
        logging.error("No git repo found at %s", repo_path)
        return False

    if repo.is_dirty():
        logging.error("Git repo at %s is dirty", repo_path)
        return False

    return True


# Private
def checkout_branch(config: dict[str, str], repo: git.Repo):
    """
    Checkout branch if it exists (with warning), or create new branch from HEAD.
    """
    try:
        repo.git.checkout(config["branch"])
        print("Branch {} already exists, please be careful.".format(config["branch"]))
    except:
        repo.git.checkout("HEAD", b=config["branch"])
        print("Creating new branch {}".format(config["branch"]))
