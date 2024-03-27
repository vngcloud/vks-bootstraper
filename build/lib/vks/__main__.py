"""
Author: Cuong. Duong Manh <cuongdm3@vng.com.vn>
Description: The CLI tool to boostrap the instances of VKS clusters.
"""

import click
from . import metadata
from . import __version__


@click.group()
@click.version_option(__version__, prog_name="vks-bootstraper")
def cli():
    pass


cli.add_command(metadata.get_instance_id)

if __name__ == "__main__":
    cli()
