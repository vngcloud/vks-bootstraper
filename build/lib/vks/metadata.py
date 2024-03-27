"""
Author: Cuong. Duong Manh <cuongdm3@vng.com.vn>
Date: 2023-03-26
Description: The commands calling the metadata service to get the instance information.
"""

import click
import requests

_metadata_url = "http://169.254.169.254/openstack/latest/meta_data.json"


@click.command("get-instance-id", help="Get the vServer ID of the current instance")
@click.option("-s", "--short", default=False, is_flag=True, help="Short or long output")
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
