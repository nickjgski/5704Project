import calendar
from datetime import datetime
from github import Github
import os
import time

def search_limit(g):
    try:
        search_rate_limit = g.get_rate_limit().search
    except:
        print("Encountered error")
    else:
        reset_timestamp = calendar.timegm(search_rate_limit.reset.timetuple())
        remaining = search_rate_limit.remaining
        if remaining < 10:
            sleep_time = reset_timestamp - calendar.timegm(time.gmtime()) + 5  # add 5 seconds to be sure the rate limit
            # has been reset
            time.sleep(sleep_time)

def core_limit(g):
    try:
        core_rate_limit = g.get_rate_limit().core
    except:
        print("Encountered 502")
    else:
        reset_timestamp = calendar.timegm(core_rate_limit.reset.timetuple())
        remaining = core_rate_limit.remaining
        if remaining < 10:
            sleep_time = reset_timestamp - calendar.timegm(time.gmtime()) + 5  # add 5 seconds to be sure the rate limit
            # has been reset
            time.sleep(sleep_time)

def main():
    g = Github("a7aec9f2a06c11bc9d9e3acb36292b886ea5e4d9")
    repos = g.search_repositories("language:kotlin")

    begin_date = datetime(2016, 2, 1, 0, 0, 0, 0)
    end_date = datetime(2020, 3, 21, 0, 0, 0, 0)
    count = 0
    commit_count = 0

    for repo in repos:
        search_limit(g)
        name = repo.name
        if name != 'kotlin' and name != 'architecture-samples':
            print(name)
            if not os.path.exists(os.getcwd()):
                os.mkdir(os.getcwd())
            elif not os.path.isdir(os.getcwd()):
                return  # you may want to throw some error or so.
            f = open(os.path.join(os.getcwd(), name + ' commits.txt'), 'w+', encoding='utf-8')
            latest_shas = []
            core_limit(g)
            print("branches")
            branches = repo.get_branches()
            for branch in branches:
                core_limit(g)
                latest_shas.append(branch.commit.sha)
            print("shas")
            for sha in latest_shas:
                core_limit(g)
                commits = repo.get_commits(sha, '', begin_date, end_date)
                print("commits")
                for commit in commits:
                    core_limit(g)
                    search_limit(g)
                    if 'fix' in commit.commit.message or 'bug' in commit.commit.message or 'patch' in commit.commit.message:
                        line = commit.commit.message.strip() + ' | ' + str(commit.commit.author.date) + ' | ' + commit.sha
                        f.write(line)
                        f.write('\n\n')
                        f.flush()
                        commit_count += 1
            f.close()
            count += 1
            print(commit_count)
            if count == 19:
                break
