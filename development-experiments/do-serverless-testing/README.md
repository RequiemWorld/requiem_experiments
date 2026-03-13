# Purpose of Experiment

The purpose of this experiment is to develop digitalocean functions and test them locally. As convenient as it might be to test in a sandbox namespace or something on every change... certain stuff such as connecting to databases spun up via testcontainers would be better suited for locally.

- Additionally, it is undesirable to have to push to an actual environment to get feedback on changes, not that there isn't a place for it.

## Writing a function
The following is my current understanding of the process that takes place for digitalocean. It may be wrong.
- Available functions are specified in project.yml, each function has a directory at a path that will be discovered by package and function name.
- Each function in a package is built into something to be executed by the runtime.
    - A single file function directory such as "sample/hello/hello.py" will result in a zip file with the file being the only thing inside.
- Each function directory will contain a python file which is the entry point with a main function that is executed by the runtime with a dictionary of arguments.

## Execution of a function
- The runtime (at some point) will take an unzipped copy of everything\* in our function directory and execute the main function specified in the project.yml.
    - This directory does not contain the project.yml.
    - This was discovered by something like a left over ``__deploy__.zip`` from running the relevant command to deploy with ``doctl``.
- The runtime appears to be in practice, executing the function in the relevant python file. A python file is provided, it is executed, we are likely dealing with a blank slate of an interpreter similar to writing github actions and nodejs.