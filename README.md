[![CI](https://github.com/sanogenetics/snps2vcf/actions/workflows/ci.yml/badge.svg)](https://github.com/sanogenetics/snps2vcf/actions/workflows/ci.yml) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

snps2vcf
========

`snps2vcf` is a tool for converting direct-to-consumer microarray results into
[VCF](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3137218/) files using the
[`snps`](https://pypi.org/project/snps/) package.

usage
-----

To use, pipe input into the process and pipe the output somewhere. e.g.

```
python -m snps2vcf < input.txt.gz > output.vcf
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
# Install editable snps2vcf with development extras
pip install -e '.[dev]'

# before making any code changes
# Run tests
pytest --cov-report=html --cov=snps2vcf tests
# Linting
ruff check --fix
# Formatting
ruff format
# Type checking
mypy --strict snps2vcf

# after making any dependency changes
# Freeze dependencies
pip-compile
# Freeze dev dependencies
pip-compile requirements-dev.in
# then run pip-sync again to install them!
```

Global git ignores per https://help.github.com/en/github/using-git/ignoring-files#configuring-ignored-files-for-all-repositories-on-your-computer

For release to PyPI see https://packaging.python.org/tutorials/packaging-projects/

To add a new development dependency, add to `requirements-dev.in` then run `pip-compile requirements-dev.in`

To add a new dependency, add to `requirements.in` then run `pip-compile`


docker
------

To build this container, use the following command:

```
docker/build.sh
```

Input and output to the container can be passed either via `stdin` / `stdout`
or by mapping the local filesystem to the container and passing file arguments.
Both options create the output file (`output.vcf`) in the current directory.

**Using `stdin` / `stdout`**
```
docker run --rm -i snps2vcf sh run.sh < input.txt.gz > output.vcf
```

**Using File Arguments**
```
docker run --rm -v $(pwd)/input.txt.gz:/app/input.txt.gz -v $(pwd):/app/output_dir snps2vcf sh run.sh /app/input.txt.gz /app/output_dir/output.vcf
```

acknowledgements
----------------
`snps2vcf` incorporates code and concepts generated with the assistance of
[OpenAI's](https://openai.com) [ChatGPT](https://chatgpt.com). ✨
