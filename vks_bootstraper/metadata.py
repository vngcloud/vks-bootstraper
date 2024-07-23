"""
Author: Cuong. Duong Manh <cuongdm3@vng.com.vn>
Date: 2023-03-26
Description: The commands calling the metadata service to get the instance information.
"""

import click
import time
import yaml
import requests

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
            response = requests.get(_metadata_url, timeout=5)  # timeout of 5 seconds
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
            response = requests.get(_vcr_url, timeout=5)  # timeout of 5 seconds
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
            phase = "services"
        elif phase == "services":
            _precheck_vngcloud_services()
            phase = "done"
        elif phase == "done":
            break


def _get_local_ipv4():
    start = time.time()

    while True:
        try:
            response = requests.get(_local_ip_v4_url, timeout=5)  # timeout of 5 seconds
            if response.status_code >= 200 and response.status_code < 300:  # noqa
                ipv4 = response.text
                return ipv4
        except (Exception,) as e:
            click.echo(f"[ERROR] - CANNOT get the local IPv4: {e}")

        if time.time() - start > 1800:  # greater than 30 minutes
            raise Exception("CANNOT get the local IPv4")

        time.sleep(10)


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
            click.echo(f"[ERROR] - Failed to load kubeadm configuration file: {exc}")
            raise SystemExit(1)

    with open(_kubeadmin_config_path, "w") as stream:
        try:
            if kubeadm_cfg_content is None:
                click.echo("[ERROR] - The kubeadm config content is empty")
                raise SystemExit(1)

            # Write this file
            yaml.dump(kubeadm_cfg_content, stream)
            click.echo(f"[INFO] - Kubeadm config content is written to {_kubeadmin_config_path}")

        except yaml.YAMLError as exc:
            click.echo(f"[ERROR] - Failed to write kubeadm config content: {exc}")
            raise SystemExit(1)


@click.command("waiting-instance-booted",
               help="Waiting for the instance to be booted up, connect to the metadata service and reach to the VngCloud services")
def waiting_instance_booted():
    try:
        _waiting_instance_booted()
        click.echo("[INFO] - The instance is booted up and ready to use")
    except Exception as e:
        click.echo(f"[ERROR] - Failed to wait for the instance to be booted up: {e}")
        raise SystemExit(1)
