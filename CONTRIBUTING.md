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

## Documentation and Test Driven Development
This project tries to adhere to a development process that is driven by development of clear documentation and unit tests. Here are the steps to follow when developing new code contributions:
- Write the function signature and a complete docstring. These should be written together.
- Write a unit test that uses the function as described by the docstring using the function name and argument names you have defined.
- Some back and forth between these two steps is appropriate to settle on names and a function signature that result in the best API. Take the time now to think deeply about the names; naming things is hard and it is even harder to rename them!
- Run your new tests locally. They should fail because you have not yet written the code in the function. This is a good time to generate a pull request, so that others can review selected names, the boundaries of your function, and your tests before you spend time writing the function code.
- Use the function signature, docstring, and unit tests as guides/checklist to write the function code itself (finally!).
- Once all the unit tests are passing, push all your commits up to your branch/pull request so they can be reviewed.
- If everyone is happy with the result, the new code will be merged.
