SNPs2VCF
========

This is tool for converting direct-to-consumer microarray results into VCF files.

usage
-----

To use, pipe input into the process and pipe the output somewhere. e.g.

```
python -m snps2vcf <input.txt >output.vcf
```

development
===========

```sh
# Create virtual environment
python3 -m venv venv
# Activate virtual environment
source venv/bin/activate

# first install pip tools
pip install pip-tools
# Install exact requirements
pip-sync requirements.txt requirements-dev.txt
# Install editable with development extras
pip install -e '.[dev]'

# before making any commits
# Enable pre-commit hooks
pre-commit install
# Run pre-commit hooks without committing
pre-commit run --all-files
# Note pre-commit is configured to use:
# - isort to sort imports
# - black to format code

# before making any code changes
# Run tests
pytest
# Run tests, print coverage
coverage run -m pytest && coverage report -m
# Type checking
mypy snps2vcf

# after making any dependency changes
# Freeze dependencies
pip-compile
# Freeze dev dependencies
pip-compile requirements-dev.in
# then run pip-sync again to install them!
# Print dependencies
pipdeptree
```

Global git ignores per https://help.github.com/en/github/using-git/ignoring-files#configuring-ignored-files-for-all-repositories-on-your-computer

For release to PyPI see https://packaging.python.org/tutorials/packaging-projects/

To add a new development dependency, add to `requirements-dev.in` then run `pip-compile requirements-dev.in`

To add a new dependency, add to `requirements.in` then run `pip-compile`


docker
------

To build this container, use a command like:

```
docker/build.sh
```

Note: `--rm` means to remove intermediate containers after a build. You may want to omit this if developing locally to utilize docker layer caching.

Note: `--progress=plain` may be useful to see all intermediate step logs.

To use, pipe input into the container and pipe the output somewhere. e.g.

```
docker run -i snps2vcf bash run.sh <input.txt >output.vcf
```

Push to AWS ECR with:

```
aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 244834673510.dkr.ecr.eu-west-2.amazonaws.com
docker tag snps2vcf:latest 244834673510.dkr.ecr.eu-west-2.amazonaws.com/snps2vcf:latest
docker push 244834673510.dkr.ecr.eu-west-2.amazonaws.com/snps2vcf:latest
docker logout
```

Push to DockerHub with:

```
docker login --username sanogenetics
docker tag snps2vcf:latest sanogenetics/snps2vcf:latest
docker push sanogenetics/snps2vcf:latest
docker logout
```

Note: will prompt for password.
