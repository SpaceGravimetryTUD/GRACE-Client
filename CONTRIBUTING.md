# Contributing guidelines

## A.  You have a question

1. Use the search functionality [here](https://github.com/SpaceGravimetryTUD/GRACE-Client/issues) to see if someone already filed the same issue.
2. If your issue search did not yield any relevant results, open a new issue.
3. Apply the "Question" label. Additionally, apply other labels when relevant.

## B. You think you may have found a bug

1. Use the search functionality [here](https://github.com/SpaceGravimetryTUD/GRACE-Client/issues) to see if someone already filed the same issue.
2. If your issue search did not yield any relevant results, open a new issue and provide enough information to understand the cause and the context of the problem. Depending on the issue, you may also want to include:
    - the [SHA hashcode](https://help.github.com/articles/autolinked-references-and-urls/#commit-shas) of the commit that is causing your problem
    - some identifying information (name and version number) for dependencies you're using
    - information about the operating system

## C. You want to make changes to the code base

### Announce your plan

1. (**important**) Announce your plan to the rest of the community *before you start working*. This announcement should be in the form of a (new) issue on the Github repository.
2. (**important**) Wait until a consensus is reached about your idea being a good idea.


### Set up a local development environment to work on your changes

1. Go to root of this repository and click on 'Fork'. This will create a copy of GRACE-Client repository in your GitHub account. 
            
2. Clone the fork to your local computer.
        
    ```bash
    git clone https://github.com/your-username/GRACE-Client.git
    ```

3. Change the directory

    ```bash
    cd <repo-name>
    ```

4. Add the upstream repository

    ```bash
    git remote add upstream https://github.com/SpaceGravimetryTUD/GRACE-Client.git
    ```  

5. Now, `git remote -v` will show two remote repositories named:

    * `upstream`, which refers to Fair Code repository 
    * `origin`, which refers to your personal fork

### Develop your contribution

1. Set up a development environment on your computer by following the Quick Start steps shared in our [README](https://github.com/SpaceGravimetryTUD/GRACE-Client?tab=readme-ov-file#-quick-start) up to and including [the python-dependencies installation step](https://github.com/SpaceGravimetryTUD/GRACE-Client?tab=readme-ov-file#install-python-dependencies).

2. Create a branch of the latest commit on the `main` branch to work on your feature/contribution:

    ```bash
    git checkout -b my-feature
    ```  

3. If you are contributing via a fork, make sure to pull in changes from the 'upstream' repository to stay up to date with the `main` branch while working on your feature branch. Follow the instructions [here](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/configuring-a-remote-repository-for-a-fork) and [here](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork).

4. Update the user documentation if relevant. Undocumented contributions might not be merged.

### Submitting your contribution

1. Push your feature branch to your fork of GRACE-Client GitHub repository.

1. Create a pull request, for an example, following the instructions [here](https://help.github.com/articles/creating-a-pull-request/).

In case you feel you've made a valuable contribution, but you don't know how to write code for it, or how to generate the documentation; don't let this discourage you from making the pull request. We can help you! Just go ahead and submit the pull request. But keep in mind that you might be asked to append additional commits to your pull request.