# Contributing
This document provides some basic guidelines and workflows to follow to contribute to the project.

## Github Workflow and Conda Development Environment Setup
To make contributions please follow these steps and get in touch if
there are any questions.

- Fork the project on Github
- Clone to your computer
- Setup conda env for project using the environment yml file in ci/  
-- conda env create -f environment.yml  
-- conda activate pySolarCalc  
-- conda install -c conda-forge jupyterlab  
-- conda install nodejs  
-- jupyter labextension install @pyviz/jupyterlab_pyviz
- Create branch for your proposed changes
- Make initial commit to your new branch
- Push commit(s) to your Github account
- Create a pull request
- Write unit tests for any new code
- New code must adhere to PEP8 and have a unit test to be merged, both are checked by Travis CI
