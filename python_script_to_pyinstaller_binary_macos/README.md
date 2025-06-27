## Purpose of Experiment

Write a script to go from a python script on MacOS to a binary. Familiarizing with pyinstaller on MacOS. Lay way for automating the process as part of broader bundling code on the project and capture basic information such as file sizes. 

## Example Usage
```
python3 script_to_binary.py --source-script-path hello_name_repeat.py --destination-binary-path hello_name_repeat_binary
```
## Example Result
```
python_script_to_pyinstaller_binary_macos
├── README.md
├── hello_name_repeat.py
├── hello_name_repeat_binary
└── script_to_binary.py

1 directory, 4 files
```

## Experienced Issues
- Python bin directories containing executable stuff such as pyinstaller not in the path with the installed version.
  - zsh: command not found: pyinstaller
  - Attempting to access it by the python interpreter in the path with python3 -m pyinstaller resulted in /Library/Developer/CommandLineTools/usr/bin/python3: No module named pyinstaller
    - Resolved [wip] with advice of https://stackoverflow.com/questions/44740792/pyinstaller-no-module-named-pyinstaller

## Conclusion
- With minimal effort, with the requirement of having familiarized with where the binaries are placed, not unlike with windows, we can take a python script on MacOS and turn it into a binary at a given path which we can then distribute.
  - Previous experimentation has revealed that the only user friendly way to distribute these binaries is in zip files so that they are extracted with the "execute" permissions set.
- The placement of --one-file binaries on MacOS are the script name without the extension, under the current working directory ./dist/{script_name_without_extension}.
  - The file at this path is made executable automatically, meaning it can be double-clicked and opened or ran from the command line with no additional effort.
    - When adding it to a zip file, assuming permissions are copied over, the end user should be able to double click it after extraction.
    - We should be verifying in some way that the file that will be inside our prepared archives is executable, and the right format after creating it.  
- The minimal binary size or at least, what we should be expecting for a script that does basically nothing is around three megabytes.
- At no point did we worry about adding anything to the path, the python interpreter was already in it, and when executing the script to bundle everything, it has access to where it is via ``sys.executable``.

