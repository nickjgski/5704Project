import calendar
from github import Github
import os
import time

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
    owners = ['Kotlin', 'AppIntro', 'android', 'android', 'google', 'google', 'Kotlin',
              'square', 'afollestad', 'mikepenz', 'square', 'alibaba', 'android', 'JakeWharton', 'shadowsocks',
              'android', 'inorichi', 'JakeWharton', 'android']
    filenames = ['anko', 'AppIntro', 'architecture-components-samples', 'architecture-samples', 'flexbox-layout',
                 'iosched', 'kotlinx.coroutines', 'leakcanary', 'material-dialogs', 'MaterialDrawer', 'okio',
                 'p3c', 'plaid', 'RxBinding', 'shadowsocks-android', 'sunflower', 'tachiyomi', 'timber', 'uamp']
    commitnums = [4, 2, 9, 8, 2, 9, 292, 90, 1, 16, 7, 2, 14, 1, 4, 2, 3, 1, 1]

    g = Github("a7aec9f2a06c11bc9d9e3acb36292b886ea5e4d9")
    file_count = 0

    for i in range(19):
        commit_count = 0
        contains_kt = False
        name = filenames[i]
        readfile = open(os.path.join(os.getcwd(), name + ' commits.txt'), 'r', encoding='utf-8')
        writefile = open(os.path.join(os.getcwd(), 'selected_commits\\' + name + '.txt'), 'w+', encoding='utf-8')
        core_limit(g)
        repo = g.get_repo(owners[i] + '/' + name)
        for line in readfile:
            if '|' in line:
                temp = line.split('|')
                sha = temp[2].strip()
                if len(sha) == 40:
                    core_limit(g)
                    commit = repo.get_commit(sha)
                    for file in commit.files:
                        core_limit(g)
                        if '.kt' in file.filename:
                            writefile.write(file.filename + '\n' + str(file.additions) + '\n' + str(file.deletions) + '\n' +
                                            str(file.changes) + '\n' + file.contents_url + '\n' + file.raw_url + '\n' +
                                            file.blob_url + '\n\n')
                            writefile.flush()
                            file_count += 1
                            contains_kt = True
                            if file_count == 500:
                                break
                    if contains_kt:
                        writefile.write(sha + '\n')
                        commit_count += 1
                    if commit_count == commitnums[i]:
                        break
                    if file_count == 500:
                        break
        if file_count == 500:
                break
    print(file_count)


if __name__ == '__main__':
    main()
