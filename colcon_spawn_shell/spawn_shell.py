# Copyright 2018 Shane Loretz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path
import sys

from colcon_core.plugin_system import satisfies_version
from colcon_core.plugin_system import SkipExtensionException
from colcon_core.shell import logger
from colcon_core.shell import ShellExtensionPoint
from colcon_core.shell import use_all_shell_extensions
from colcon_core.shell.template import expand_template


class SpawnBashShell(ShellExtensionPoint):
    """Generate spawn_shell.bash script."""
    # Use lower priority than default because this is 'non-primary'
    PRIORITY = ShellExtensionPoint.PRIORITY - 10

    def __init__(self):
        super().__init__()
        satisfies_version(ShellExtensionPoint.EXTENSION_POINT_VERSION, '^2.0')
        if sys.platform == 'win32' and not use_all_shell_extensions:
            raise SkipExtensionException('Not used on Windows systems')

    def create_prefix_script(self, prefix_path, merge_install):
        # Use parent of prefix_path to display a pretty workspace name
        workspace_name = 'unknown'
        if len(prefix_path.parts) >= 2:
            workspace_name = prefix_path.parts[-2]

        output_path = prefix_path / 'spawn_shell.bash'
        logger.info("Creating '{output_path}'".format_map(locals()))
        expand_template(
            Path(__file__).parent / 'template' / 'spawn_shell.bash.em',
            output_path,
            {
                'workspace_name': workspace_name
            })

    def create_package_script(self, prefix_path, pkg_name, hooks):
        # No package-specific script required
        pass
