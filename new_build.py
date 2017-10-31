import git
import os


repo_path = os.path.join(os.getcwd(), 'test_updated')
repo = git.Repo(repo_path)
backup_branch = repo.active_branch
origin = repo.remotes.origin

new_branch_name = 'new_build'
remotes_branches = repo.git.ls_remote()

complete_branch_name = 'refs/heads/' + new_branch_name + ''
if new_branch_name not in remotes_branches:
    new_branch = repo.create_head(new_branch_name)
    new_branch.checkout()
    repo.git.add('README.md')
    author = git.Actor("Alan Bracco", "internetagb@gmail.com")
    committer = git.Actor("Alan Bracco", "internetagb@gmail.com")
    repo.index.commit("new_build",
                      author=author, committer=committer)
    origin.push(new_branch)
    backup_branch.checkout()


