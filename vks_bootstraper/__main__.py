"""
Author: Cuong. Duong Manh <cuongdm3@vng.com.vn>
Description: The CLI tool to boostrap the instances of VKS clusters.
"""

import click
from . import metadata, ssh_utils


@click.group()
@click.version_option("1.4.0", prog_name="vks-bootstraper")
def cli():
    pass


cli.add_command(metadata.get_instance_id)  # noqa
cli.add_command(metadata.get_local_ipv4)  # noqa
cli.add_command(metadata.prepare_kubeadm_config)  # noqa
cli.add_command(metadata.waiting_instance_booted)  # noqa
cli.add_command(metadata.waiting_internet)  # noqa
cli.add_command(metadata.add_host)  # noqa
cli.add_command(ssh_utils.generate_ssh_key)  # noqa

# if __name__ == "__main__":
#     cli()
