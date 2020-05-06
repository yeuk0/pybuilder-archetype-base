# PyBuilder Archetype Base Plugin

This plugin generates a base common structure with no major dependecies. The main idea is to get an skeleton that can
 be used for any kind of Python module. It modifies PyBuilder structure logic lightly, removing some packages making
  it less _Java-like_.

In the following diagram there is every directory and file created during `create_archetype_base`:

```text
bin
docs
src
└── package_name
    ├── config  # For any kind of configuration files or constants
    |   ├── logger
    |   |   └── logger.yml
    |   ├── __init__.py
    |   ├── constants.py
    |   └── messages.py
    ├── core  # Logic of the project itself
    |   └── __init__.py
    ├── errors  # For every custom exception made
    |   ├── core  # Make as many scripts as packages in core (i.e. processing.py for core.processing)
    |   |   └── __init__.py
    |   └── __init__.py
    ├── utils  # For any kind of util used in the project
    |   ├── logging
    |   |   ├── __init__.py
    |   |   └── handlers.yml  # For custom logging handles (i.e. database logging)
    |   ├── __init__.py
    |   └── helpers.py
    └── __init__.py
tests  # For every custom exception made
├── __init__.py
└── example_test.py
.gitignore
LICENSE # Empty file
README.md
requirements.txt
setup.py
```

There are other PyBuilder plugins that depend on pybuilder_archetype_base that include other more specific packages.
These plugins are:

* [pybuilder_archetype_api](https://github.com/yeuk0/pybuilder-archetype-api): For projects focused on web services
* (WIP) ~~[pybuilder_archetype_db](https://github.com/yeuk0/pybuilder-archetype-db): For projects using databases~~

## How to use pybuilder_archetype_base

> **NOTICE**: This plugin only works on Windows due to its dependency with pybuilder_pycharm_workspace PyBuilder
> plugin. Using this plugin in other OS shall not work properly. Multi-platform support soon.

Add plugin dependencies to your `build.py` (it requires [pybuilder_pycharm_workspace](https://github.com/yeuk0/pybuilder-pycharm-workspace)
to work properly):

```python
use_plugin('pypi:pybuilder_archetype_base')
use_plugin('pypi:pybuilder_pycharm_workspace')
```

Configure the plugin within your `init` function:

```python
@init
def initialise(project):
    project.set_property('project_base_path', project_path)
    project.set_property('pycharm_workspace_project_path', project_path)
```

This will tell the plugin which is the project location in the filesystem. `project_base_path` property value should be
 always the same. It is needed to inform `pycharm_workspace_project_path` too in order to get
  pybuilder_pycharm_workspace working.

Launch the task with:

```console
(venv) C:\Users\foo\PycharmProjects\bar> pyb create_archetype_base
```

### `build.py` file recommended

This plugin doesn't include a `build.py` file due to there should be already one at the moment of the execution of `pyb`
command. The following template can be used along this plugin. Modify as desired.

```python
from pathlib import Path

from pybuilder.core import use_plugin, init, Author, before


use_plugin('python.core')
use_plugin('python.distutils')
use_plugin('python.flake8')
use_plugin('python.unittest')

use_plugin('pypi:pybuilder_pycharm_workspace')
use_plugin('pypi:pybuilder_archetype_base')

project_path = Path(__file__).resolve().parent

name = project_path.name
authors = [Author("foo", 'bar')]
license = "Apache License, Version 2.0"
version = '1.0.0'


@init
def initialise(project):
    project.depends_on_requirements('requirements.txt')

    project.set_property('dir_source_main_python', 'src')

    project.set_property('dir_source_unittest_python', 'tests')
    project.set_property('unittest_module_glob', 'test_*')

    project.set_property('project_base_path', project_path)
    project.set_property('pycharm_workspace_project_path', project_path)


@init(environments='develop')
def initialise_dev(project):
    project.version = f'{project.version}.dev'
    project.set_property('flake8_verbose_output', True)


@init(environments='production')
def initialise_pro(project):
    project.set_property('flake8_break_build', True)
    project.set_property('flake8_include_test_sources', True)


@before('prepare')
def pack_files(project):
    """
    Includes non-Python files in the build.

    :param pybuilder.core.Project project: PyBuilder project instance
    :return: None
    """
    package_path = list(Path(project.get_property('dir_source_main_python')).glob('*'))[0]
    resources_paths = sorted(package_path.glob('**'))[1:]
    project.package_data.update(
        { package_path.name: [str((path.relative_to(package_path) / '*').as_posix()) for path in resources_paths] })
```

Take note of ``build.py`` example on [pybuilder_pycharm_workspace](https://github.com/yeuk0/pybuilder-pycharm-workspace/blob/master/README.md)
plugin README to cover its needs too.

## Properties

Plugin has next properties with provided defaults

| Name | Type | Default Value | Description |
| --- | --- | --- | --- |
| project_base_path | Path | None | Project's path in filesystem (same as `build.py` file). Mandatory |
