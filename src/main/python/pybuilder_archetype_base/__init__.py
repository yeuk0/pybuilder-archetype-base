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

from pathlib import Path

from pybuilder.core import depends, init, task

import pybuilder_archetype_base.messages as msg
from pybuilder_archetype_base.errors import MissingPropertyError
from pybuilder_archetype_base.helpers import Builder, Utils


@init
def initialise_plugin(project):
	"""
	Sets project defaults.

	:param pybuilder.core.Project project: PyBuilder project instance
	:return: None
	"""
	project.set_property('pycharm_workspace_project_path', project.get_property('project_base_path'))

	project_name = Utils.underscore(project.name)

	directories = {
		'BIN': Path('bin'),
		'DOCS': Path('docs'),
		'SRC': Path('src'),
		'TESTS': Path('tests')
	}
	directories_2nd = {
		'CONFIG_LOGGER': directories['SRC'] / project_name / 'config' / 'logger'
	}
	directories.update(directories_2nd)
	project.set_property('base_directories', directories)

	packages = {
		'CONFIG': Path('config'),
		'CORE': Path('core'),
		'ERRORS': Path('errors'),
		'UTILS': Path('utils')
	}
	packages_2nd = {
		'UTILS_LOGGER': packages['UTILS'] / 'loggers',
		'ERRORS_CORE': packages['ERRORS'] / 'core'
	}
	packages.update(packages_2nd)
	project.set_property('base_packages', packages)

	templates_first_level = {
		'GITIGNORE': 'gitignore',
		'README': 'README.md',
		'REQUIREMENTS': 'requirements.txt',
		'SETUP': 'setup.py',
		'TEST_EXAMPLE': directories['TESTS'] / 'test_example.py',
		'TEST_INIT': directories['TESTS'] / '__init__.py'
	}
	project.set_property('base_templates_first_level', templates_first_level)

	templates_second_level = {
		'CONSTANTS': packages['CONFIG'] / 'constants.py',
		'MESSAGES': packages['CONFIG'] / 'messages.py',
		'LOGGER_YML': packages['CONFIG'] / 'logger' / 'logger.yml',
		'LOGGER_INIT': packages['UTILS_LOGGER'] / '__init__.py',
		'LOGGER_HANDLERS': packages_2nd['UTILS_LOGGER'] / 'handlers.py',
		'HELPERS': packages['UTILS'] / 'helpers.py'
	}
	project.set_property('base_templates_second_level', templates_second_level)


@task(description=msg.TASK_DESCRIPTION_CREATE_ARCHETYPE_BASE)
@depends('generate_pycharm_workspace')
def create_archetype_base(project, logger):
	"""
	Main plugin task.

	It creates the entire project skeleton with some base packages and scripts that can help during a project
	fresh start.

	:param pybuilder.core.Project project: PyBuilder project instance
	:param pybuilder.core.Logger logger: PyBuilder logger instance
	:return: None
	"""
	logger.info(msg.ARCHETYPE_START)
	if not project.get_property('project_base_path'):
		raise MissingPropertyError('project_base_path')

	builder = Builder(logger)
	project_path = Path(Utils.underscore(project.name))

	logger.info(msg.ARCHETYPE_DIRECTORIES)
	for directory in project.get_property('base_directories').values():
		builder.create_directory(project_path, directory, False)

	logger.info(msg.ARCHETYPE_PACKAGES)
	for package in project.get_property('base_packages').values():
		builder.create_directory(project_path, package, True)

	logger.info(msg.ARCHETYPE_EMPTY_FILE.format(file='LICENSE'))
	builder.create_empty_file(Path('.'), 'LICENSE')

	logger.info(msg.ARCHETYPE_TEMPLATES_ROOT)
	for template in project.get_property('base_templates_first_level').values():
		builder.copy_file_templates(Path('.'), Path(__file__).parent, template)

	logger.info(msg.ARCHETYPE_TEMPLATES_PACKAGE)
	for template in project.get_property('base_templates_second_level').values():
		builder.copy_file_templates('src' / project_path, Path(__file__).parent, template)

	logger.info(msg.ARCHETYPE_INIT_FILE)
	for package in project.get_property('base_packages').values():
		builder.create_init(project_path, Path(__file__).parent, package)

	logger.info(msg.ARCHETYPE_FINISH)
