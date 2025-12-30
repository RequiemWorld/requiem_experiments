## Purpose of Experiment
- The purpose of this experiment is to use pexpect to interact with a shell in a subprocess and conveniently get the command output. This is necessary for automated testing of command line applications e.g. to drop into a shell in a docker container and verify things work as expected. 

## Discovery 1 - \n rewritten to \r\n

- Pexpect uses a psuedo terminal (pty) to be able to interact with the program like the user would in the terminal.
  - The psuedo terminal processes lines from the application and outputs them with a \r\n instead of \n.

## Discovery 2 - input is seen in the output read
  - The output of the psuedo terminal output what is sent with ``pexpect.spawn.sendline`` like a real terminal would. **Echo can be disabled with echo=False in the spawn constructor.**

## Discovery 3 - escape sequences
- There is a lot of data for controlling the terminal when commands are executed. It makes it more difficult to read the output of commands. The solution I've chosen is to prefix each command with ``__COMMAND_START__`` and ``__COMMAND_FINISH__`` so that the only concern is finding the command start and then the command finish and erasing it, getting the desired output.
