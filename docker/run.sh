#!/bin/sh
set -e
set -x
set -u

. venv/bin/activate

if [ "$#" -eq 0 ]; then
  # No arguments, use stdin and stdout
  python3.12 -m snps2vcf <&0 >&1
elif [ "$#" -eq 2 ]; then
  # Two arguments, use input and output files
  input_file="$1"
  output_file="$2"
  python3.12 -m snps2vcf "$input_file" "$output_file"
else
  echo "Invalid arguments"
  exit 1
fi
