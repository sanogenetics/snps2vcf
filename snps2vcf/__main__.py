import logging
import sys

from . import Converter

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.ERROR)

    # read from stdin
    # write to stdout as uncompressed vcf
    converter = Converter()

    # get binary input and output streams
    stdin = sys.stdin.buffer
    stdout = sys.stdout.buffer

    converter.convert(stdin, stdout)
