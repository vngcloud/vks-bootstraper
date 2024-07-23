# vks-bootstraper ![PyPI](https://img.shields.io/pypi/v/vks-bootstraper?label=pypi%20package)
_The simple CLI tool to bootstrap instances of VKS workload clusters_

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)


<hr>

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
  
- Publish the CLI to PyPi _(make sure you have configured the `$HOME/.pypirc` config file)_
  ```bash
  twine upload dist/*
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