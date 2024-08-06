#!/bin/sh
set -e
set -x
set -u

# arg 1 is the input s3 url
# arg 2 is the output s3 url
# args other are passed to snps2vcf

# TODO optionally integrate with AWS S3

. venv/bin/activate && python3.12 -m snps2vcf <&0 >&1
