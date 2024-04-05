"""
Author: Cuong. Duong Manh <cuongdm3@vng.com.vn>
Date: 2023-03-26
Description: The commands calling the metadata service to get the instance information.
"""

import click
import yaml
import requests

_metadata_url_prefix = "http://169.254.169.254"
_metadata_url = _metadata_url_prefix + "/openstack/latest/meta_data.json"
_local_ip_v4_url = _metadata_url_prefix + "/latest/meta-data/local-ipv4"
_kubeadmin_config_path = "/run/kubeadm/kubeadm-join-config.yaml"
_provider_id_prefix = "vngcloud://"


def _get_instance_id():
    response = requests.get(_metadata_url)
    response.raise_for_status()
    try:
        instance_id = response.json()["meta"]["portal_uuid"]
        return instance_id
    except Exception as e:
        raise Exception(f"Cannot get instance ID: {e}")


def _get_local_ip_v4():
    response = requests.get(_local_ip_v4_url)
    response.raise_for_status()
    try:
        ipv4 = response.text
        return ipv4
    except Exception as e:
        raise Exception(f"Cannot get local IPv4: {e}")


@click.command("get-instance-id", help="Get the vServer ID of the current instance")
@click.option("-s", "--short", default=False, is_flag=True, help="Short or long output")
def get_instance_id(short):
    try:
        instance_id = _get_instance_id()
        if short:
            click.echo(instance_id)
        else:
            click.echo(f"Instance ID: {instance_id}")
    except Exception as e:
        click.echo(f"Error: {e}")
        raise SystemExit(1)


@click.command("get-local-ipv4", help="Get the local IPv4 of the current instance")
@click.option("-s", "--short", default=False, is_flag=True, help="Short or long output")
def get_local_ipv4(short):
    try:
        ipv4 = get_local_ipv4()
        if short:
            click.echo(ipv4)
        else:
            click.echo(f"Local IPv4: {ipv4}")
    except Exception as e:
        click.echo(f"Error: {e}")
        raise SystemExit(1)


@click.command("prepare-kubeadm-config", help="Prepare the kubeadm config file for the current instance")
def prepare_kubeadm_config():
    with open(_kubeadmin_config_path, "w+") as stream:
        try:
            kubeadm_config = yaml.safe_load(stream)
            kubeadm_config["nodeRegistration"]["kubeletExtraArgs"]["node-ip"] = _get_local_ip_v4()
            kubeadm_config["nodeRegistration"]["kubeletExtraArgs"][
                "provider-id"] = _provider_id_prefix + _get_instance_id()

            # Write this file
            yaml.dump(kubeadm_config, stream)
            click.echo(f"Kubeadm config file is written to {_kubeadmin_config_path}")

        except yaml.YAMLError as exc:
            click.echo(f"Error: {exc}")
            raise SystemExit(1)
