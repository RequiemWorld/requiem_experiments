import pexpect


class ShellOrientedProcessReader:
    def __init__(self, spawn: pexpect.spawn):
        self._spawn = spawn
        self._buffer = bytearray()

    def read_until_and_erase(self, exact_match: str) -> str:
        exact_match_bytes = exact_match.encode()
        while True:
            try:
                data = self._spawn.read_nonblocking(4096, timeout=1)
                self._buffer.extend(data)
                if exact_match_bytes in self._buffer:
                    match_start_index = self._buffer.find(exact_match_bytes)
                    match_stop_index = match_start_index + len(exact_match_bytes)
                    all_data_before_match = self._buffer[:match_start_index]
                    self._buffer = self._buffer[match_stop_index:]
                    return all_data_before_match.decode()
            except pexpect.TIMEOUT:
                continue
            except pexpect.EOF:
                raise EOFError("Program exited")


class PexpectBashInteractor:
    """
    A utility for interacting with a bash terminal over pexpect. Pexpect
    uses a pseudo terminal that processes lines and provides them with \r\n instead of \n.
    """
    def __init__(self, spawn: pexpect.spawn):
        self._spawn = spawn
        self._reader = ShellOrientedProcessReader(spawn)

    def execute_command(self, command: str) -> str:
        """
        Executes a command and returns the output of the command as a string with
        each line ending in \r\n instead of \n.
        """
        start_marker = f"__COMMAND_STARTED__"
        finish_marker =f"__COMMAND_FINISHED__"
        self._spawn.sendline(f"echo {start_marker}; {command}; echo {finish_marker}")
        # I'm pretty sure the PTY reads the lines and sends them back with \r\n instead of \n
        self._reader.read_until_and_erase(start_marker + "\r\n")
        command_output = self._reader.read_until_and_erase("\r\n" + finish_marker + "\r\n")
        return command_output


# https://serverfault.com/questions/593399/what-is-the-benefit-of-not-allocating-a-terminal-in-ssh
# https://unix.stackexchange.com/questions/343324/why-in-the-output-of-script-1-the-newline-is-cr-lf-dos-style
# This is significantly slower on python3.8 than python3.13 for some reason.
spawn = pexpect.spawn("/bin/bash", echo=False)
interactor = PexpectBashInteractor(spawn)
print(interactor.execute_command("echo fsfosafkafopkfpasokf"))
print(interactor.execute_command("cat /etc/os-release"))

