# vks-bootstraper ![PyPI](https://img.shields.io/pypi/v/vks-bootstraper?label=pypi%20package)
_The simple CLI tool to bootstrap instances of VKS workload clusters_

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)


<hr>

# Installation
- Install the `vks-bootstraper:latest` with `pip` tool:
  ```bash
  pip3 install --upgrade vks-bootstraper
  ```

# Build
- Install the Pip dependencies
  ```bash
  pip3 install --upgrade pip
  pip3 install --upgrade -r requirements.txt
  pip3 install --upgrade build twine
  ```

- Build the CLI
  ```bash
  python3 -m build
  twine check dist/*
  ```
  
- Publish the CLI to PyPi _(make sure you have configured the `$HOME/.pypirc` config file, refer this [section](#the-pypirc-config-file) to pre-configure before performing this step)_
  ```bash
  twine upload [--repository pypi] dist/*
  ```

# Others
## The `.pypirc` config file
- The config file should be located at `$HOME/.pypirc`
- The content of the file should be like this:
  ```ini
  [pypi]
    username = __token__
    password = pypi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  ```
  
# Usage
- Run the CLI with the following command:
  ```bash
  vks-bootstraper --help
  ```
  > ```bash
  > ➜   vks-bootstraper --help             
  > Usage: vks-bootstraper [OPTIONS] COMMAND [ARGS]...
  > 
  > Options:
  >   --version  Show the version and exit.
  >   --help     Show this message and exit.
  > 
  > Commands:
  >   add-host                 Add a new host to the /etc/hosts file
  >   generate-ssh-key         Generate the SSH key for the current instance
  >   get-instance-id          Get the vServer ID of the current instance
  >   get-local-ipv4           Get the local IPv4 of the current instance
  >   prepare-kubeadm-config   Prepare the kubeadm config file for the...
  >   waiting-instance-booted  Waiting for the instance to be booted up,...
  >   waiting-internet         Waiting for the instance to reach to the...
  > ```
