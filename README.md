## Commit with different name
```
git config --local user.name <your github name>
git config --local user.email <your email address>
```

## Change the auther info in the previous commits and github
Checkout [https://help.github.com/articles/changing-author-info/](https://help.github.com/articles/changing-author-info/)

## Git command lines
* sync branch with origin/master
  * `git fetch origin && git rebase -i origin/master`
* pending files:
  * `git status`
* recent commits in this branch:
  * `git log`
* modified files in a given commit-id:
  * `git show --name-only <commit-id>`
* revert a file to a previous version:
* `git checkout <commit-id> -- <file-path>`
* revert all untracked files:
  * `git clean -f -n`  (show what to delete)
  * `git clean -f`  (actually delete)
* revert all tracked files:
  * `git reset --hard HEAD^`
  * 
