import os


class LocalToRemoteFileWalker:
	"""
	Traverses a directory from the top down and gives the absolute
	local paths of files to upload along with where to upload to remotely.
	"""
	def __init__(self, local_directory_path: str, remote_directory_path: str):
		self._local_directory_path = local_directory_path
		self._remote_directory_path = remote_directory_path

	def walk(self) -> tuple[str, str]:
		"""
		Yields tuples of (local_path, remote_path) for each file found
		in the local directory tree.
		"""
		for root, _, files in os.walk(self._local_directory_path):
			for file in files:
				local_path = os.path.join(root, file)
				relative_path = os.path.relpath(local_path, self._local_directory_path)
				remote_path = os.path.join(self._remote_directory_path, relative_path)
				yield local_path, remote_path
