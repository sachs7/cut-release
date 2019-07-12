"""
#!/usr/bin/env python3
"""

import os
import subprocess
import shutil

DIRECTORY_TO_REMOVE = []


def catch_git_errors(fun):
    def wrapper(*args, **kwargs):
        try:
            fun(*args, **kwargs)
        except subprocess.CalledProcessError as ce:
            print(f"Called Process Error: {ce}")
        except subprocess.SubprocessError as se:
            print(f"Subprocess Error: {se}")
        except OSError as ose:
            print(f"OS Error: {ose}")
        except Exception:
            print(f"Got an exception. Please check the git access (maybe)!")

    return wrapper


@catch_git_errors
def git_clone(repo):
    print(f"\n1. Cloning the Git Repo...")
    my_clone = subprocess.Popen(
        ["git", "clone", repo],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    stdout, stderr = my_clone.communicate()

    print(f"   Standard Output: {stdout.decode('utf-8')}")
    print(f"   Standard Error: {stderr}")


@catch_git_errors
def go_into_the_repo(repo):
    """
    Given repo => "https://github.com/sachs7/Flight-Finder.git"

    repo.split("/") => ['https:', '', 'github.com', 'sachs7', 'Flight-Finder.git']

    repo.split("/")[-1] => "Flight-Finder.git"

    repo.split("/")[-1][-4] => "Flight-Finder"

    """
    extract_repo_name = repo.split("/")[-1][:-4]
    cwd = os.getcwd()

    os.chdir(cwd + "/" + extract_repo_name)

    new_cwd = os.getcwd()
    DIRECTORY_TO_REMOVE.append(new_cwd)
    print(f"\n2. Changing Directory to... : {new_cwd}")


@catch_git_errors
def get_jira_list(which_branch="development"):
    print(f"\n   Showing which branch: {which_branch}")
    print(f"\n")
    print(f"**" * 5 + f" List of JIRAs merged " + f"**" * 5)
    os.system(
        "git log --pretty=\"format:%s\" origin/master...origin/" + which_branch + " | "
        "grep -e '[A-Z]\+-[0-9]\+' -o -i|awk '{ print toupper($0) }'| sort -u"
    )
    print(f"**" * 5 + f" End of List " + f"**" * 5)


@catch_git_errors
def git_checkout(branch_name):
    """
    Usually, the branch will be created off the default branch.
    But if you want you can modify the below code.
    
    CHECK FOR THIS:

    Create a branch off 'development'

    git checkout -b <branch name> development
    """
    print(f"\n3. Checkout the branch... {branch_name}")

    my_branch = subprocess.Popen(
        ["git", "checkout", "-b", branch_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    stdout, stderr = my_branch.communicate()

    print(f"   Standard Output: {stdout.decode('utf-8')}")
    print(f"   Standard Error: {stderr}")


@catch_git_errors
def git_push(branch_name):
    print(f"\n4. Push the branch... ")
    push_branch = subprocess.Popen(
        ["git", "push", "origin", branch_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    stdout, stderr = push_branch.communicate()

    print(f"   Standard Output: {stdout.decode('utf-8')}")
    print(f"   Standard Error: {stderr}")


@catch_git_errors
def delete_cloned_repos():
    print(f"\n6. Showing the contents of DIRECTORY_TO_REMOVE: {DIRECTORY_TO_REMOVE}")
    repo_path = DIRECTORY_TO_REMOVE.pop()
    print(f"\n   Removing the Folder: {repo_path}")
    shutil.rmtree(repo_path)


@catch_git_errors
def show_directory_contents():
    folder_lists = subprocess.Popen(
        ["ls", "-ltr"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    stdout, stderr = folder_lists.communicate()

    print(f"   Standard Output: {stdout.decode('utf-8')}")
    print(f"   Standard Error: {stderr}")


if __name__ == '__main__':
    PROJECT_A_DEFAULT_BRANCH = "development"
    PROJECT_B_DEFAULT_BRANCH = "develop"

    list_of_repo = [
        ("https://github.com/sachs7/cut-release.git", ""),
        ("git@github.com:sachs7/Youtube-Bot-.git", "develop"),
        ("git@github.com:sachs7/Apartment-Bot.git", "development")
    ]

    parent_directory = os.getcwd()
    print(f"\n0. Parent Directory: {parent_directory}")

    """
    For now the release_Version is hardcoded - for testing purpose.

    This can be customized for user input or when run on CI servers, 
    read the version from parameters
    """
    release_version = "test_release/2019.7.11"

    for repo_link in list_of_repo:
        print(f"\n")
        print(f"--" * 5 + f" Clone, Branch and Push: {repo_link[0]} " + f"--" * 5)
        git_clone(repo_link[0])
        go_into_the_repo(repo_link[0])
        get_jira_list(repo_link[1])
        git_checkout(branch_name=release_version)
        git_push(branch_name=release_version)
        os.chdir(parent_directory)
        print(f"\n5. Going back to Parent Directory: {os.getcwd()}")
        # show_directory_contents()
        delete_cloned_repos()
