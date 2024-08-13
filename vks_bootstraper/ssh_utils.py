import os
import click

from sshkey_tools.keys import RsaPrivateKey


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
        click.echo("[INFO] - The SSH key is generated and added to the authorized_keys file")
    except Exception as e:
        click.echo(f"[ERROR] - Failed to generate the SSH key: {e}")
        raise SystemExit(1)
