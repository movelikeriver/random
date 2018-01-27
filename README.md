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

## Git show branch name in console
In `~/.bashrc`, add following lines
```
parse_git_branch() {
     git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}
```
then `$(parse_git_branch)` into part of the `PS1` var, e.g.
```
export PS1="\u@\h \[\033[32m\]\w\[\033[33m\]\$(parse_git_branch)\[\033[00m\] $ "
```

## Sync code between local and remote machine
* Setup git server in your remote machine
  * [https://www.digitalocean.com/community/tutorials/how-to-set-up-a-private-git-server-on-a-vps](https://www.digitalocean.com/community/tutorials/how-to-set-up-a-private-git-server-on-a-vps)
  * you can just use `ssh-keygen` without `-C` to generate the pubkey.

* Local machine setup
  * your local repo dir1 for official git is `~/code`
  * your local repo dir2 for remote machine git is `~/rt/code`
  * `git remote -v` to check the remote repo
  * sync code between dir1 and dir2
    * `rsync -av --progress ~/code/<your project> ~/rt/code/  --exclude .git --exclude */target/*`
  * workflow
    * normal workflow in dir1
    * sync from dir1 to dir2
    * `git push` whatever change in dir2 to remote machine git

* Remote machine setup
  * `git clone` your own created repo
  * always `git pull` and run test
