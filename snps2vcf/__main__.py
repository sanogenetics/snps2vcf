import io
import logging
import sys

from . import Converter

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.ERROR)

    # read from stdin
    # write to stdout as uncompressed vcf
    converter = Converter()

    # Create TextIOWrapper objects from the existing streams
    stdin_wrapper = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
    stdout_wrapper = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

    converter.convert(stdin_wrapper, stdout_wrapper)
