import os
import argparse
from airhelper import AirSDKExecutionHelper
from airhelper import SwfToCaptiveRuntimeHelper
from airhelper import SimplifiedBundlingOptions

parser = argparse.ArgumentParser()
# for this experiment on this mac, it isn't added to the path to find,
# and we are specifying the path to the downloaded/extracted directory manually.
parser.add_argument("--air-sdk-bin-path", required=True)
parser.add_argument("--source-swf-path", required=True)
parser.add_argument("--executable-name", required=True)
parser.add_argument("--window-title", required=True)
# This is a specially structured directory that gets .app appended to the name
# where an executable inside will be executed when clicked, it might also be signed.
#
# The executable name (filename), for context, will show up in top as the name of the process,
# and the binary used in the directory will have it as the name inside of it.
# https://v2.tauri.app/distribute/macos-application-bundle/
parser.add_argument(
    "--runtime-output-path",
    help="the path to output the captive runtime to, will be a directory ending in .app",
    required=True)

arguments = parser.parse_args()

air_sdk_binaries_directory_path = arguments.air_sdk_bin_path
source_swf_path = arguments.source_swf_path
internal_executable_name = arguments.executable_name
# ^ internal because it's only going to show inside the directory, and in processes.
runtime_output_path = arguments.runtime_output_path
window_title = arguments.window_title
assert os.path.exists(air_sdk_binaries_directory_path), "not an existing path to the bin directory"
assert os.path.exists(source_swf_path), "not an existing path to any file let alone a swf to bundle"

adt_utility_path = os.path.join(air_sdk_binaries_directory_path, "adt")
mxmlc_utility_path = os.path.join(air_sdk_binaries_directory_path, "mxmlc")
execution_helper = AirSDKExecutionHelper(adt_path=adt_utility_path, mxmlc_path=mxmlc_utility_path)
swf_to_captive_runtime_helper = SwfToCaptiveRuntimeHelper(
    source_swf_path=source_swf_path,
    execution_helper=execution_helper,
    bundling_options=SimplifiedBundlingOptions(
        # the name given will result in a directory with {name}.app
        output_captive_runtime_root=runtime_output_path,
        # for the filename option in the application descriptor
        executable_name_in_directory=internal_executable_name,
        application_version_number="0.1",
        application_window_title=window_title))
swf_to_captive_runtime_helper.produce_captive_runtime()
expected_application_bundle_output_path = runtime_output_path + ".app"
if not os.path.exists(expected_application_bundle_output_path):
    print(f"the bundle was not created by this script as expected, expected output to {expected_application_bundle_output_path}")
else:
    print(f"the bundle was created as expected at the path {expected_application_bundle_output_path}")
