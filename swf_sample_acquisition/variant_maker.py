from __future__ import annotations

import argparse
import os.path
import subprocess
import sys
import enum
import shutil
import tempfile
from typing import LiteralString


def determine_air_sdk_bin_directory_path(provided_argument: str | None) -> str | None:
	"""
	Determines the path to an AIR sdk bin directory to use, either an argument for it
	is provided, or one is inferred based on the utilities in the path on the system.
	"""
	if provided_argument is not None:
		return provided_argument

	# the bin directory for AIR should be the one that the mxmlc utility in the path is.
	mxmlc_utility_location = shutil.which("mxmlc")
	if mxmlc_utility_location is None:
		return None
	mxmlc_utility_parent_directory_path = os.path.dirname(mxmlc_utility_location)
	return mxmlc_utility_parent_directory_path


def get_path_to_swf_compress_in_directory(directory: str) -> str | None:
	"""
	Takes the path to a directory and finds the path to the swfcompress
	script file in the directory, returning None if it can't be found.
	"""
	swf_compress_path = os.path.join(directory, "swfcompress.bat")
	if os.path.exists(swf_compress_path):
		return swf_compress_path
	else:
		return None


def get_path_to_mxmlc_in_directory(directory: str) -> str | None:
	mxmlc_path = os.path.join(directory, "mxmlc.bat")
	if os.path.exists(mxmlc_path):
		return mxmlc_path
	else:
		return None


class _CompressionAlgorithm(enum.Enum):
	LZMA = "lzma"
	ZLIB = "zlib"


class SWFVariantMaker:
	"""
	Encapsulates the whole process of taking a SWF, compiling it, and creating
	three copies of it with different compressions (one with none).
	"""

	def __init__(self,
				 mxmlc_path: str,
				 swf_compress_path: str,
				 air_sdk_bin_directory: str,
				 actionscript_file_path: str):
		self._mxmlc_path = mxmlc_path
		self._swf_compress_path = swf_compress_path
		self._air_sdk_bin_directory = air_sdk_bin_directory
		self._actionscript_file_path = actionscript_file_path
		self._temporary_directory = tempfile.TemporaryDirectory()
		# the path to the SWF that is compiled first with no compression to transform
		self._uncompressed_swf_path: str | None = None

	def _run_compile_command(self, swf_output_path: str):
		compile_command = [
			self._mxmlc_path,
			self._actionscript_file_path,
			"-output", swf_output_path,
			"-compress=false",
		]
		# devnull is being redirected to (to silence the process output) instead of a new pipe because I'm pretty
		# sure there are technically implications of giving a proper pipe to an application that won't be read from and can fill up.
		subprocess.check_call(compile_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

	@staticmethod
	def _assert_swf_is_fws_variant(swf_path: str):
		with open(swf_path, "rb") as f:
			if f.read(3) != b"FWS":
				raise AssertionError()

	@staticmethod
	def _assert_swf_is_zws_variant(swf_path: str):
		with open(swf_path, "rb") as f:
			if f.read(3) != b"ZWS":
				raise AssertionError()

	@staticmethod
	def _assert_swf_is_cws_variant(swf_path: str):
		with open(swf_path, "rb") as f:
			if f.read(3) != b"CWS":
				raise AssertionError()

	def _compress_and_re_output_compiled_swf(self, output_swf_path: str, algorithm: _CompressionAlgorithm):
		self._assert_swf_is_fws_variant(self._uncompressed_swf_path)
		command = [
			self._swf_compress_path,
			"-compress", self._uncompressed_swf_path,
			"-algorithm", algorithm.value,
			"-output", output_swf_path,
		]
		# during the making of this (using it prior), the swfcompress script
		# would not work if the current directory wasn't the bin directory.
		subprocess.check_call(command, cwd=self._air_sdk_bin_directory, stdout=subprocess.DEVNULL,
							  stderr=subprocess.DEVNULL)
		# devnull is being redirected to (to silence the process output) instead of a new pipe because I'm pretty
		# sure there are technically implications of giving a proper pipe to an application that won't be read from and can fill up.
		if algorithm is _CompressionAlgorithm.LZMA:
			self._assert_swf_is_zws_variant(output_swf_path)
		if algorithm is _CompressionAlgorithm.ZLIB:
			self._assert_swf_is_cws_variant(output_swf_path)

	def compile_actionscript_file(self):
		"""
		:raises RuntimeError: When the actionscript file has already been compiled.
		"""
		if self._uncompressed_swf_path is not None:
			raise RuntimeError("swf has already been compiled by this instance")

		output_swf_path = os.path.join(self._temporary_directory.name, "uncompressed_swf.swf")
		self._run_compile_command(output_swf_path)
		self._uncompressed_swf_path = output_swf_path
		self._assert_swf_is_fws_variant(output_swf_path)

	def make_fws_variant(self, output_swf_path: str) -> None:
		"""
		Makes a variant of SWF that has no compression for the actionscript file.
		The actionscript file must have been compiled with the compile_actionscript_file method first.
		"""
		if self._uncompressed_swf_path is None:
			raise RuntimeError("the actionscript file hasn't been compiled to a swf yet.")
		# we just copy the original which isn't compress to here
		self._assert_swf_is_fws_variant(self._uncompressed_swf_path)
		shutil.copy(self._uncompressed_swf_path, output_swf_path)

	def make_cws_variant(self, output_swf_path: str) -> None:
		"""
		Makes a variant of SWF that has zlib compression for the actionscript file.
		The actionscript file must have been compiled with the compile_actionscript_file method first.
		"""
		if self._uncompressed_swf_path is None:
			raise RuntimeError("the actionscript file hasn't been compiled to a swf yet.")
		self._compress_and_re_output_compiled_swf(output_swf_path, _CompressionAlgorithm.ZLIB)

	def make_zws_variant(self, output_swf_path: str) -> None:
		"""
		Makes a variant of SWF that has lzma compression for the actionscript file.
		The actionscript file must have been compiled with the compile_actionscript_file method first.
		"""
		if self._uncompressed_swf_path is None:
			raise RuntimeError("the actionscript file hasn't been compiled to a swf yet.")
		self._compress_and_re_output_compiled_swf(output_swf_path, _CompressionAlgorithm.LZMA)


def _add_signature_string_to_swf_name(file_name: str, signature_string):
	if "." not in file_name:
		return file_name + "-" + signature_string
	else:
		name_part, extension_part = file_name.rsplit(".", 1)
		return name_part + "-" + signature_string + "." + extension_part


def main() -> None:
	# A script for taking an actionscript file and compiling it and
	# producing a copy with each variation of compression (none, zlib, lzma) (fws, cws, zws).
	#
	# The preferred way to use this script is to add the bin directory of the air sdk to the system
	# path, so that the script can infer where the bin directory is, and use mxmlc and swfcompress nicely.
	#
	# Swfcompress is one of the newer additions to the airsdk since harmon took over, this has been manually
	# testd against:
	if sys.platform != "win32":
		print("only windows is supported at this time (use a windows vm or try wine)")
		return
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"actionscript_path",
		help="the path to the root actionscript file to compile, should usually be a single file in this case.")
	parser.add_argument(
		"base_output_name",
		help="this will be what the output is suffixed with (e.g. BaseName.swf, then output fws-BaseOutputName.swf)")
	parser.add_argument(
		"--output-directory",
		help="this will be the directory that the actionscript is made into the three variants of swfs to, current working directory by default")
	parser.add_argument(
		"--air-sdk-bin-path",
		help="path to the bin directory of an air sdk containing mxmlc and swfcompress. inferred from environment path if not provided")

	arguments = parser.parse_args()
	# right now this is effectively hardcoded to only automatically find mxmlc and swfcompress from the environment paths
	air_sdk_bin_directory = determine_air_sdk_bin_directory_path(None)
	if air_sdk_bin_directory is None:
		print(
			"unable to find path to the bin directory of an AIR sdk, one wasn't provided and or one couldn't be inferred.")

	mxmlc_path = get_path_to_mxmlc_in_directory(air_sdk_bin_directory)
	swf_compress_path = get_path_to_swf_compress_in_directory(air_sdk_bin_directory)
	assert mxmlc_path is not None and swf_compress_path is not None
	actionscript_file_path = arguments.actionscript_path
	swf_variant_maker = SWFVariantMaker(
		mxmlc_path,
		swf_compress_path,
		air_sdk_bin_directory=air_sdk_bin_directory,
		actionscript_file_path=actionscript_file_path)
	if arguments.output_directory is None:
		output_directory = os.getcwd()
	else:
		output_directory = os.path.abspath(arguments.output_directory)
		if not os.path.exists(arguments.output_directory) or not os.path.isdir(arguments.output_directory):
			print("output directory doesn't exist or isn't a directory.")
	base_output_name = arguments.base_output_name
	adjusted_output_name_fws = _add_signature_string_to_swf_name(base_output_name, "fws")
	adjusted_output_name_cws = _add_signature_string_to_swf_name(base_output_name, "cws")
	adjusted_output_name_zws = _add_signature_string_to_swf_name(base_output_name, "zws")

	swf_variant_maker.compile_actionscript_file()
	fws_output_path = os.path.join(output_directory, adjusted_output_name_fws)
	cws_output_path = os.path.join(output_directory, adjusted_output_name_cws)
	zws_output_path = os.path.join(output_directory, adjusted_output_name_zws)
	swf_variant_maker.make_fws_variant(fws_output_path)
	print(f"made no compression variant of swf for {actionscript_file_path} at {fws_output_path}")
	swf_variant_maker.make_zws_variant(zws_output_path)
	print(f"made lzma compression variant of swf for {actionscript_file_path} at {zws_output_path}")
	swf_variant_maker.make_cws_variant(cws_output_path)
	print(f"made zlib compression variant of swf for {actionscript_file_path} at {cws_output_path}")


if __name__ == '__main__':
	main()