"""
Author: Cuong. Duong Manh <cuongdm3@vng.com.vn>
Description: The CLI tool to boostrap the instances of VKS clusters.
"""

import click
import requests

_metadata_url = "http://169.254.169.254/openstack/latest/meta_data.json"


@click.command()
@click.option("--short/--long", default=False, help="Short or long output")
def get_instance_id(short):
    response = requests.get(_metadata_url)
    response.raise_for_status()
    try:
        instance_id = response.json()["meta"]["portal_uuid"]
        if short:
            click.echo(instance_id)
        else:
            click.echo(f"Instance ID: {instance_id}")
    except Exception as e:
        click.echo(f"Error: {e}")
        raise SystemExit(1)


@click.group()
def cli():
    pass


cli.add_command(get_instance_id)

if __name__ == "__main__":
    cli()
