import os
import git
import sys


repo_path = os.path.join(os.getcwd(), 'apitest')

repo = git.Repo(repo_path)
branch = repo.active_branch
origin = repo.remotes.origin
# commits_log = repo.git.log(format="%H").split('\n')

# Print current branch
print("Current branch is '{branch}'".format(branch=branch))

# Commits behind (pull) checkpoint
origin.fetch(branch)
commits_behind = list(repo.iter_commits('{branch}..origin/{branch}'
                                        ''.format(branch=branch)))
if commits_behind:
    n_commits = len(commits_behind)
    print("\nYour branch is {n_commits} commit{s} behind {branch}"
          "".format(n_commits=n_commits, branch=branch,
                    s='s' if n_commits > 1 else ''))
    print('(use "git pull" to update your local branch)')
    sys.exit()

# Untracked files checkpoint
untracked_files = repo.untracked_files
if untracked_files != []:
    print("\nUntracked files:")
    for file in untracked_files:
        print("Added '{file}'".format(file=file))
        repo.git.add(file)
    print("Done!")
else:
    print("\nNo untracked files")

# Modified or deleted files checkpoint
if repo.is_dirty():
    print("\nModified or deleted files:")
    modified_files = [file.a_path for file in repo.index.diff(None)]
    for file in modified_files:
        print("Added '{file}'".format(file=file))
        repo.git.add(file)
    print("Done!")
else:
    print("\nNo modified files")

# To be commited checkpoint
if "Changes to be committed" in repo.git.status():
    author = git.Actor("Alan Bracco", "internetagb@gmail.com")
    committer = git.Actor("Alan Bracco", "internetagb@gmail.com")
    repo.index.commit(raw_input("\nCommit message: "),
                      author=author, committer=committer)

# Commits ahead (push) checkpoint
commits_ahead = list(repo.iter_commits('origin/{branch}..{branch}'
                                       ''.format(branch=branch)))
if commits_ahead:
    n_commits = len(commits_ahead)
    print("\nYou have {n_commits} commit{s} "
          "to push".format(n_commits=n_commits,
                           s='s' if n_commits > 1 else ''))
    try:
        origin.push(branch)
        print("Done!")
    except Exception:
        print("\nCould not push commit{s}"
              "".format(s='s' if n_commits > 1 else ''))
else:
    print("\nNothing to push")
