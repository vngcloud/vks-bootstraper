"""
Author: Cuong. Duong Manh <cuongdm3@vng.com.vn>
Description: The CLI tool to boostrap the instances of VKS clusters.
"""

import click
from . import metadata


@click.group()
@click.version_option("0.2.0", prog_name="vks-bootstraper")
def cli():
    pass


cli.add_command(metadata.get_instance_id)  # noqa
cli.add_command(metadata.get_local_ipv4)  # noqa
cli.add_command(metadata.prepare_kubeadm_config)  # noqa

# if __name__ == "__main__":
#     cli()
