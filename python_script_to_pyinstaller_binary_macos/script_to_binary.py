
import shutil
import os
import sys
import tempfile
import argparse
import subprocess


def script_to_binary(script_path: str, destination_binary_path: str) -> None:
    if not script_path.endswith(".py"):
        raise ValueError("the source script should have a .py extension for the simple intended usage")
    script_name_without_extension = script_path[0:-3]
    with tempfile.TemporaryDirectory() as temp_directory:
        command = [sys.executable, "-m", "PyInstaller", os.path.abspath(script_path), "-F"]
        subprocess.check_call(command, cwd=temp_directory)
        # e.g. ./dist/hello_name_repeat
        ready_binary_path = os.path.join(temp_directory, "dist", script_name_without_extension)
        shutil.copy(ready_binary_path, destination_binary_path)

parser = argparse.ArgumentParser()
parser.add_argument("--source-script-path", required=True)
parser.add_argument("--destination-binary-path", required=True)

arguments = parser.parse_args()

script_to_binary(arguments.source_script_path, arguments.destination_binary_path)