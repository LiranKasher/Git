import subprocess


commit_count = 0
commits = ""


def get_last_tag():
    last_tag = subprocess.getoutput("git tag -l --sort=-version:refname --sort=-creatordate | head -1")
    return last_tag


def get_previous_tag():
    previous_tag = subprocess.getoutput("git tag -l --sort=-version:refname --sort=-creatordate | head -2 | tail -1")
    return previous_tag


def get_git_log():
    msg = "\"Message: %s, " \
          "Author: %an, " \
          "Date: %ai, " \
          " %H\""
    git_log = subprocess.getoutput(f"git log --no-merges --pretty=format:{msg} {get_previous_tag()}..{get_last_tag()}")
    return git_log


def split_commits():
    global commits
    global commit_count
    subprocess.getoutput("git pull --tags --force")
    commits = get_git_log().splitlines()
    commit_count = len(commits)
    return commits, commit_count


split_commits()


with open('commits.html', 'w+') as file:
    file.write('<html><body>')
    file.write(f"<h1><u>Commit list for current build</u></h1>")
    file.write(f"<h2>Tag: {get_last_tag()}</h2>")
    file.write(f"<h2>Number of commits for current tag: {commit_count}</h2>")
    file.write(f"<h2>Commits:</h2>")
    file.write("<ol style='font-size: 16px;'>")
    for n, commit in enumerate(commits, start=1):
        file.write(f"<li style='font-size: 20px;'>{commit}</li>")
    file.write("</ol>")
    file.write('</body></html>')