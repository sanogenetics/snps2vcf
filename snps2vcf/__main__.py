import argparse
import logging
import sys
from . import Converter

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    # read from stdin
    # write to stdout as uncompressed vcf
    converter = Converter()
    converter.convert(sys.stdin, sys.stdout)