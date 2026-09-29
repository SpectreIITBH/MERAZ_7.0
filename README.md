# MERAZ 7.0


## Contributing Guidelines

- Fork the repository by clicking on fork button (Forking is COMPULSORY)

- Clone the forked repo to your local machine

- Create a separate branch from main

```
git branch <branch_name>

git checkout <branch_name>
```

- Do all your work in this newly created branch

- When your changes are ready and you feel you need to push, fetch the latest changes from main branch first (as the main branch may have moved since you made a branch)

```
git checkout main
git pull https://github.com/SpectreIITBH/MERAZ_7.0

git checkout <branch_name>
git rebase main
```

(If any merge conflicts arise, discuss among yourselves or make most appropriate changes, have a thought!)

- Now after clearing all merge conflicts (if exist) you are ready to push your changes

```
git push origin <branch_name> -f
```

- You can raise a pull request from the github UI after the previous command 

