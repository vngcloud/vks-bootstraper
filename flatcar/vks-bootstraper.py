#!/usr/bin/python

"""
Author: Cuong. Duong Manh <cuongdm3@vng.com.vn>
Description: The CLI tool to boostrap the instances of VKS clusters.
"""


import click
import time
import yaml
import requests
import os

from python_hosts import Hosts, HostsEntry
from sshkey_tools.keys import RsaPrivateKey

_vcr_url = "https://vcr.vngcloud.vn"  # The VngCloud Registry URL domain
_metadata_url_prefix = "http://169.254.169.254"
_metadata_url = _metadata_url_prefix + "/openstack/latest/meta_data.json"
_local_ip_v4_url = _metadata_url_prefix + "/latest/meta-data/local-ipv4"
_kubeadmin_config_path = "/run/kubeadm/kubeadm-join-config.yaml"
_provider_id_prefix = "vngcloud://"


def _get_instance_id():
    start = time.time()

    while True:
        try:
            # timeout of 5 seconds
            response = requests.get(_metadata_url, timeout=5)
            if response.status_code >= 200 and response.status_code < 300:  # noqa
                instance_id = response.json()["meta"]["portal_uuid"]
                return instance_id
        except (Exception,) as e:
            click.echo(f"[ERROR] - CANNOT get the instance ID: {e}")

        if time.time() - start > 1800:  # greater than 30 minutes
            raise Exception("CANNOT get the instance ID")

        time.sleep(10)


def _precheck_vngcloud_services():
    start = time.time()

    while True:
        try:
            # timeout of 5 seconds
            response = requests.get(_vcr_url, timeout=5)
            if response.status_code >= 200 and response.status_code < 300:  # noqa
                return
        except (Exception,) as e:
            click.echo(f"[ERROR] - CANNOT reach to the VngCloud services: {e}")

        if time.time() - start > 1800:  # greater than 30 minutes
            raise Exception("CANNOT reach to the external internet")

        time.sleep(10)


def _waiting_instance_booted():
    phase = "metadata"
    while True:
        if phase == "metadata":
            _get_local_ipv4()
            phase = "done"
        elif phase == "done":
            break


def _waiting_the_internet():
    phase = "internet"
    while True:
        if phase == "internet":
            _precheck_vngcloud_services()
            phase = "done"
        elif phase == "done":
            break


def _get_local_ipv4():
    start = time.time()

    while True:
        try:
            # timeout of 5 seconds
            response = requests.get(_local_ip_v4_url, timeout=5)
            if response.status_code >= 200 and response.status_code < 300:  # noqa
                ipv4 = response.text
                return ipv4
        except (Exception,) as e:
            click.echo(f"[ERROR] - CANNOT get the local IPv4: {e}")

        if time.time() - start > 1800:  # greater than 30 minutes
            raise Exception("CANNOT get the local IPv4")

        time.sleep(10)


def _add_host(file_path: str, domain: str, ipaddress: str):
    hosts = Hosts(path=file_path)
    new_entry = HostsEntry(
        entry_type="ipv4", address=ipaddress, names=[domain])
    hosts.add([new_entry], True)
    hosts.write()


@click.command("add-host", help="Add a new host to the /etc/hosts file")
@click.option("-d", "--domain", required=True, help="The domain name")
@click.option("-i", "--ipaddress", required=True, help="The IP address")
@click.option("-f", "--file-path", default="/etc/hosts", help="The file path of the hosts file")
def add_host(domain, ipaddress, file_path):
    try:
        _add_host(file_path, domain, ipaddress)
        click.echo(
            f"[INFO] - The host {domain} with IP {ipaddress} is added to the {file_path} file")
    except Exception as e:
        click.echo(
            f"[ERROR] - Failed to add the host to the {file_path} file: {e}")
        raise SystemExit(1)


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
        click.echo(f"[ERROR] - Failed to get instance ID: {e}")
        raise SystemExit(1)


@click.command("get-local-ipv4", help="Get the local IPv4 of the current instance")
@click.option("-s", "--short", default=False, is_flag=True, help="Short or long output")
def get_local_ipv4(short):
    try:
        ipv4 = _get_local_ipv4()
        if short:
            click.echo(ipv4)
        else:
            click.echo(f"Local IPv4: {ipv4}")
    except Exception as e:
        click.echo(f"[ERROR] - Failed to get local IPv4 address: {e}")
        raise SystemExit(1)


@click.command("prepare-kubeadm-config", help="Prepare the kubeadm config file for the current instance")
def prepare_kubeadm_config():
    kubeadm_cfg_content = None
    with open(_kubeadmin_config_path, "r") as stream:
        try:
            kubeadm_config = yaml.safe_load(stream)
            kubeadm_config["nodeRegistration"]["kubeletExtraArgs"]["node-ip"] = _get_local_ipv4()
            kubeadm_config["nodeRegistration"]["kubeletExtraArgs"][
                "provider-id"] = _provider_id_prefix + _get_instance_id()
            kubeadm_cfg_content = kubeadm_config

            click.echo(f"[INFO] - Kubeadm config: {kubeadm_config}")
        except yaml.YAMLError as exc:
            click.echo(
                f"[ERROR] - Failed to load kubeadm configuration file: {exc}")
            raise SystemExit(1)

    with open(_kubeadmin_config_path, "w") as stream:
        try:
            if kubeadm_cfg_content is None:
                click.echo("[ERROR] - The kubeadm config content is empty")
                raise SystemExit(1)

            # Write this file
            yaml.dump(kubeadm_cfg_content, stream)
            click.echo(
                f"[INFO] - Kubeadm config content is written to {_kubeadmin_config_path}")

        except yaml.YAMLError as exc:
            click.echo(
                f"[ERROR] - Failed to write kubeadm config content: {exc}")
            raise SystemExit(1)


@click.command("waiting-instance-booted",
               help="Waiting for the instance to be booted up, connect to the metadata service and reach to the VngCloud services")
def waiting_instance_booted():
    try:
        _waiting_instance_booted()
        click.echo("[INFO] - The instance is booted up and ready to use")
    except Exception as e:
        click.echo(
            f"[ERROR] - Failed to wait for the instance to be booted up: {e}")
        raise SystemExit(1)


@click.command("waiting-internet",
               help="Waiting for the instance to reach to the external internet and the VngCloud services")
def waiting_internet():
    try:
        _waiting_the_internet()
        click.echo(
            "[INFO] - The instance is connected to the external internet and the VngCloud services")
    except Exception as e:
        click.echo(
            f"[ERROR] - Failed to wait for the instance to reach to the external internet: {e}")
        raise SystemExit(1)


def _generate_ssh_key():
    # check if exists key, ignore
    if os.path.exists(os.path.expanduser('~/.ssh/id_rsa')):
        click.echo("[INFO] - The SSH key is already generated")
        return

    click.echo("[INFO] - Generating the SSH key")

    path_priv = os.path.expanduser('~/.ssh/vngcloud_rsa')
    path_pub = os.path.expanduser('~/.ssh/vngcloud_rsa.pub')
    path_auth = os.path.expanduser('~/.ssh/authorized_keys')
    dir_ssh = os.path.expanduser('~/.ssh')

    os.system(f"mkdir -p {dir_ssh}")
    os.system(f"touch {path_priv} {path_pub} {path_auth}")

    rsa_priv = RsaPrivateKey.generate()
    try:
        rsa_priv.to_file(path_priv)
        rsa_priv.public_key.to_file(path_pub)
    except Exception as e:
        click.echo(f"[ERROR] - Failed to generate the SSH key: {e}")
        raise SystemExit(1)

    # load the public key
    pub_key = f"\n\n{rsa_priv.public_key.to_string().strip()} stackops@vng.com.vn"

    # add the public key to the authorized_keys file
    os.system(f"echo '{pub_key}' >> {path_auth}")

    # change the permission of the private key
    os.system(f"chmod 600 {path_priv}")


@click.command("generate-ssh-key", help="Generate the SSH key for the current instance")
def generate_ssh_key():
    try:
        _generate_ssh_key()
        click.echo(
            "[INFO] - The SSH key is generated and added to the authorized_keys file")
    except Exception as e:
        click.echo(f"[ERROR] - Failed to generate the SSH key: {e}")
        raise SystemExit(1)


@click.group()
@click.version_option("1.4.0", prog_name="vks-bootstraper")
def cli():
    pass


cli.add_command(get_instance_id)  # noqa
cli.add_command(get_local_ipv4)  # noqa
cli.add_command(prepare_kubeadm_config)  # noqa
cli.add_command(waiting_instance_booted)  # noqa
cli.add_command(waiting_internet)  # noqa
cli.add_command(add_host)  # noqa
cli.add_command(generate_ssh_key)  # noqa

if __name__ == "__main__":
    cli()
