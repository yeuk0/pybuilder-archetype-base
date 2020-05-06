#   -*- coding: utf-8 -*-
#   Copyright 2020 Diego Barrantes
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import re
from pathlib import Path
from shutil import copy, move

import pybuilder_archetype_base.messages as msg


class Utils():
	"""
	Class including some utils.
	"""

	@staticmethod
	def underscore(word):
		"""
		``underscore()`` function taken from ``inflection`` library.

		More information:
			https://inflection.readthedocs.io/en/latest/#inflection.underscore

		:param str word: Text to process
		:return: Underscored word with no hyphens and lowercased.
		:rtype: str
		"""
		word = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", word)
		word = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", word)
		word = word.replace('-', '_')
		return word.lower()

	@staticmethod
	def update_requirements(source, dest):
		"""
		Updates base requirements file with plugin's version.

		Checks if the requirement to include is already present in existing ``requirements.txt`` file. If it exists,
		the version is compared with the one on the requirements file. It will be replaced if the new version is
		higher than the previous one. If the Python module to import is not present, it is added to the existing file.

		:param str source: Path to plugin's ``requirements.txt`` file
		:param str dest: Path to project's (destination) ``requirements.txt`` file
		:return: None
		"""
		with open(source, 'r') as source_file, open(dest, 'r+') as dest_file:
			requirements = dict(line.split('==') for line in dest_file.readlines())
			for module in source_file:
				if module in requirements.keys():
					if source_file[module] > requirements[module]:
						requirements[module] = source_file[module]
				else:
					requirements[module] = source_file[module]
			dest_file.writelines(requirements)

	@staticmethod
	def update_file(source, dest):
		"""
		Updates a file with new contents.

		The method opens destination files and append the lines from the source.

		:param str source: Path to file with new contents
		:param str dest: Path to project's (destination) file
		:return: None
		"""
		with open(source, 'r') as source_file, open(dest, 'a') as dest_file:
			dest_file.writelines(source_file.readlines())


class Builder():
	"""
	Class to support project structure building.

	``Builder`` class offers methods to create new Python packages and directories as well as copy file templates to
	new project location.
	"""

	def __init__(self, logger):
		self.logger = logger

	def create_directory(self, project_package, directory_path, python_package):
		"""
		Creates a directory in the new Python project.

		:param Path project_package: Name of project's main package
		:param Path directory_path: Directory path to create
		:param bool python_package: If the directory is a Python package or not
		"""
		directory = 'src' / project_package / directory_path if python_package else Path(directory_path)
		if directory.exists():
			self.logger.debug(msg.BUILDER_DIRECTORY_EXISTS.format(directory=directory))
		else:
			directory.mkdir(parents=True)
			self.logger.debug(msg.BUILDER_DIRECTORY_CREATED.format(directory=directory))

	def create_init(self, project_package, template_source, directory_path):
		"""
		Creates a new ``__init__.py`` file in the directory specified for the new Python project based on a template.

		:param Path project_package: Name of project's main package
		:param Path template_source: Path where the template is located
		:param Path directory_path: Directory path to create
		"""
		directory = 'src' / project_package / directory_path
		if (directory / '__init__.py').exists():
			self.logger.debug(msg.BUILDER_FILE_EXISTS.format(file=(Path(directory) / '__init__.py')))
			return

		directory_init = template_source / 'resources' / '__init__.py'
		copy(directory_init, directory)
		self.logger.debug(msg.BUILDER_FILE_CREATED.format(file=(Path(directory) / '__init__.py')))

	def create_empty_file(self, path, name):
		"""
		Creates a new empty file.

		:param Path path: Location where the new file will be created
		:param str name: Name of the file to create
		"""
		file_path = path / name
		if file_path.exists():
			self.logger.debug(msg.BUILDER_FILE_EXISTS.format(file=file_path))
			return

		open(file_path, 'a').close()
		self.logger.debug(msg.BUILDER_FILE_CREATED.format(file=file_path))

	def copy_file_templates(self, project_package, template_source, directory_path):
		"""
		Copies a template file to a specific location.

		:param Path project_package: Name of project's main package
		:param Path template_source: Path where the template is located
		:param Path directory_path: Directory where the file will be copied
		"""
		file_path = project_package / directory_path
		if file_path.exists():
			self.logger.debug(msg.BUILDER_FILE_EXISTS.format(file=file_path))
			return

		path_from_file = template_source / 'resources' / directory_path
		copy(path_from_file, file_path)
		# Hack to avoid PyBuilder build ignore hidden files
		if path_from_file.name is 'gitignore':
			move(file_path, file_path.parent / '.gitignore')
		self.logger.debug(msg.BUILDER_FILE_CREATED.format(file=file_path))
