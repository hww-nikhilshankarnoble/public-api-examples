"""
Main API for the Hokey Campaign Manager.

Example usage:
    >>> from hvfx_campaign_manager import manager
    >>> # Start a campaign
    >>> manager.start_campaign("weyland_corp", "a1680")
    >>> # Complete a campaign from inside the campaign directory.
    >>> os.chdir("./di-campaign-weyland_corp-a1680")
    >>> manager.complete_campaign()
"""
from __future__ import annotations

# Built-ins
import json
import os.path
import random
import string
import subprocess

# Third-party
import git

# Internal
from hvfx_campaign_manager import git_utils


def start_campaign(client: str, jobid: str):
    """
    Start a new campaign.

    Args:
        client (str): The client name.
        jobid (str): The job id.
    """
    config = create_campaign_config(client, jobid)
    repo = git_utils.clone_repo(config["url"], config["directory"])
    if not repo:
        return
    git_utils.checkout_branch(config, repo)
    create_project_spec(config)
    create_campaign_directory(config)
    jobdir = config["jobdir"]
    command = "open  " + jobdir
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()


def complete_campaign():
    """
    Complete the campaign.
    """
    spec = get_project_spec()
    if not spec:
        return
    config = create_campaign_config(spec["client"], spec["jobid"])
    if not config:
        return
    repo = git_utils.verify_local_repo(config["direcory"])
    if not repo:
        return
    branch = verify_project_branch(config, repo)
    if not branch:
        return
    # Repo and branch are correct and push. Create PR.
    pr = "https://github.com/Hogarth-Worldwide/di-campaign-{}/compare/{}?expand=1".format(
        config["client"], config["branch"]
    )
    command = "open  " + pr
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    print(
        f"Project closed, please create a PR: {pr}. You can now safely remove the directory."
    )


# Private
def get_project_spec() -> dict[str, str] | None:
    """
    Get projectspec from current directory and verify contents.
    """
    if not os.path.exists("projectspec.json"):
        print("Unable to find project spec, navidate to the root directory")
        return
    with open("projectspec.json", "r") as file:
        spec = json.load(file)
    if not spec:
        print("Unable to load project spec.")
        return
    if "client" not in spec:
        print("Client not in project spec.")
        return
    if "jobid" not in spec:
        print("JobId not in project spec.")
        return
    return {
        "client": spec["client"],
        "jobid": spec["jobid"],
    }


# Private
def create_campaign_config(client: str, jobid: str) -> dict[str, str]:
    """
    Generate config vars from the client and job id.

    Args:
        client (str): The client name.
        jobid (str): The job id.

    Returns:
        dict[str, str]: The config vars.
    """
    repo_base = "git@github.com:Pineapple-Worldwide/"
    repo_prefix = "campaign-config"
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return {
        "client": client,
        "jobid": jobid,
        "name": f"{repo_prefix}-{client}",
        "spec": f"./{repo_prefix}-{client}-{suffix}/projectspec.json",
        "url": f"{repo_base}{repo_prefix}-{client}.git",
        "branch": f"campaign/{jobid}",
        "directory": f"./{repo_prefix}-{client}-{suffix}/",
        "jobdir": f"./{repo_prefix}-{client}-{suffix}/campaign/{jobid}",
    }


# Private
def verify_project_branch(config: dict[str, str], repo: git.Repo) -> git.Head:
    """
    Verify the repo branch of the current directory, matches the value from the project spec.
    """
    if str(repo.active_branch) == config["branch"]:
        return repo.active_branch
    print("Current branch does not match project spec.")


# Private
def create_project_spec(config: dict[str, str]) -> None:
    """
    Create a project spec with required information.
    """
    print("Creating project spec")
    content = {"client": config["client"], "jobid": config["jobid"]}
    with open(config["spec"], "w") as f:
        json.dump(content, f)


# Private
def create_campaign_directory(config: dict[str, str]) -> None:
    """
    Creates the directory structure for the campaign.

    Args:
        config (dict[str, str]): the config vars.

    """
    path = os.path.abspath(config["jobdir"])
    if os.path.exists(path):
        print("Campaign already exists, please check job number")
        return
    os.makedirs(path)
