from __future__ import annotations
import os
import shutil
import subprocess
from tempfile import TemporaryDirectory


class AirSdkExecutor:
	def __init__(self, bin_directory: str) -> None:
		self._bin_directory = bin_directory

	@staticmethod
	def from_environment_paths() -> "AirSdkExecutor":
		mxmlc_utility_path = shutil.which("mxmlc")
		assert mxmlc_utility_path is not None
		mxmlc_utility_parent_directory = os.path.basename(mxmlc_utility_path)
		return AirSdkExecutor(mxmlc_utility_parent_directory)

	def _execute_utility(self, utility_name: str, arguments: list[str], cwd: str | None = None) -> None:
		utility_path = shutil.which(utility_name)
		# assert os.path.exists(utility_path), f"{utility_name} not in bin directory"
		subprocess.check_call([utility_path] + arguments, cwd=cwd)

	def execute_utility(self, utility_name: str, arguments: list[str], cwd: str | None = None):
		self._execute_utility(utility_name, arguments, cwd=cwd)


class AirSdkHelperEphemeralSigningContext:
	"""
	An ephemeral context for what is needed to sign an AIR
	application with a key that will be thrown away.
	"""
	def __init__(self, sdk_executor: AirSdkExecutor):
		# this is trashy to have all this in the constructor, but I'm not putting
		# more thought/design into architecture for this right now.
		self._temp_directory = TemporaryDirectory()
		self._pkcs_file_path = os.path.join(self._temp_directory.name, "signing-stuff.pkcs")
		self._generate_pkcs_file(sdk_executor, self._pkcs_file_path)

	@staticmethod
	def _generate_pkcs_file(sdk_executor: AirSdkExecutor, output_path: str) -> None:
		arguments = [
			"-certificate",
			"-cn", "RequiemWorld",
			"-validityPeriod", "15",  # years
			"2048-RSA",  # key
			output_path,  # output
			"password"]
		sdk_executor.execute_utility("adt", arguments)

	@property
	def pkcs_file_path(self) -> str:
		return self._pkcs_file_path

	def get_signing_arguments(self) -> list[str]:
		signing_arguments = [
			"-storetype", "pkcs12",
			"-keystore", self._pkcs_file_path,
			"-storepass", "password"
		]
		# keeps getting errors if any server is used for this, so I've set it to None
		# since it probably doesn't even apply to self signed certificates anyway.
		"-tsa", "none",
		return signing_arguments

class RelevantApplicationDescriptorOptions:
	def __init__(self,
				 identifier: str = "com.requiemworld.airhelper",
				 version_number: str = "1.0"):
		self.identifier = identifier
		self.version_number = version_number

class ActionscriptToCaptiveRuntimeHelper:
	def __init__(self,
				 actionscript_file: str,
				 air_sdk_executor: AirSdkExecutor,
				 ephemeral_signing_context: AirSdkHelperEphemeralSigningContext):
		self._actionscript_file = actionscript_file
		self._air_sdk_executor = air_sdk_executor
		self._ephemeral_signing_context = ephemeral_signing_context
		self._temporary_directory = TemporaryDirectory()
		self._compiled_swf_path: str | None = None

	def compile_actionscript_to_swf(self):
		swf_output_path = os.path.join(self._temporary_directory.name, "application.swf")
		compiler_arguments = [
			self._actionscript_file,
			"-output", swf_output_path,
			"-compress=false",
			"-debug=false"]
		self._air_sdk_executor.execute_utility("mxmlc", compiler_arguments)
		self._compiled_swf_path = swf_output_path

	def make_application_descriptor_for_swf(self):
		descriptor = """<?xml version="1.0" encoding="utf-8" ?>
		<application xmlns="http://ns.adobe.com/air/application/51.0">
		    <id>com.harman.air.SwfEncrypt</id> 
		    <versionNumber>1.0</versionNumber> 
		    <filename>Encrypt.exe</filename> 

		    <name>SWF Encrypt</name> 
		    <description></description> 
		    <copyright>(c) 2021 HARMAN Connected Services, Inc.</copyright> 

		    <initialWindow> 
		        <title>SWF Encrypt</title> 
		        <content>application.swf</content> 
		        <systemChrome>standard</systemChrome> 
		        <transparent>false</transparent> 
		        <visible>true</visible> 
		        <minimizable>true</minimizable> 
		        <maximizable>true</maximizable> 
		        <resizable>true</resizable> 
		    </initialWindow> 

		    <!-- 
		    More options:
		    http://livedocs.adobe.com/flex/3/html/File_formats_1.html#1043413
		    -->
		</application>"""

		descriptor_output_path = os.path.join(self._temporary_directory.name, "application.xml")
		with open(descriptor_output_path, "w") as f:
			f.write(descriptor)

	def build_captive_runtime_from_swf_and_descriptor(self, output_directory: str) -> None:
		pkcs_file_path = self._ephemeral_signing_context.pkcs_file_path
		# adt -package SIGNING_OPTIONS? -target bundle SIGNING_OPTIONS? ARCH_OPTIONS? <output-package> ( <app-desc> FILE-AND-PATH-OPTIONS | <input-package> )
		# signing options do not seem to e optional, just the position they appear seems to be.
		arguments = [
			"-package",
		]
		# SIGNING_OPTIONS      : -storetype <type> ( -keystore <store> )? ( -storepass <pass> )? ( -alias <aliasName> )? ( -keypass <pass> )? ( -providerName <name> )? ( -providerClass <name> -providerArg <configFile> )? ( -tsa <url> )? ( -provisioning-profile <profile> )?
		arguments += [
			"-storetype", "pkcs12",
			"-keystore", pkcs_file_path,
			"-storepass", "password",
			# keeps getting errors if any server is used for this, so I've set it to None
			# since it probably doesn't even apply to self signed certificates anyway.
			"-tsa", "none",
		]
		arguments += [
			"-target", "bundle"
		]
		descriptor_path = os.path.join(self._temporary_directory.name, "application.xml")
		captive_runtime_output_directory = os.path.abspath(output_directory)
		arguments += [
			captive_runtime_output_directory,
			descriptor_path,
			"application.swf",
		]
		self._air_sdk_executor.execute_utility("adt", arguments, cwd=self._temporary_directory.name)


def main() -> None:
	sdk_executor = AirSdkExecutor.from_environment_paths()
	ephemeral_signing_context = AirSdkHelperEphemeralSigningContext(sdk_executor)
	print(ephemeral_signing_context.pkcs_file_path)
	actionscript_to_captive_runtime_helper = ActionscriptToCaptiveRuntimeHelper(
		actionscript_file="SetBackground/SetBackground.as",
		air_sdk_executor=sdk_executor,
		ephemeral_signing_context=ephemeral_signing_context)
	actionscript_to_captive_runtime_helper.compile_actionscript_to_swf()
	actionscript_to_captive_runtime_helper.make_application_descriptor_for_swf()
	actionscript_to_captive_runtime_helper.build_captive_runtime_from_swf_and_descriptor("./captive-runtime")
if __name__ == '__main__':
	main()