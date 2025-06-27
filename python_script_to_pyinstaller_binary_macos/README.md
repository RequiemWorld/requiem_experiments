## Purpose of Experiment

Write a script to go from a python script on MacOS to a binary. Lay way for automating the process as part of broader bundling code on the project and capture basic information such as file sizes.


## Experienced Issues
- Python bin directories containing executable stuff such as pyinstaller not in the path with the installed version.
  - zsh: command not found: pyinstaller
  - Attempting to access it by the python interpreter in the path with python3 -m pyinstaller resulted in /Library/Developer/CommandLineTools/usr/bin/python3: No module named pyinstaller
    - Resolved [wip] with advice of https://stackoverflow.com/questions/44740792/pyinstaller-no-module-named-pyinstaller
