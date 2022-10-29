#!/bin/bash
set -e
set -x

# build the slim default version
docker build \
  -t snps2vcf:latest \
  -f docker/Dockerfile \
  .
