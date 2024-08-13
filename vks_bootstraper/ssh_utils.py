import os
import click

from sshkey_tools.keys import RsaPrivateKey


def _generate_ssh_key():
    # check if exists key, ignore
    if os.path.exists(os.path.expanduser('~/.ssh/id_rsa')):
        click.echo("[INFO] - The SSH key is already generated")
        return

    rsa_priv = RsaPrivateKey.generate()
    try:
        rsa_priv.to_file("~/.ssh/vngcloud_rsa")
        rsa_priv.public_key.to_file("~/.ssh/vngcloud_rsa.pub")
    except Exception as e:
        click.echo(f"[ERROR] - Failed to generate the SSH key: {e}")
        raise SystemExit(1)

    # add the public key to the authorized_keys file
    os.system(f"cat ~/.ssh/vngcloud_rsa.pub >> ~/.ssh/authorized_keys")

    # change the permission of the private key
    os.system("chmod 600 ~/.ssh/vngcloud_rsa")

    click.echo("[INFO] - The SSH key is generated and added to the authorized_keys file")


@click.command("generate-ssh-key", help="Generate the SSH key for the current instance")
def generate_ssh_key():
    try:
        _generate_ssh_key()
        click.echo("[INFO] - The SSH key is generated and added to the authorized_keys file")
    except Exception as e:
        click.echo(f"[ERROR] - Failed to generate the SSH key: {e}")
        raise SystemExit(1)
