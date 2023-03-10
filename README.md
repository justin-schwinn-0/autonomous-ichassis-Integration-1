# autonomous-ichassis
The master deliverable repository for the autonomous iChassis.

# Mini Teams
- UI: 
- Navigation: Noah
- Obstacle Detection: Noah, Wyatt
- Hardware: Wyatt

# Contributing
There is a specific workflow necessary to contribute to the autonomous-ichassis main repository.

1. Fork the repository from AutonomousiChassis/autonomous-ichassis using the github ui. You should now have your own fork of the repository called githubUserName/autonomous-ichassis.

2. Clone your fork of the autonomous-ichassis repository. In NoahC77's case the following command is used within the terminal

```
git clone https://github.com/NoahC77/autonomous-ichassis.git
```

3. Now navigate to the local git repository and notice that you are in your forked local main branch. Do not make changes to your local main branch. This branch will be used to update from the upstream main repository. Perform the following to see what branches you have. N
```
git branch -v


* main         9c2ab9d Initial commit

```

4. To get the latest updates from the main repository you must first add the main upstream repository as the upstream by doing the following
```

git remote -v
origin	https://github.com/NoahC77/autonomous-ichassis.git (fetch)
origin	https://github.com/NoahC77/autonomous-ichassis.git (push)




git remote add upstream https://github.com/AutonomousiChassis/autonomous-ichassis.git

git remote -v
origin  https://github.com/NoahC77/autonomous-ichassis.git (fetch)
origin  https://github.com/NoahC77/autonomous-ichassis.git (push)
upstream	https://github.com/AutonomousiChassis/autonomous-ichassis.git (fetch)
upstream	https://github.com/AutonomousiChassis/autonomous-ichassis.git (push)
```

5. Now that upstream is setup, ensure you are in your local main branch and do the following to bring your local main branch up to date with the upstream main repository. Remember in this case it should be AutonomousiChassis/autonomous-ichassis.

```
git pull upstream main
Username for 'https://github.com': NoahC77
Password for 'https://NoahC77@github.com': 
From https://github.com/AutonomousiChassis/autonomous-ichassis
 * branch            main       -> FETCH_HEAD
 * [new branch]      main       -> upstream/main
Already up to date.
```

6. Your local main branch is now up to date with the upstream main branch. To update your local non-main branch with the new changes in your local main branch checkout the non main branch and merge it with main. This will not change main.

```
git checkout contributing
Switched to branch 'contributing'


git merge main
Already up to date.
```

7. Finally in order to merge your changes with the upstream main repository and make changes to the end product, push your non-main local branch to your forked github repository. Once this is done you will submit a merge request using the UI. Request to merge your forked github branch with the upstream main branch.

```
git push origin contributing
Username for 'https://github.com': NoahC77
Password for 'https://NoahC77@github.com': 
Enumerating objects: 11, done.
Counting objects: 100% (11/11), done.
Delta compression using up to 4 threads
Compressing objects: 100% (6/6), done.
Writing objects: 100% (9/9), 1.66 KiB | 340.00 KiB/s, done.
Total 9 (delta 2), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (2/2), done.
remote: 
remote: Create a pull request for 'contributing' on GitHub by visiting:
remote:      https://github.com/NoahC77/autonomous-ichassis/pull/new/contributing
remote: 
To https://github.com/NoahC77/autonomous-ichassis.git
 * [new branch]      contributing -> contributing
```