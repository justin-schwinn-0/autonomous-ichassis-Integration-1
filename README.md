# autonomous-ichassis
The master deliverable repository for the autonomous iChassis.

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
upstream	https://github.com/AutonomousiChassis/autonomous-ichassis.git (fetch)
upstream	https://github.com/AutonomousiChassis/autonomous-ichassis.git (push)


```

5. Now that upstream is setup, ensure you are in your forked local main branch and do the following to bring your local main branch up to date with the main repository.

```
git pull upstream main
```
