## pySolarCalc
Solar design and NEC calculations implemented with a python backend and excel front end.

My experience working in the solar industry is that every firm has their own excel spreadsheet (often a bit unwieldy) to perform solar design calculations and NEC compliant cable and conduit calculations.

This approach works, but there are enough calculations and table lookups that the calculation stream often becomes confusing.  Additionally, version control is not always easy with Excel.

The goal of this project is to create a efficient and user-friendly solar design tool that is open source.  

## Future Development
* Database of inverters and modules
* Climatic design condition lookup
* String sizing tool
* DC/AC loading calculation
* DC & AC NEC compliant conduit and cable sizing

## Contributing
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
