from github import Github


def main():
    g = Github()

    repos = g.search_repositories("language:go")

    for repo in repos:
        print(repo.name)


if __name__ == '__main__':
    main()
