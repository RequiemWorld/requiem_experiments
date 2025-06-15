import os
from airhelper import AirSDKExecutionHelper
from airhelper import SimplifiedBundlingOptions
from airhelper import ActionscriptToCaptiveRuntimeHelper



def main() -> None:
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("actionscript_root_path", help="the root actionscript file of the project to compile/bundle with the captive runtime")
	parser.add_argument("captive_runtime_output_path", help="the root actionscript file of the project to compile/bundle with the captive runtime")
	parser.add_argument("--runtime-executable-name", help="the name that the executable in the directory for the captive runtime should have e.g. Application (which will be Application.exe)")
	parser.add_argument("--window-title", help="the title that the window should have when the application is started")
	parser.add_argument("--version-number", help="the version number of the application")

	arguments = parser.parse_args()

	if arguments.version_number is None:
		version_number = "0.0"
	else:
		version_number = arguments.version_number
	if arguments.window_title is None:
		window_title = "Window Title"
	else:
		window_title = arguments.window_title

	air_execution_helper = AirSDKExecutionHelper.from_environment_path()
	actionscript_to_runtime_helper = ActionscriptToCaptiveRuntimeHelper(
		air_execution_helper,
		SimplifiedBundlingOptions(
			arguments.captive_runtime_output_path,
			arguments.runtime_executable_name,
			application_version_number=version_number,
			application_window_title=window_title,
		),
		arguments.actionscript_root_path,
	)
	actionscript_to_runtime_helper.do_whole_shebang()


if __name__ == "__main__":
	main()