from datetime import datetime
from github import Github
import os


def main():
    g = Github()

    repos = g.search_repositories("language:kotlin")

    begindate = datetime(1990, 1, 1, 0, 0, 0, 0)
    enddate = datetime(2020, 3, 21, 0, 0, 0, 0)

    for repo in repos:
        name = repo.name
        f = open(os.path.join(os.getcwd(), name + ' commits'), 'r+')
        latestshas = []
        branches = repo.get_branches()
        for branch in branches:
            latestshas += branch.commit.sha
        for sha in latestshas:
            commits = repo.get_commits(sha, begindate, enddate)
            for commit in commits:
                if 'fix' in commit.commit.message or 'bug' in commit.commit.message or 'patch' in commit.commit.message:
                    f.write(commit.commit)
                    f.write('\n')
                    f.flush()
        f.close()

if __name__ == '__main__':
    main()
