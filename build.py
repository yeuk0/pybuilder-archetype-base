#   -*- coding: utf-8 -*-
#   Copyright 2020 Arturo González, Diego Barrantes
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

from datetime import datetime
from pathlib import Path

from pybuilder.core import Author, before, init, use_plugin


use_plugin('python.core')
use_plugin('python.distutils')

use_plugin('pypi:pybuilder_pycharm_workspace')

name = 'pybuilder-archetype-base'
version = '0.1.1'
license = "Apache License, Version 2.0"

authors = [Author("Arturo GL", 'r2d2006@hotmail.com'), Author("Diego BM", 'diegobm92@gmail.com')]
url = 'https://github.com/yeuk0/pybuilder-archetype-base'
summary = "External plugin for PyBuilder to generate a base project structure"
markdown_encoding = 'utf8'
description = open('README.md', encoding=markdown_encoding).read()

default_task = ['clean', 'publish']


@init
def initialise(project):
	project.set_property('distutils_readme_file_type', 'text/markdown')
	project.set_property('distutils_readme_file_encoding', markdown_encoding)


@before('prepare')
def pack_files(project):
	"""
	Includes non-Python files in the build.
	
	The plugin must contain every file present in ``resource`` package. 

	:param pybuilder.core.Project project: PyBuilder project instance
	:return: None
	"""
	# https://github.com/pybuilder/pybuilder/issues/127#issuecomment-350513803
	package_path = list(Path(__file__).parent.glob('src/main/python/*'))[0]
	resources_paths = sorted(package_path.glob('resources/**'))
	project.package_data.update(
		{ package_path.name: [str((path.relative_to(package_path) / '*').as_posix()) for path in resources_paths] })
